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


class SeenMarker(Thread):

    def __init__(self, chat, messages):
        super().__init__()
        self.chat = chat
        self.messages = messages
        self.tg = Telegram().get_instance()


    def run(self):
        params = {
            "chat_id": self.chat.chat_id,
            "message_ids": [m.id for m in self.messages],
            "force_read": True
        }
        self.tg.call_method("viewMessages", params=params)

        for m in self.messages:
            m.seen = True
        self.chat.unreaded -= len(self.messages)
        if (self.chat.unreaded < 0):
            self.chat.unreaded = 0

        SeenMarker.chatlist.reload()
