import logging
from models.models import *


class RoomManager:
    def __init__(self):
        self.room_list = dict()

    def create_room(self, roomname):
        if roomname in self.room_list:
            return None
        room = Room(roomname)
        self.room_list[roomname] = room
        logging.info("A room created [%s]" % room)
        return room

    def remove_room(self, room):
        return True if self.room_list.pop(room.name) else False

    def get_room(self, name):
        return self.room_list.get(name)

gRoomManager = RoomManager()