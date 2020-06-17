import tgusers

from dataclasses import dataclass


@dataclass
class User:
    telegram_id: int
    first_name: str
    last_name: str
    user_name: str
    phone: str
    language: str
    role: str
    room: str
    id: int = -1


class Users(tgusers.Table):
    def get_user_room(self, message):
        sql = """
                    SELECT room
                    FROM "Users"
                    WHERE telegram_id = %s;
        """
        return self.db.request(sql, (message.chat.id,))[0].get("room")

    def check_user_for_registration(self, message=None, telegram_id: int = None):
        if message:
            telegram_id = message.chat.id
        sql = """
                    SELECT id
                    FROM "Users"
                    WHERE telegram_id = %s;
                """
        if self.db.request(sql, (telegram_id, )):
            return True
        else:
            return False

    def set_user_role(self, role_name: str, message=None, telegram_id: int = None):
        if message:
            telegram_id = message.chat.id
        sql = """   UPDATE "Users" 
                    SET role = %s
                    WHERE telegram_id = %s;"""
        self.db.request(sql, (role_name, telegram_id))

    def get_user(self, message):
        sql = """
                    SELECT id, telegram_id, first_name, last_name, user_name, phone, language, role, room
                    FROM "Users"
                    WHERE telegram_id = %s;
                """
        response = self.db.request(sql, (message.chat.id,))[0]
        return User(**response)

    def get_user_role(self, message):
        sql = """
                    SELECT role
                    FROM "Users"
                    WHERE telegram_id = %s;
                """
        return self.db.request(sql, (message.chat.id, ))[0]["role"]


    def set_room(self, message, rooms: list, room_name: str):
        for room in rooms:
            if room == room_name:
                sql = """   UPDATE "Users" 
                            SET room = %s
                            WHERE telegram_id = %s;"""
                self.db.request(sql, (room_name, message.chat.id))
                self.db.commit()
                return True
        return False

    def add(self, user: User):
        sql = """   INSERT INTO "Users" (telegram_id, first_name, last_name, user_name, phone, language, role, room)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
        """
        response = self.db.request(sql, (
            user.telegram_id, user.first_name, user.last_name, user.user_name, user.phone, user.language,
            user.role, user.room))
        self.db.commit()
        return response
