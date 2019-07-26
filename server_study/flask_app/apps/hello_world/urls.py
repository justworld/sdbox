# coding: utf-8
from flask_restful import Api

from config.blueprints import hello_page
from apps.hello_world.apis import Index

api = Api(hello_page)

# 注册路由
api.add_resource(Index, '/index')
