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
from spike.tui import tui

class ChatList:
    def __init__(self, window_size, dialog):
        lines, columns, start_y, start_x = window_size

        self.first_disp_index = 0
        self.sel_chat_index = 0
        self.curr_chat_index = -1
        # -4 => two for margins, one for "Chats" banner and one for separator
        self.n_displayed_chats = lines - 4
        self.writable_width = columns - 2

        self.window = cu.newwin(lines, columns, start_y, start_x)
        self.window.border()

        self.dialog = dialog


    def set_chats(self, chats):
        self.chats = chats


    def scroll_down(self):
        # If at bottom
        if self.sel_chat_index == len(self.chats) - 1:
            return

        if self.sel_chat_index == self.first_disp_index + \
                                self.n_displayed_chats - 1:
            self.first_disp_index += 1
        self.sel_chat_index += 1
        self.reload()


    def scroll_up(self):
        # If at top
        if self.sel_chat_index == 0:
            return

        if self.sel_chat_index == self.first_disp_index:
            self.first_disp_index -= 1
        self.sel_chat_index -= 1
        self.reload()


    def enter_chat(self):
        self.curr_chat_index = self.sel_chat_index
        sel_chat = list(self.chats.keys())[self.sel_chat_index]
        self.dialog.set_messages(sel_chat, self.chats[sel_chat])
        self.dialog.reload()


    def leave_chat(self):
        self.curr_chat_index = -1
        self.dialog.leave_dialog()


    def reload(self):
        self.window.erase()
        self.window.border()
        # "Chats" banner
        self.window.addstr(1, 1, "Chats")
        self.window.addstr(2, 0, "├" + "─"*self.writable_width + "┤")

        i = self.first_disp_index  # index for self.chats
        j = 3  # index for self.window lines
        while i < len(self.chats) and i < (self.first_disp_index + \
                                self.n_displayed_chats):
            name = list(self.chats.keys())[i].name
            unreaded = list(self.chats.keys())[i].unreaded

            if unreaded > 0:
                text = "{} ({})".format(name[:self.writable_width - \
                                    (len(str(unreaded))+3)], unreaded)
            else:
                text = name[:self.writable_width]

            bold = cu.A_BOLD if unreaded else 0

            if i == self.sel_chat_index:
                self.window.addstr(j, 1, text,
                            cu.color_pair(tui.Tui.COLOR_SEL_CHAT) | bold)
            else:
                self.window.addstr(j, 1, text, bold)
            i += 1
            j += 1
        self.window.noutrefresh()
        cu.doupdate()
