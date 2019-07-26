# coding: utf-8
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from django.conf import settings

# 预设 log 输出格式
format_str = "[%(asctime)s] [%(module)s.%(funcName)s:%(lineno)s] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.WARNING, format=format_str)


class DefaultFileHandler(TimedRotatingFileHandler):
    def __init__(self):
        project_name = getattr(settings, "PROJECT_NAME", 'logs')
        log_path = os.path.abspath('logs')
        if not os.path.isdir(log_path):
            os.makedirs(log_path)
        filename = os.path.join(log_path, '%s_%s.log' % (project_name, os.getpid()))

        super(DefaultFileHandler, self).__init__(filename, when='midnight')
