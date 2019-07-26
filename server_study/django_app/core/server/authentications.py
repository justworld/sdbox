# coding: utf-8
from rest_framework import authentication


class DefaultAuthentication(authentication.BaseAuthentication):
    u"""
    API认证
    """

    def authenticate(self, request):
        """
        编写校验逻辑
        :param request:
        :return:
        """
        user = request.GET.get('user')
        # 返回用户
        if user:
            return (DemoUser(user), self)

        return None


class DemoUser:
    def __init__(self, username):
        self.is_authenticated = False
        self.username = username
