# coding: utf-8
import time
import logging

from werkzeug.wrappers import Request, Response


class APIMiddleware(object):
    def __init__(self, old_wsgi_app):
        self.old_wsgi_app = old_wsgi_app

    def _handle_request(self, request):
        """
        处理请求
        :return:
        """

    def _handle_response(self, response):
        """
        处理返回
        :return:
        """

    def __call__(self, environ, start_response):
        self._handle_request(Request(environ, shallow=True))
        start_time = time.time()
        # 请求之前

        ret = self.old_wsgi_app(environ, start_response)

        # 请求之后
        during = time.time() - start_time
        logging.info('request during: {}'.format(during))
        self._handle_response(Response(environ))
        return ret


MIDDLEWARE_CHAIN = [
    APIMiddleware
]
