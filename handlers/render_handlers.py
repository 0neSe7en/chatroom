import tornado.web
import logging

from .base_handler import BaseHandler
from models.models import *
from room_manage import gRoomManager

class LoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('login.html', pos="登录")

    def post(self, *args, **kwargs):
        username = self.get_argument("username")
        roomname = self.get_argument("roomname")
        logging.info("Username=%s, roomname=%s" % (username, roomname))
        room = gRoomManager.get_room(roomname)
        if not room:
            self.set_secure_cookie("username", self.get_argument("username"))
            gRoomManager.create_room(roomname)
        self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect('/chat/%s' % roomname)


class ChatRoomHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, roomname):
        logging.info("someone in the %s" % roomname)
        self.render("chat.html", username=self.get_secure_cookie("username"), pos="欢迎", roomname=roomname)