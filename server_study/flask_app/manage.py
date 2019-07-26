# coding: utf-8

# gevent patch
from gevent import monkey

monkey.patch_all()

from core.server import create_app

app = create_app('config.prod')
