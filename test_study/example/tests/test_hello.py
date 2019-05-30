# coding: utf-8
from simple_test.base_test import BaseTestCase, RequestMethod, batch_request


class TestHello(BaseTestCase):
    mock_data_key = 'hello'

    def test_get(self):
        route = 'hget'
        response = self.send_request(RequestMethod.Get, route, data={'name': 'test'})
        # 添加判断逻辑
        self.assertIsNotNone(response)

    @batch_request('hpost', 'hpost', RequestMethod.Post)
    def test_post(self, response):
        self.assertIsNotNone(response)
