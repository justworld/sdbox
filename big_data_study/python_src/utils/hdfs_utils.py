# coding: utf-8
# hdfs 文件操作
import os
import glob
from hdfs import InsecureClient
from snakebite.client import Client as QuickClient


class QuickHdfsProxy:
    """
    应该会更快，还没有测试
    """

    # todo 连接关闭
    # todo 连接池或单例
    def __init__(self, host='127.0.0.1', port=9000):
        self.client = QuickClient(host=host, port=port)

    def __getattr__(self, key):
        return getattr(self.client, key)


class HdfsProxy:
    # todo 连接关闭
    # todo 连接池或单例
    def __init__(self, url='http://127.0.0.1:50070'):
        self.client = InsecureClient(url=url, user='hadoop')

    def __getattr__(self, key):
        return getattr(self.client, key)

    def batch_upload(self, parent_path, local_path):
        for i in glob.glob(local_path):
            file_name = os.path.basename(i)
            self.upload('{}/{}'.format(parent_path, file_name), i)


if __name__ == '__main__':
    fs = HdfsProxy()
    fs.makedirs('/home/hadoop/input')
    fs.list('/home/hadoop')
    # fs.write('/home/hadoop/input/test.txt', 'hello,world')
    fs.batch_upload('/home/hadoop/input/', '../input/01/*.txt')
    fs.list('/home/hadoop/input')
