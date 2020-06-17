import tgusers

from dataclasses import dataclass


@dataclass
class Message:
    user_id: int
    message: str
    message_id: int
    time: int


class Messages(tgusers.Table):
    def add(self, message: Message):
        sql = """   INSERT INTO "Messages" (user_id, message, message_id, time)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id;
        """
        self.db.request(sql, (message.user_id, message.message, message.message_id, message.time))
        self.db.commit()
