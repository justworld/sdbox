# coding: utf-8
import logging
import json
from functools import wraps
from enum import Enum
from importlib import import_module
from django.test import TestCase
from django.conf import settings


class RequestMethod(Enum):
    Get = 0
    Post = 1
    Put = 2
    Delete = 3


class BaseTestCase(TestCase):
    mock_data = dict()
    mock_data_key = None

    def setUp(self):
        # 加载mock里的默认参数
        mock_data_path = getattr(settings, 'TEST_MOCK_DATA_MODULE', '')
        if not mock_data_path:
            mock_data_path = 'tests.mock'
        try:
            mock_data_module = import_module(mock_data_path)
            self.mock_data = mock_data_module.get_data(self.mock_data_key)
        except:
            pass
        self.base_url = self.mock_data.get('base_url', '')
        self.default_header = self.mock_data.get('header', dict())

        self.class_name = self.__class__.__name__
        logging.info('%s 类的 %s 函数测试开始...', self.class_name, self._testMethodName)

    def tearDown(self):
        logging.info('%s 类的 %s 函数测试完毕。。。\r\n', self.class_name, self._testMethodName)

    def send_request(self, method, uri, data=None, header=None):
        """
        获取请求
        """
        merge_header = self.merge_default_header(header)

        if self.base_url:
            uri = self.base_url + uri
            if not uri.endswith('/'):
                uri = uri + '/'

        if method == RequestMethod.Get:
            response = self.client.get(uri, data, **merge_header)
        else:
            if method == RequestMethod.Post:
                func = self.client.post
            elif method == RequestMethod.Put:
                func = self.client.put
            elif method == RequestMethod.Delete:
                func = self.client.delete
            if not isinstance(data, str):
                data = json.dumps(data)
            response = func(uri, data, content_type='application/json', **merge_header)

        logging.warning(
            '请求url：{}, 请求数据：{}, 请求header：{}, 响应：{}'.format(uri, str(data), str(merge_header), str(response.content)))

        return response

    def merge_default_header(self, header):
        merge_header = self.default_header
        if header:
            merge_header = dict(merge_header, **header)
        return merge_header

    def get_mock_data(self, key):
        """
        获取指定key的mock data
        """
        if self.mock_data:
            if key in self.mock_data:
                return self.mock_data.get(key)
        return None

    def split_mock_data(self, ori_data):
        data = ori_data.get('data', None)
        header = ori_data.get('header', None)
        disable = ori_data.get('disable', False)
        return data, header, disable


def batch_request(route, key, method=RequestMethod.Get):
    """
    批量请求
    """

    def decorator(func):
        @wraps(func)
        def wrapper(cls, res=None):
            mock_data = cls.get_mock_data(key)
            if mock_data:
                for i in mock_data:
                    data, header, disable = cls.split_mock_data(i)
                    if disable:
                        continue
                    response = cls.send_request(method, route, data=data, header=header)
                    func(cls, response)

        return wrapper

    return decorator
