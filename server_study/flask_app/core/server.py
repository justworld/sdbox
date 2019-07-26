# coding: utf-8
from flask import Flask


def create_app(config_module):
    app = Flask(__name__)

    # load configuration
    app.config.from_object(config_module)

    # register blueprint
    import apps
    from config.blueprints import BLUEPRINTS
    for bluprint, options in BLUEPRINTS:
        app.register_blueprint(bluprint, **options)

    # middleware
    from .middleware import MIDDLEWARE_CHAIN
    wsgi_app = app.wsgi_app
    for md in MIDDLEWARE_CHAIN:
        wsgi_app = md(wsgi_app)
    app.wsgi_app = wsgi_app

    return app
