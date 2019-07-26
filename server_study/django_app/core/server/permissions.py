# coding: utf-8
from rest_framework.permissions import IsAuthenticated


class DefaultPermission(IsAuthenticated):
    """
    权限认证
    """

    def has_permission(self, request, view):
        username = getattr(request.user, 'username', None)
        if username == 'admin':
            return True

        return super(DefaultPermission, self).has_permission(request, view)
