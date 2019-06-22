# coding: utf-8

def flash_sale(cache_key, cache_func):
    """
    处理类似限时抢购问题
    限时抢购涉及库存问题，多请求下减库存可能会出现脏数据
    通过加锁减库存不能适应高并发
    使用redis可以解决，redis本身是单进程，使用DECR减库存，使用SETNX加锁写库存
    后续优化点：分布式锁、写库存
    todo: 加入pfbox
    :param cache_key: 缓存key
    :param cache_func: 写入缓存的方法
    :return:
    """

    def _set():
        """
        将库存写入缓存
        :return:
        """

    if not cache_key or not cache_func or not hasattr(cache_func, '__call__'):
        return


if __name__ == '__main__':
    # 测试限时抢购
    flash_sale('', '')
