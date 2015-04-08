import logging
import json
import datetime


class Room:
    def __init__(self, name):
        self.name = name
        self.user_list = []
        self.records = []

    def __str__(self):
        return "name:%s, %d users, %d records" % (self.name, len(self.user_list), len(self.records))

    def user_in(self, username, callback):
        logging.debug("user_list" % self.user_list)
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
        if self._user_out(username):
            if not len(self.user_list):
                return
            logging.debug('%s is removed from user_list' % username)
            self.broadcast_user_status()
        else:
            pass
            #Todo:if user out error, what to do?

    def _user_out(self, username):
        for u in self.user_list:
            if u.name == str(username, encoding='utf-8'):
                self.user_list.remove(u)
                return True
        logging.error('%s is not found when user_out' % username)
        return False

    def new_message(self, message, username):
        self.records.append(Record(message, username, datetime.datetime.now()))
        self.broadcast_message()

    def broadcast_message(self):
        info = dict(type="message", info=None)
        logging.debug('message updating...')
        for u in self.user_list:
            if len(self.records) > u.latest:
                info['info'] = [r.to_dict() for r in self.records[u.latest:]]
                u.callback(info)
                u.latest = len(self.records)

    def broadcast_user_status(self):
        u_dict = [dict(latest=u.latest, username=str(u.name)) for u in self.user_list]
        info = dict(type="user_status", info=u_dict)
        logging.debug('user status updating...')
        for u in self.user_list:
            u.callback(info)


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
        logging.debug("new user [%s]", name)
        self.name = str(name, encoding='utf-8')
        self.latest = 0
        self.callback = callback

    def __str__(self):
        return "name:%s" % self.name