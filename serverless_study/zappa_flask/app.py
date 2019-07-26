# coding: utf-8

import time
from flask import Flask

myapp = Flask(__name__)


@myapp.route('/')
def hello():
    time.sleep(2)
    return 'hello,world'
