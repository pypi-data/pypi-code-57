from tgusers.bot.bot_class import TelegramBot
from tgusers.database.database import DataBase, PostgresAuthData
from .rooms.room_class import Rooms, Room
from .tables.tables import Tables


class Connect:
    def __init__(self, bot_token: str, pgData: PostgresAuthData, message_logging: bool = False):
        self.data_base    = DataBase(pgData)
        self.tables       = Tables(self.data_base)
        self.rooms        = Rooms(self.tables)
        self.telegram_bot = TelegramBot(bot_token, self.tables, self.rooms, message_logging)

