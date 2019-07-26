# coding: utf-8
from rest_framework.views import exception_handler

from utils.log_util import log_msg


def api_exception_handler(exc, context):
    """
    API通用异常处理
    """
    # 添加处理逻辑
    return exception_handler(exc, context)


def other_exception_handler(e, event, context):
    """
    未处理异常处理
    :param e:
    :param event:
    :param context:
    :return:
    """
    log_msg('{}, {}, {}'.format(e, event, context))
