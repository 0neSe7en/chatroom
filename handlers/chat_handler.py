import tornado.websocket
import logging
from room_manage import gRoomManager

class ChatHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        self.room = None
        super(ChatHandler, self).__init__(application, request, **kwargs)

    def open(self, roomname):
        username = self.get_secure_cookie("username")
        logging.info("[%s] is log in [%s] room" % (username, roomname))
        if not self.room:
            self.room = gRoomManager.get_room(roomname)
        self.room.user_in(username, self.callback)

    def callback(self, info):
        self.write_message(info)

    def on_close(self):
        username = self.get_secure_cookie('username')
        logging.info("%s is log out" % username)
        self.room.user_out(username)

    def on_message(self, message):
        username = str(self.get_secure_cookie("username"), encoding='utf-8')
        logging.info("[MESSAGE] [%s] Send [%s]" % (username, message))
        self.room.new_message(message, username)