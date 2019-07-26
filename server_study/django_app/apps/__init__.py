# coding: utf-8
from rest_framework.routers import SimpleRouter

from apps.hello_world.apis import HelloViewSet

api_router = SimpleRouter()

# register
api_router.register(r'hello', HelloViewSet, basename='hello')
