# Copyright (C) 2020 Esteban López Rodríguez <gnu_stallman@protonmail.ch>
#
# This file is part of Spike.
#
# Spike is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Spike is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from threading import Thread
from spike.tg.telegram import Telegram


class MessageSender(Thread):

    def __init__(self, tui_textbox, tui_chatlist):
        super().__init__()
        self.tg = Telegram().get_instance()
        self.tui_textbox = tui_textbox
        self.tui_chatlist = tui_chatlist


    def run(self):
        if self.tui_chatlist.curr_chat_index > -1:
            chat = list(self.tui_chatlist.chats.keys())[self.tui_chatlist.curr_chat_index]
            chat_id = chat.chat_id

            text = self.tui_textbox.get_text()
            self.tui_textbox.delete_text()

            self.tg.send_message(chat_id=chat_id, text=text)
        super().__init__()  # To allow restarting the thread multiple times
