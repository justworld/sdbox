# coding: utf-8
from .basic import *

ENV_MODE = 'prod'
DEBUG = False
WSGI_APPLICATION = 'settings.wsgi.application'

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',

    }
}
