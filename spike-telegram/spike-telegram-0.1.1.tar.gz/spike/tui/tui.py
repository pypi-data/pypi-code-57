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
import locale
from sys import stderr
from spike.tui import chatlist
from spike.tui import dialog
from spike.tui import textbox
from spike.tui import userinput
from spike.common.chat import Chat  # For test
from spike.common.textmessage import TextMessage  # For test
from spike.tg.messages_updater import MessagesUpdater
from spike.tg.message_sender import MessageSender
from spike.tg.telegram import Telegram
from spike.tg.seen_marker import SeenMarker
from spike.tg.chat_history import ChatHistory
from spike.config.config import Config


class SmallTerminalError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Tui:
    # Color pairs codes
    COLOR_SEL_CHAT = 1
    COLOR_DEFAULT = 2
    COLOR_UNHANDLED_MSG = 3
    COLOR_HEADER_USER = 4
    COLOR_HEADER_TIME = 5
    COLOR_HEADER_DATE = 6
    COLOR_HEADER_ID_MSG = 7
    COLOR_HEADER_REPLY_TO = 8
    # Windows proportions and sizes
    MINIMUM_WIDTH = 87
    MINIMUM_HEIGHT = 12
    TOP_LINES_PADDING = 1
    HEIGHT_TEXTBOX = 6
    CHATLIST_WIDTH_PROP = 0.25  # 1/4 of terminal width

    def __init__(self):
        # Set locale to user default in all categories
        locale.setlocale(locale.LC_ALL, "")
        try:
            cu.wrapper(self.start)
        except SmallTerminalError as ex:
            print(ex, file=stderr)


    def set_defaults(self):
        # Color pairs
        cu.use_default_colors()
        cu.init_pair(Tui.COLOR_SEL_CHAT, cu.COLOR_BLACK, cu.COLOR_BLUE)
        cu.init_pair(Tui.COLOR_DEFAULT, -1, -1)
        cu.init_pair(Tui.COLOR_UNHANDLED_MSG, cu.COLOR_WHITE, cu.COLOR_RED)
        cu.init_pair(Tui.COLOR_HEADER_USER, cu.COLOR_GREEN, -1)
        cu.init_pair(Tui.COLOR_HEADER_TIME, cu.COLOR_CYAN, -1)
        cu.init_pair(Tui.COLOR_HEADER_DATE, cu.COLOR_BLUE, -1)
        cu.init_pair(Tui.COLOR_HEADER_ID_MSG, cu.COLOR_RED, -1)
        cu.init_pair(Tui.COLOR_HEADER_REPLY_TO, cu.COLOR_YELLOW, -1)

        cu.curs_set(False)  # Hide cursor
        self.stdscr.attrset(cu.color_pair(Tui.COLOR_DEFAULT))
        self.stdscr.erase()
        width_chatlist = Tui.get_size_window_chatlist()[1]
        self.stdscr.addstr(0, int(width_chatlist/2) - 7, "Spike Messenger", cu.A_BOLD)
        self.stdscr.refresh()
        self.dialog = dialog.Dialog(Tui.get_size_window_dialog())
        self.chat_list = chatlist.ChatList(Tui.get_size_window_chatlist(),
                                          self.dialog)
        SeenMarker.chatlist = self.chat_list
        self.textbox = textbox.TextBox(Tui.get_size_window_textbox())
        self.message_sender = MessageSender(self.textbox, self.chat_list)
        self.userinput = userinput.UserInput(self.stdscr, self, self.textbox,
                            self.chat_list, self.dialog, self.message_sender)

        users_dict = dict()  # Cache of User ID and usernames
        ChatHistory.users_dict = users_dict
        self.messages_updater = MessagesUpdater(self.chat_list, self.dialog,
                                                users_dict)

    def _check_terminal_dimensions(self):
        if cu.COLS < Tui.MINIMUM_WIDTH:
            raise SmallTerminalError("Terminal width below minimum")
        if cu.LINES < Tui.MINIMUM_HEIGHT:
            raise SmallTerminalError("Terminal height below minimum")


    def start(self, stdscr):
        self.stdscr = stdscr
        self._check_terminal_dimensions()
        self.set_defaults()
        self.messages_updater.start()
        if Config.get_instance().get_priv_online():
            Telegram().set_online()
        self.userinput.mainloop()
        del(self.stdscr)  # So cu.wrapper can close everything


    def resize_windows(self):
        cu.update_lines_cols()
        self._check_terminal_dimensions()
        self.stdscr.erase()

        # Program header
        width_chatlist = Tui.get_size_window_chatlist()[1]
        self.stdscr.addstr(0, int(width_chatlist/2) - 7, "Spike Messenger", cu.A_BOLD)
        self.stdscr.noutrefresh()
        cu.doupdate()

        # Chatlist resize
        lines, columns, y, x = Tui.get_size_window_chatlist()
        self.chat_list.window.resize(lines, columns)
        self.chat_list.window.mvwin(y, x)
        self.chat_list.n_displayed_chats = lines - 4
        self.chat_list.writable_width = columns - 2
        self.chat_list.reload()

        # Dialog resize
        lines, columns, y, x = Tui.get_size_window_dialog()
        self.dialog.window.resize(lines, columns)
        self.dialog.window.mvwin(y, x)
        self.dialog.lines = lines
        self.dialog.columns = columns
        self.dialog.available_width = columns - 2
        if self.chat_list.curr_chat_index > -1:
            self.dialog.reload()
        else:
            self.dialog.leave_dialog()

        # Textbox resize
        lines, columns, y, x = Tui.get_size_window_textbox()
        self.textbox.window.resize(lines, columns)
        self.textbox.window.mvwin(y, x)
        self.textbox.writtable_cols = columns - 2
        self.textbox.writtable_lines = lines - 2
        text = self.textbox.get_text()
        self.textbox.delete_text()
        for c in text:
            self.textbox.add_char(c)


    def get_size_window_chatlist():
        lines = cu.LINES - Tui.TOP_LINES_PADDING
        columns = int(cu.COLS * Tui.CHATLIST_WIDTH_PROP)
        start_y = Tui.TOP_LINES_PADDING
        start_x = 0

        return (lines, columns, start_y, start_x)


    def get_size_window_dialog():
        chatlist_columns = Tui.get_size_window_chatlist()[1]
        lines = cu.LINES - Tui.TOP_LINES_PADDING - Tui.HEIGHT_TEXTBOX
        columns = cu.COLS - chatlist_columns - 1  # 1: Marging bewtween windows
        start_y = Tui.TOP_LINES_PADDING
        start_x = chatlist_columns + 1  # 1: Marging bewtween windows

        return (lines, columns, start_y, start_x)


    def get_size_window_textbox():
        dia_l, dia_c, dia_y, dia_x = Tui.get_size_window_dialog()
        lines = Tui.HEIGHT_TEXTBOX
        columns = dia_c
        start_y = Tui.TOP_LINES_PADDING + dia_l
        start_x = dia_x

        return (lines, columns, start_y, start_x)
