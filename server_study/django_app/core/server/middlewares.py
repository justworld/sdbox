# coding: utf-8
import os
import socket
import logging
import time

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

logger = logging.getLogger('django.request')

# 本进程信息
PROCESS_INFO = '{}-{}'.format(socket.gethostname(), os.getpid())


class APIMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request_method = request.method.upper()
        # 拦截 OPTIONS以及不知名请求
        if request_method in ('OPTIONS', 'UNKNOWN'):
            return HttpResponse(content='SUCCESS', content_type='text/plain')

    def process_view(self, request, view_func, view_args, view_kwargs):
        start_time = time.time()
        url = request.get_full_path()
        error = None

        try:
            # 添加处理逻辑
            response = view_func(request, *view_args, **view_kwargs)
            return response
        except Exception as e:
            error = e
            raise
        finally:
            # 执行时间
            duration = time.time() - start_time
            # 正常执行的请求
            if error is None:
                logger.info(
                    '请求: {}, method: {}, 执行时间: {}, 进程信息: {}'.format(url, request.method, duration, PROCESS_INFO))
            # 有异常的请求
            else:
                logger.error('请求: {}, method: {}, 执行时间: {}, 进程信息: {}, 出现错误: {}'.format(
                    url, request.method, duration, PROCESS_INFO, error), exc_info=error)
