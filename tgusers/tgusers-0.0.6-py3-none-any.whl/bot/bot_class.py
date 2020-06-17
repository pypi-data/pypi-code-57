from time import time
from tgusers.tables.users import User
from tgusers.tables.tables import Tables
from tgusers.rooms.room_class import Rooms
from tgusers.tables.messages import Message
from aiogram import Bot, Dispatcher, executor, types

class TelegramBot:
    def __init__(self, api_key: str, tables: Tables, rooms: Rooms, message_logging: bool):
        self.bot = Bot(api_key)
        self.disp = Dispatcher(self.bot)
        self.rooms = rooms
        self.tables = tables

        @self.disp.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
        async def handler(message: types.Message):
            if not self.tables.users.check_user_for_registration(message):
                user = User(telegram_id=message.chat.id, first_name=message.chat.first_name,
                            last_name=message.chat.last_name, user_name=message.chat.username,
                            phone="", language=message.from_user.language_code, role="user",
                            room="start")
                user.id = self.tables.users.add(user).get("id")
            else:
                user = self.tables.users.get_user(message)
            if message_logging:
                log_message = Message(user_id=user.id, message=message.text, message_id=message.message_id, time=round(time()))
                self.tables.messages.add(log_message)
                print(message.chat.username, ":", message.chat.id, " -> ", message.text, "[", message.content_type, "]")
            for room_name in self.rooms.rooms:
                room = self.rooms.rooms[room_name]
                if room.message_handler and message.content_type in room.content_type and (room.name == user.room or room.is_global):
                    await room.function(message)

    def polling(self):
        executor.start_polling(self.disp, skip_updates=False)
