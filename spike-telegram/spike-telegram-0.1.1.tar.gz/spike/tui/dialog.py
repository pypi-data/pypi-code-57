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

import time
import curses as cu
from textwrap import wrap
from spike.tui import tui
from spike.common.textmessage import TextMessage
from spike.tg.seen_marker import SeenMarker
from spike.tg.chat_history import ChatHistory
from spike.config.config import Config

class Dialog:
    TEXT_MSG_PADDING = 2

    def __init__(self, window_size):
        lines, columns, start_y, start_x = window_size

        self.lines = lines
        self.available_width = columns - 2  # 2 of sides borders
        self.offset = 0
        self.reached_chat_start = False

        self.columns = columns
        self.window = cu.newwin(lines, columns, start_y, start_x)
        self.window.border()
        self.window.noutrefresh()
        cu.doupdate()


    def set_messages(self, chat, messages):
        self.offset = 0
        self.reached_chat_start = False
        self.messages = messages
        self.chat = chat


    def _display_text_message(self, msg):
        msg_lines = wrap(msg.text, self.available_width - \
                         Dialog.TEXT_MSG_PADDING)
        i = len(msg_lines) - 1
        while i >= 0 and self.available_lines > 0:
            # Check for empty lines
            if msg_lines[i][0] == "\n":
                self.available_lines -= 1
                msg_lines[i] = msg_lines[i].lstrip()


            self.window.addstr(self.available_lines, 1 +
                               Dialog.TEXT_MSG_PADDING, msg_lines[i])
            i -= 1
            self.available_lines -= 1


    def _display_header(self, msg):
        if self.available_lines > 0:
            sender = msg.sender[:self.available_width - 60]
            msg_time = time.strftime("%H:%M:%S", time.localtime(msg.epoch))
            msg_date = time.strftime("%d-%m-%Y", time.localtime(msg.epoch))
            id_hex = "ID:{}".format(format(msg.id, "X"))
            reply_to = "Reply:{}".format(format(msg.reply_to, "X"))

            offset = 1
            # Sender
            self.window.addstr(self.available_lines, offset, sender,
                                cu.color_pair(tui.Tui.COLOR_HEADER_USER))
            offset += len(sender) + 1
            # Time
            self.window.addstr(self.available_lines, offset, msg_time,
                                cu.color_pair(tui.Tui.COLOR_HEADER_TIME))
            offset += len(msg_time) + 1
            # Date
            self.window.addstr(self.available_lines, offset, msg_date,
                                cu.color_pair(tui.Tui.COLOR_HEADER_DATE))
            offset += len(msg_date) + 1
            # ID message
            self.window.addstr(self.available_lines, offset, id_hex,
                                cu.color_pair(tui.Tui.COLOR_HEADER_ID_MSG))
            offset += len(id_hex) + 1
            # Reply to
            if reply_to != "Reply:0":
                self.window.addstr(self.available_lines, offset, reply_to,
                                    cu.color_pair(tui.Tui.COLOR_HEADER_REPLY_TO))

            self.available_lines -= 1


    def _write_chat_name(self):
        name = "╼ " + self.chat.name[:self.columns - 6] + " ╾"
        half_len_name = int(len(name) / 2)
        half_columns = int(self.columns / 2)
        self.window.addstr(0, half_columns - half_len_name, name)


    def scroll_up(self):
        if self.offset < len(self.messages):
            self.offset += 1
            self.reload()
        elif not self.reached_chat_start:
            last_id = self.messages[0].id
            ChatHistory(self.chat.chat_id, self, last_id).retrieve()


    def scroll_down(self):
        if self.offset > 0:
            self.offset -= 1
            self.reload()


    def leave_dialog(self):
        self.offset = 0
        self.reached_chat_start = False
        self.messages = None
        self.chat = None

        self.window.erase()
        self.window.border()
        self.window.noutrefresh()
        cu.doupdate()


    def reload(self):
        self.window.erase()
        self.window.border()
        self._write_chat_name()

        if len(self.messages) == 0:
            if self.reached_chat_start:  # Clear and leave
                self.window.noutrefresh()
                cu.doupdate()
                return
            else:
                ChatHistory(self.chat.chat_id, self).retrieve()
        # If the number of preloaded messages is low and chat start not reached
        elif len(self.messages) < ChatHistory.NUMBER_MESSAGES_TO_RETRIEVE and \
                not self.reached_chat_start:
            ChatHistory(self.chat.chat_id, self, self.messages[0].id).retrieve()

        unreaded_messages = []
        self.available_lines = self.lines - 2  # 2: top and bottom borders
        i = len(self.messages) - 1 - self.offset
        while i >= 0 and self.available_lines > 0:
            msg = self.messages[i]

            # Check if is an unread message
            if not msg.seen:
                unreaded_messages.append(msg)

            # Classification of type of message
            if isinstance(msg, TextMessage):
                self._display_text_message(msg)
            elif self.available_lines > 0:
                self.window.addstr(self.available_lines, 1,
                                ">> Unhandled message type <<",
                                cu.color_pair(tui.Tui.COLOR_UNHANDLED_MSG) |
                                cu.A_BOLD)
                self.available_lines -= 1

            # Header printing
            self._display_header(msg)

            i -= 1
        self.window.noutrefresh()
        cu.doupdate()

        if Config.get_instance().get_priv_mark_as_seen():
            SeenMarker(self.chat, unreaded_messages).start()
