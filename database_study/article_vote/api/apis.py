# coding=utf-8
import json
import tornado.ioloop
import tornado.web


class Base(tornado.web.RequestHandler):
    pass


# helloworld
class Hello(Base):
    def post(self):
        self.finish({'msg': 'hello,world'})


def make_app():
    return tornado.web.Application([
        (r'/hello', Hello)
    ])


def run():
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    run()