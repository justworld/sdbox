# coding: utf-8
from flask import Blueprint

hello_page = Blueprint('hello_world', __name__)
do_page = Blueprint('do_something', __name__)

# 注册配置: (blueprint, options)
BLUEPRINTS = [
    (hello_page, {'url_prefix': '/hello'}),
    (do_page, {'url_prefix': '/do'})
]
