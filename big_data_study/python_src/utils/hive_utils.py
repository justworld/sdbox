# coding: utf-8
from pyhive import hive


# todo: 支持with，连接池
class CursorProxy:
    def __init__(self, host='localhost', database='test'):
        self.cursor = hive.Connection(host=host, auth='NOSASL', database=database).cursor()

    def fetchall_dict(self, sql, params=None):
        self.cursor.execute(sql, parameters=params)
        return self.parse_data(self.cursor.description, self.cursor.fetchall())

    def fetchone_dict(self, sql, params=None):
        self.cursor.execute(sql, parameters=params)
        return self.parse_data(self.cursor.description, self.cursor.fetchone(), True)

    def __getattr__(self, key):
        return getattr(self.cursor, key)

    def parse_data(self, desc, data, single=False):
        row_headers = [x[0].split('.')[-1] for x in desc]
        if single:
            return dict(zip(row_headers, data))
        return [dict(zip(row_headers, row)) for row in data]


if __name__ == '__main__':
    cursor = CursorProxy()
    data1 = cursor.fetchall_dict('select * from student')
    print data1
    data2 = cursor.fetchall_dict('select * from student where age=18')
    print data2
