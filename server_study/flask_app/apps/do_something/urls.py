# coding: utf-8
from flask_restful import Api

from config.blueprints import do_page
from apps.do_something.apis import Index

api = Api(do_page)

# 注册路由
api.add_resource(Index, '/')
