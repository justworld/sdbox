# coding: utf-8
# 美国百年气温数据分析
# 指标如下：
# 最高气温、各年代最高气温、各地区最高气温，各年代地区最高气温
# 最低气温、各年代最低气温、各地区最低气温，各年代地区最低气温
# 平均气温、各年代平均气温、各地区平均气温，各年代地区平均气温
# 最大温差，各年代最大温差，各地区最大温差，各年代地区最大温差
# 文件格式 area，type，value
import time
import os
import re
from python_src.utils import hive_utils, spark_utils, hbase_utils, hdfs_utils

NUM_MATCH = re.compile(r'\d+')


def process_val(val):
    return str(int(val))


def run_hive():
    """
    hive方式
    """
    # 初始化
    cursor = hive_utils.CursorProxy()
    exist_tables = [i['tab_name'] for i in cursor.fetchall_dict("show tables")]
    if 'temperature' not in exist_tables:
        # 建表
        cursor.execute('''create table temperature(area string, type string, value int)
        partitioned by(year int)
        row format delimited fields terminated by ","
         ''')
        # 初始化数据
        base_path = '/home/linux/Documents/python/hadoop-example/input/01'
        for file in os.listdir(base_path):
            file_path = os.path.join(base_path, file)
            year = int(NUM_MATCH.findall(file)[0])
            cursor.execute('load data local inpath "{}" into table temperature partition(year={})'.format(
                file_path, year))

    # 总体
    all_val = cursor.fetchone_dict('select max(value) as max, avg(value) as avg, min(value) as min  from temperature')
    # 各年代
    year_val = cursor.fetchall_dict(
        'select max(value) as max, avg(value) as avg, min(value) as min, year from temperature group by year')
    # 各地区（数量太大，待优化）
    area_val = cursor.fetchall_dict(
        'select max(value) as max, avg(value) as avg, min(value) as min, area from temperature group by area limit 100')
    # 各年代地区（数量太大，只计算）
    year_area_val = cursor.fetchall_dict(
        'select max(value) as max, avg(value) as avg, min(value) as min, area, year from temperature group by area, year limit 100')

    # 结果更新到hbase，方便查询
    insert_data = {}
    insert_data['all'] = {'stat:max': process_val(all_val['max']), 'stat:avg': process_val(all_val['avg']),
                          'stat:min': process_val(all_val['min']),
                          'stat:sub': process_val(all_val['max'] - all_val['min'])}

    for row in year_val:
        insert_data.setdefault(str(row['year']), {}).update({'stat:max': process_val(row['max']),
                                                             'stat:avg': process_val(row['avg']),
                                                             'stat:min': process_val(row['min']),
                                                             'stat:sub': process_val(row['max'] - row['min'])})
    for row in area_val:
        insert_data.setdefault(str(row['area']), {}).update({'stat:max': process_val(row['max']),
                                                             'stat:avg': process_val(row['avg']),
                                                             'stat:min': process_val(row['min']),
                                                             'stat:sub': process_val(row['max'] - row['min'])})
    for row in year_area_val:
        insert_data.setdefault('{},{}'.format(row['year'], row['area']), {}).update(
            {'stat:max': process_val(row['max']), 'stat:avg': process_val(row['avg']),
             'stat:min': process_val(row['min']),
             'stat:sub': process_val(row['max'] - row['min'])})

    hb = hbase_utils.HbasePoolProxy()
    hbase_tables = hb.tables()
    if 'temperature' not in hbase_tables:
        # 建表
        hb.create_table(
            'temperature',
            {'stat': dict()}
        )
    table = hb.table('temperature')
    # 批量插入
    with table.batch() as batch:
        for key, val in insert_data.items():
            batch.put(key, val)


def run_spark():
    """
    spark方式
    """
    sc = spark_utils.SparkProxy()
    fs = hdfs_utils.HdfsProxy()
    dirs = fs.list('/home/hadoop')
    if 'spark' not in dirs:
        # 上传文件到hdfs
        fs.makedirs('/home/hadoop/spark')
        fs.batch_upload('/home/hadoop/spark/', '../input/01/*.txt')

    files = sc.wholeTextFiles('hdfs://localhost:9000/home/hadoop/spark/')

    def flat_map(data):
        f, lines = data
        # 解析出年份一起返回
        file_name = os.path.basename(f)
        year = int(NUM_MATCH.findall(file_name)[0])
        return [[year] + line.split(",") for line in lines.splitlines()]

    def base_map(data):
        if len(data) == 4:
            return data[:3] + [int(data[3])]

    def area_map(data):
        return (data[1], data[3])

    def year_map(data):
        return (data[0], data[3])

    def area_year_map(data):
        return ((data[1], data[0]), data[3])

    def sub_map(data):
        return max(data) - min(data)

    def append(a, b):
        a.append(b)
        return a

    def extend(a, b):
        a.extend(b)
        return a

    ori_rdd = files.flatMap(flat_map).map(base_map)

    # todo: 减少运算次数
    # 最高气温
    max_val = ori_rdd.map(lambda x: x[3]).max()
    # 各年代最高气温
    max_year_val = ori_rdd.map(year_map).combineByKey(lambda x: [x], append, extend).mapValues(max).collect()
    # 各地区最高气温（数量太大，待优化）
    max_area_val = ori_rdd.map(area_map).combineByKey(lambda x: [x], append, extend).mapValues(max).take(100)
    # 各年代地区最高气温（数量太大，待优化）
    max_year_area_val = ori_rdd.map(area_year_map).combineByKey(lambda x: [x], append, extend).mapValues(max).take(100)

    # 平均气温
    avg_val = ori_rdd.map(lambda x: x[3]).mean()
    # 各年代平均气温
    avg_year_val = ori_rdd.map(year_map).combineByKey(lambda x: [x], append, extend).aggregateByKey(
        (0, 0), lambda x, y: (x[0] + sum(y), x[1] + len(y)), lambda x, y: (x[0] + y[0], x[1] + y[1])).mapValues(
        lambda x: x[0] / x[1]).collect()
    # 各地区平均气温
    avg_area_val = ori_rdd.map(area_map).combineByKey(lambda x: [x], append, extend).aggregateByKey(
        (0, 0), lambda x, y: (x[0] + sum(y), x[1] + len(y)), lambda x, y: (x[0] + y[0], x[1] + y[1])).mapValues(
        lambda x: x[0] / x[1]).take(100)
    # 各年代地区平均气温
    avg_year_area_val = ori_rdd.map(area_year_map).combineByKey(lambda x: [x], append, extend).aggregateByKey(
        (0, 0), lambda x, y: (x[0] + sum(y), x[1] + len(y)), lambda x, y: (x[0] + y[0], x[1] + y[1])).mapValues(
        lambda x: x[0] / x[1]).take(100)

    # 最大温差
    sub_rdd = ori_rdd.map(lambda x: x[3])
    sub_val = sub_rdd.max() - sub_rdd.min()
    # 各年代最大温差
    sub_year_val = ori_rdd.map(year_map).combineByKey(lambda x: [x], append, extend).mapValues(sub_map).collect()
    # 各地区最大温差
    sub_area_val = ori_rdd.map(area_map).combineByKey(lambda x: [x], append, extend).mapValues(sub_map).take(100)
    # 各年代地区最大温差
    sub_area_year_val = ori_rdd.map(area_year_map).combineByKey(lambda x: [x], append, extend).mapValues(
        sub_map).take(100)

    # 结果更新到hbase，方便查询


def main():
    hive_start = time.time()
    # run_hive()
    print 'hive执行时间：{}'.format(time.time() - hive_start)

    spark_start = time.time()
    run_spark()
    print 'spark执行时间：{}'.format(time.time() - spark_start)
