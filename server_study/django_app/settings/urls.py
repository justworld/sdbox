# coding: utf-8
from django.conf.urls import include, url
from apps import api_router

urlpatterns = [
    url(r'^api/', include(api_router.urls))
]
