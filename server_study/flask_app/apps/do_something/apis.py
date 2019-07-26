# coding: utf-8
from flask import current_app, request
from flask_restful import Resource


class Index(Resource):
    def get(self):
        return 'hello, {}'.format(current_app.config.get('PROJECT_NAME'))

    def post(self):
        data = request.get_json()
        return 'request data is {}'.format(data)
