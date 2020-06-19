from time import time
from tgusers.tables.users import User
from tgusers.tables.tables import Tables
from tgusers.tables.messages import Message
from aiogram import Bot, Dispatcher, executor, types


class TelegramBot:
    def __init__(self, api_key: str, tables: Tables, rooms: list, message_logging: bool, antispam: bool = False):
        self.bot = Bot(api_key)
        self.disp = Dispatcher(self.bot)
        self.rooms = rooms
        self.tables = tables
        self.antispam = antispam
        self.spam_filter = {}
        self.max_messages_in_minute = 15
        self.last_list_update = time()

        @self.disp.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
        async def message_handler(message: types.Message):
            if self.antispam:
                if time() - self.last_list_update > 60:
                    self.spam_filter = {}
                    self.last_list_update = time()
                if not self.spam_filter.get(message.chat.id):
                    self.spam_filter[message.chat.id] = 1
                else:
                    self.spam_filter[message.chat.id] += 1
                if self.spam_filter.get(message.chat.id) > self.max_messages_in_minute:
                    await message.answer("Slower, slower. Not spam please.")
                    return

            if not self.tables.users.check_user_for_registration(message):
                user = User(telegram_id=message.chat.id, user_name=message.chat.username,
                            language=message.from_user.language_code, role="user",
                            room="start")
                user.id = self.tables.users.add(user).get("id")
            else:
                user = self.tables.users.get_user(message)
            if message_logging:
                log_message = Message(user_id=user.id, message=message.text, message_id=message.message_id, time=round(time()))
                self.tables.messages.add(log_message)
                print(message.chat.username, ":", message.chat.id, " -> ", message.text, "[", message.content_type, "]")
            for room in self.rooms:
                if room.message_handler and message.content_type in room.content_type and (room.name == user.room or room.is_global):
                    await room.function(message)

        @self.disp.callback_query_handler()
        async def callback_query_handler(call: types.CallbackQuery):
            if not self.tables.users.check_user_for_registration(telegram_id=call.from_user.id):
                user = User(telegram_id=call.from_user.id, user_name=call.from_user.username,
                            language=call.from_user.language_code, role="user",
                            room="start")
                user.id = self.tables.users.add(user).get("id")
            else:
                user = self.tables.users.get_user(telegram_id=call.from_user.id)
            if message_logging:
                print("[ CALLBACK ]" + call.from_user.username, ":", call.from_user.id, " -> ", call.data)
            for room in self.rooms:
                if room.callback_query_handler and (room.name == user.room or room.is_global):
                    await room.function(call)

    def polling(self):
        executor.start_polling(self.disp, skip_updates=False)
