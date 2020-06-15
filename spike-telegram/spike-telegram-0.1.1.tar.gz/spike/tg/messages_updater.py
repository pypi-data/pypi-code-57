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
from _thread import start_new_thread
from os.path import join
from os import devnull
from sys import stderr, prefix
from subprocess import run
from spike.common import textmessage, message
from spike.common import chat as cht
from spike.tg.telegram import Telegram
from spike.tg.utils import create_message_object
from spike.config.config import Config


class MessagesUpdater(Thread):

    def __init__(self, tui_chatlist, tui_dialog, users):
        super().__init__()
        self.tg = Telegram().get_instance()
        self.tui_chatlist = tui_chatlist
        self.tui_dialog = tui_dialog
        self.users = users
        self.chats = dict()
        self.tui_chatlist.set_chats(self.chats)
        self.fnull= open(devnull, "w")


    def _get_own_id(self):
        result = self.tg.get_me()
        result.wait()
        self.own_id = result.update["id"]


    def _request_error(self, result):
        print("Error while calling Telegram API:", result.error_info)
        exit(1)


    def _retrieve_chatlists(self):
        # https://github.com/alexander-akhmetov/python-telegram/issues/58
        result = self.tg.get_chats(offset_order=9223372036854775807)
        result.wait()

        if result.error:
            self._request_error(result)

        chat_ids = result.update["chat_ids"]
        for chat_id in chat_ids:
            # Add chat only if is not already in self.chats
            if not chat_id in [ch.chat_id for ch in self.chats.keys()]:
                result = self.tg.get_chat(chat_id)
                result.wait()
                if result.error:
                    self._request_error(result)

                chat = cht.Chat(chat_id)
                if result.update["notification_settings"]["mute_for"] != 0:
                    chat.notifications = False
                chat.unreaded = result.update["unread_count"]
                if len(result.update["title"]) > 0:
                    chat.name = result.update["title"]
                else:
                    chat.name = "Cuenta eliminada"

                self.chats[chat] = []
        self.tui_chatlist.reload()


    def _message_handler(self, update):
        msg = create_message_object(update["message"], self.users)

        # Message chat fetch
        # Retrieve chats again if is not in current chat list
        if not update["message"]["chat_id"] in [ch.chat_id for ch in self.chats.keys()]:
            self._retrieve_chatlists()
        chat = None
        for ch in self.chats.keys():
            if ch.chat_id == update["message"]["chat_id"]:
                chat = ch
                break
        if not chat:
            print("Could not find chat for chat ID:", update["message"]["chat_id"],
                    file=stderr)
            exit(1)

        self.chats[chat].append(msg)
        chat.unreaded += 1
        if self.tui_chatlist.curr_chat_index > -1:
            selected_chat = list(self.chats.keys())[self.tui_chatlist.curr_chat_index]
        else:
            selected_chat = None

        # Reload dialog if the message is from selected chat
        if chat == selected_chat and \
                self.tui_dialog.offset == 0:  # Do not reload if scrolled
            self.tui_dialog.reload()

        # Reload chatlist to update unseen messages
        self.tui_chatlist.reload()

        # Notification
        if Config.get_instance().get_sttg_notifications() and \
                chat.notifications and \
                (chat != selected_chat or self.tui_dialog.offset > 0 ) and \
                update["message"]["sender_user_id"] != self.own_id:
            if isinstance(msg, textmessage.TextMessage):
                text = msg.text
            else:
                text = "New message"
            run(["notify-send", "-a", "Spike", chat.name, text])

            if Config.get_instance().get_sttg_sound():
                start_new_thread(run,
                        (["aplay", join(prefix, "share/spike-telegram/plup.wav")],),
                        {"stderr": self.fnull})

    def run(self):
        self._get_own_id()
        self._retrieve_chatlists()
        self.tg.add_message_handler(self._message_handler)
