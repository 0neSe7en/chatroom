import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
from handlers.render_handlers import LoginHandler, ChatRoomHandler
from handlers.chat_handler import ChatHandler
from models.models import *

define("port", default=8000, help="run on the given port", type=int)
define("maxroom", default=100, help="max rooms", type=int)
define("maxuser", default=100, help="max users per room", type=int)
define("recordsize", default=500, help="max records per room", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/login', LoginHandler),
            (r'/chat/(\w+)/update', ChatHandler),
            (r'/chat/(\w+)', ChatRoomHandler)
        ]
        settings = {
            'template_path': 'templates',
            'static_path': 'static',
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "xsrf_cookies": True,
            "login_url": "/login",
            "debug": True
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()