import tgusers

from dataclasses import dataclass


@dataclass
class Message:
    user_id: int
    message: str
    message_id: int
    time: int


class Messages(tgusers.Table):
    """ CREATE TABLE public."Messages"
            (
                id SERIAL PRIMARY KEY,
                "user_id" integer,
                "message" character varying(1040),
                "message_id" integer,
                "time" integer
            )

            TABLESPACE pg_default;

            ALTER TABLE public."Messages"
                OWNER to "Admin";
            """
    def add(self, message: Message):
        sql = """   INSERT INTO "Messages" (user_id, message, message_id, time)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id;
        """
        self.db.request(sql, (message.user_id, message.message, message.message_id, message.time))
        self.db.commit()
