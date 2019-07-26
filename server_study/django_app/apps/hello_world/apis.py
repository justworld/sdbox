# coding: utf-8
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet


class HelloViewSet(GenericViewSet):

    @action(methods=["GET"], detail=False)
    def index(self, request, **kwargs):
        return Response('hello, {}'.format(settings.PROJECT_NAME))
