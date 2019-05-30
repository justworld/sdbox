# coding: utf-8
from pyspark import SparkContext


class SparkProxy:
    def __init__(self, app_name=None):
        self.sc = SparkContext(appName=app_name)

    def __getattr__(self, key):
        return getattr(self.sc, key)


if __name__ == '__main__':
    sc = SparkProxy()
    lines = sc.parallelize(["hello,world", "ok,my,friend", "just,do,this,my,friend"])
    words = lines.flatMap(lambda line: line.split(','))
    result = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)


    # print result.collect()

    def test_persist(key):
        print 'run'
        return (key, 1)


    result1 = words.map(test_persist)
    # print result1.count()
    # print result1.count()
    # result1.persist()
    # print result1.count()
    # # 不再计算
    # print result1.count()

    data = sc.parallelize([('1880', 'a,12\nb,23'), ('1881', 'a,2\nb,3')])


    def f(data):
        year, lines = data
        return [line.split(",") + [year] for line in lines.splitlines()]


    def f1(data):
        return (data[0], int(data[1]))


    def f2(data):
        return (data[2], int(data[1]))


    def append(a, b):
        a.append(b)
        return a


    def extend(a, b):
        a.extend(b)
        return a


    ori = data.flatMap(f)
    ori1 = ori.map(f1).combineByKey(lambda x: [x], append, extend).aggregateByKey((0, 0), lambda x, y: (x[0] + sum(y), x[1] + len(y)), lambda x, y: (x[0] + y[0], x[1] + y[1])).mapValues(lambda x:x[0]/x[1]).collect()
    ori2 = ori.map(f2).combineByKey(lambda x: [x], append, extend).collect()
    print ori1
    print ori2
