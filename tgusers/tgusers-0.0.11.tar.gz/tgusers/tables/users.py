import tgusers

from dataclasses import dataclass


@dataclass
class User:
    telegram_id: int
    user_name: str
    language: str
    role: str
    room: str
    id: int = -1


class Users(tgusers.Table):
    """
    CREATE TABLE public."Users"
        (
            id SERIAL PRIMARY KEY,
            "telegram_id" integer,
            "user_name" character varying(500),
            "language" character varying(500),
            "role" character varying(500),
            "room" character varying(500) DEFAULT 'start'
        )

        TABLESPACE pg_default;

        ALTER TABLE public."Users"
            OWNER to "Admin"

        CREATE INDEX telegram_id_index
        ON public."Users" USING btree
        (telegram_id ASC NULLS LAST)
        TABLESPACE pg_default;
    """
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

    def get_user(self, message=None, telegram_id: int = None):
        if message:
            telegram_id = message.chat.id
        sql = """
                    SELECT id, telegram_id, user_name, language, role, room
                    FROM "Users"
                    WHERE telegram_id = %s;
                """
        response = self.db.request(sql, (telegram_id,))[0]
        return User(**response)

    def get_user_role(self, message=None, telegram_id: int = None):
        if message:
            telegram_id = message.chat.id
        sql = """
                    SELECT role
                    FROM "Users"
                    WHERE telegram_id = %s;
                """
        return self.db.request(sql, (telegram_id, ))[0]["role"]


    def set_room(self, message=None, rooms: list = None, room_name: str = "", telegram_id: int = None):
        if rooms is None:
            rooms = []
        if message:
            telegram_id = message.chat.id
        for room in rooms:
            if room == room_name:
                sql = """   UPDATE "Users" 
                            SET room = %s
                            WHERE telegram_id = %s;"""
                self.db.request(sql, (room_name, telegram_id))
                self.db.commit()
                return True
        return False

    def add(self, user: User):
        sql = """   INSERT INTO "Users" (telegram_id, user_name, language, role, room)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
        """
        response = self.db.request(sql, (
            user.telegram_id, user.user_name, user.language,
            user.role, user.room))
        self.db.commit()
        return response

    def get_users_ids(self):
        sql =   """
                    SELECT telegram_id
                    FROM "Users";
                """
        return self.db.request(sql)
