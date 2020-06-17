from random import randint
from dataclasses import dataclass
from tgusers.tables.tables import Tables
from tgusers.database.database import DataBase
"""
Room content type can be in range of ['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker']
"""


@dataclass
class Room:
    name: str
    content_type: list
    roles: list
    function: any
    is_global: bool = False
    message_handler: bool = False


class RoomsErrors(Exception):
    def __init__(self, message):
        self.message = message


class RoomsAlerts:
    @staticmethod
    def access_denied(get_alerts):
        if get_alerts:
            return [False, "Access denied"]
        else:
            return False

    @staticmethod
    def room_not_found(get_alerts):
        if get_alerts:
            return [False, "Room not found"]
        else:
            return False

    @staticmethod
    def successfully(get_alerts):
        if get_alerts:
            return [True, "Successfully"]
        else:
            return True


def valid_check(string: str):
    valid_chars = "abcdefghijklmnopqrstuvwxyz1234567890_-"
    for char in string:
        if char not in valid_chars:
            return False
    return True


class Rooms:
    def __init__(self, tables: Tables, db: DataBase, get_alerts: bool = False):
        self.db = db
        self.rooms = {}
        self.tables = tables
        self.get_alerts = get_alerts

    def add_message_room(self, name: str = None, content_type: list = None, roles: list = None,
                         is_global: bool = False):
        if roles is None:
            roles = ["all"]
        if content_type is None:
            content_type = []
        if name is None:
            name = str(randint(100000, 999999))
        if not valid_check(name):
            raise RoomsErrors("Invalid room name")


        def decorator(room_func):
            if is_global:
                room = Room(name=None, content_type=content_type, roles=roles, function=room_func, is_global=True,
                            message_handler=True)
                self.rooms[name] = room
            else:
                room = Room(name=name, content_type=content_type, roles=roles, function=room_func, is_global=False,
                            message_handler=True)
                self.rooms[name] = room

        return decorator


    def add_role(self, role: str, users: list):
        for user in users:
            if not self.tables.users.check_user_for_registration(telegram_id=user):
                users.pop(user)
        for user in users:
            self.tables.users.set_user_role(role, telegram_id=user)
        self.db.commit()


    def user_go_to_room(self, message, room_name: str):
        print(self.tables.users.get_user_role(message))
        if self.tables.users.get_user_role(message) in self.rooms.get(room_name).roles or "all" in self.rooms.get(
                room_name).roles:
            if self.tables.users.set_room(message, self.rooms.keys(), room_name):
                return RoomsAlerts.successfully(self.get_alerts)
            else:
                return RoomsAlerts.room_not_found(self.get_alerts)
        else:
            return RoomsAlerts.access_denied(self.get_alerts)

    def go_to_one_of_the_rooms(self, message, rooms_dict: dict):
        get_room = rooms_dict.get(message.text)
        if get_room:
            return self.user_go_to_room(message, get_room)
        else:
            return False

    def show_rooms(self):
        print(self.rooms)
