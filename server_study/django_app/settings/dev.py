# coding: utf-8
from .basic import *

ENV_MODE = 'dev'
DEBUG = True
WSGI_APPLICATION = 'settings.wsgi_dev.application'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'test',
        'USER': '',
        'PASSWORD': ''
    }
}
