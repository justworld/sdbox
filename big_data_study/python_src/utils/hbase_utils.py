# coding: utf-8
# hbase操作
# todo: 支持with，连接池
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from happybase import Connection


class HbaseProxy:
    def __init__(self):
        socket = TSocket.TSocket('127.0.0.1', 9090)
        socket.setTimeout(5000)

        transport = TTransport.TBufferedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)

        self.client = Hbase.Client(protocol)
        socket.open()


class HbasePoolProxy:
    def __init__(self):
        self.conn = Connection()

    def __getattr__(self, key):
        return getattr(self.conn, key)


if __name__ == '__main__':
    hb = HbasePoolProxy()
    print hb.tables()
    table = hb.table('test1')
    table.put('3', {'cf:c1': 1})
    for r in table.scan(include_timestamp=True):
        print r
    a = table.row('1')
    print table.cells('1', 'cf', include_timestamp=True)
