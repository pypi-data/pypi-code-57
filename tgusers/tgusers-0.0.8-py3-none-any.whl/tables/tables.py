from .users import Users
from .messages import Messages
from tgusers.database.database import DataBase


class Tables:
    def __init__(self, db: DataBase):
        self.users      = Users("Users", db)
        self.messages   = Messages("Messages", db)