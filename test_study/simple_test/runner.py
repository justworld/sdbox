# coding: utf-8
from django.test.runner import DiscoverRunner


class ExistDatabaseRunner(DiscoverRunner):
    """
    不创建或销毁unit test数据库
    """

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass
