# coding: utf-8
from django.conf.urls import include, url
from apps import api_router

# register
from apps.hello_world.apis import HelloViewSet

api_router.register(r'hello', HelloViewSet, basename='hello')

urlpatterns = [
    url(r'^api/', include(api_router.urls))
]
