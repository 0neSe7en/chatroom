__author__ = '0neSe7en'
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.websocket
import json
import datetime
import logging

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
define("maxroom", default=100, help="max rooms", type=int)
define("maxuser", default=100, help="max users per room", type=int)
define("recordsize", default=500, help="max records per room", type=int)


class Room:
    def __init__(self, name):
        self.name = name
        self.user_list = list()
        self.records = []

    def user_in(self, username, callback):
        if not self.user_exist(username):
            self.user_list.append(User(username, callback))
            logging.debug('%s is added into user_list' % username)
            self.broadcast_user_status()

    def user_exist(self, username):
        for u in self.user_list:
            if username == u.name:
                return True
        return False

    def user_out(self, username):
        self._user_out(username)
        logging.debug('%s is removed from user_list' % username)
        self.broadcast_user_status()

    def _user_out(self, username):
        for u in self.user_list:
            if u.name == str(username):
                self.user_list.remove(u)
                return
        logging.error('%s is not found when user_out' % username)

    def new_message(self, message, username):
        self.records.append(Record(message, username, datetime.datetime.now()))
        self.broadcast_message()

    def broadcast_message(self):
        info = dict(type="message", info=None)
        logging.debug('message updating...')
        for u in self.user_list:
            info['info'] = [r.to_dict() for r in self.records[u.latest:]]
            u.callback(json.dumps(info))
            u.latest = len(self.records)-1

    def broadcast_user_status(self):
        u_dict = [dict(latest=u.latest, username=str(u.name)) for u in self.user_list]
        info = dict(type="user_status", info=u_dict)
        user_json = json.dumps(info)
        logging.debug('user status updating...')
        for u in self.user_list:
            u.callback(user_json)


class Record:
    def __init__(self, message, username, date):
        self.message = message
        self.username = username
        self.date = date

    def to_dict(self):
        return {
            'message' : str(self.message),
            'username': str(self.username),
            'date': str(self.date)
        }

class User:
    def __init__(self, name, callback):
        self.name = str(name)
        self.latest = 0
        self.callback = callback

groom = Room("chatroom-test")




class LoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('login.html', pos="登录")

    def post(self, *args, **kwargs):
        username = self.get_argument("username")
        if groom.user_exist(username):
            self.redirect('/login')
        self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect('/chat')


class ChatRoomHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("chat.html", username=self.get_secure_cookie("username"), pos="欢迎")


class ChatHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args, **kwargs):
        username = self.get_secure_cookie("username")
        logging.info("%s is log in" % username)
        groom.user_in(username, self.callback)

    def callback(self, info):
        self.write_message(info)

    def on_close(self):
        username = self.get_secure_cookie('username')
        logging.info("%s is log out" % username)
        groom.user_out(username)

    def on_message(self, message):
        username = self.get_secure_cookie("username")
        logging.info("[MESSAGE] [%s] Send [%s]" % (username, message))
        groom.new_message(message, username)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/login', LoginHandler),
            (r'/chat', ChatRoomHandler),
            (r'/chat/update', ChatHandler)
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