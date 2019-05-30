from django.conf.urls import url
from django.contrib import admin
from views import hello_get, hello_post

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello/hget/', hello_get),
    url(r'^hello/hpost/', hello_post),
]
