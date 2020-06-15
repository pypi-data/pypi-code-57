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

import curses as cu
from spike.tg.telegram import Telegram
from spike.config.config import Config

class UserInput:
    KEY_SCROLL_UP_CHATLIST = 259   # Arrow up
    KEY_SCROLL_DOWN_CHATLIST = 258 # Arrow down
    KEY_ENTER_CHAT = 261           # Arrow right
    KEY_LEAVE_CHAT = 260           # Arrow left
    KEY_SCROLL_UP_DIALOG = 339     # Page up
    KEY_SCROLL_DOWN_DIALOG = 338   # Page down
    KEY_EXIT = 17                  # Ctrl + q
    KEY_BACKSPACE = (127, 263)
    KEY_ENTER = 10

    def __init__(self, stdscr, tui, textbox, chatlist, dialog, message_sender):
        self.stdscr = stdscr
        self.tui = tui
        self.textbox = textbox
        self.chatlist = chatlist
        self.dialog = dialog
        self.message_sender = message_sender


    def mainloop(self):
        while True:
            # wch can be str or int types. key ternary ensures int type
            wch = self.stdscr.get_wch()
            key = wch if isinstance(wch, int) else ord(wch)

            if key == UserInput.KEY_SCROLL_UP_CHATLIST:
                self.chatlist.scroll_up()
            elif key == UserInput.KEY_SCROLL_DOWN_CHATLIST:
                self.chatlist.scroll_down()
            elif key == UserInput.KEY_ENTER_CHAT:
                self.chatlist.enter_chat()
            elif key == UserInput.KEY_LEAVE_CHAT:
                self.chatlist.leave_chat()
            elif key == UserInput.KEY_SCROLL_UP_DIALOG:
                self.dialog.scroll_up()
            elif key == UserInput.KEY_SCROLL_DOWN_DIALOG:
                self.dialog.scroll_down()
            elif key in UserInput.KEY_BACKSPACE:
                self.textbox.delete_last_char()
            elif key == UserInput.KEY_EXIT:
                break
            elif key == UserInput.KEY_ENTER:
                self.message_sender.start()
            elif key == cu.KEY_RESIZE:
                self.tui.resize_windows()
            else:
                self.textbox.add_char(wch)

        if Config.get_instance().get_priv_online():
            Telegram().set_offline()
