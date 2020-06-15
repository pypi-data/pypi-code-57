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

from spike.tg.telegram import Telegram
from spike.tg.utils import create_message_object

class ChatHistory:

    NUMBER_MESSAGES_TO_RETRIEVE = 30

    def __init__(self, chat_id, tui_dialog, from_msg_id=0):
        self.chat_id = chat_id
        self.tui_dialog = tui_dialog
        self.from_msg_id = from_msg_id
        self.tg = Telegram().get_instance()


    def retrieve(self):
        left = ChatHistory.NUMBER_MESSAGES_TO_RETRIEVE
        raw_messages = []

        while left > 0:
            result = self.tg.get_chat_history(self.chat_id, left, self.from_msg_id)
            result.wait()

            if result.update["total_count"] == 0:
                self.tui_dialog.reached_chat_start = True
                break

            self.from_msg_id = result.update["messages"][-1]["id"]
            left -= result.update["total_count"]

            raw_messages.extend(result.update["messages"])

        for raw_msg in raw_messages:
            msg = create_message_object(raw_msg, ChatHistory.users_dict)
            self.tui_dialog.messages.insert(0, msg)
