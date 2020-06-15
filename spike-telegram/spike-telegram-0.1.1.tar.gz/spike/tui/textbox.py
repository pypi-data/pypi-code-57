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
from spike.config.config import Config
if Config.get_instance().get_emoji_convert_codes():
    import emoji

class TextBox:
    def __init__(self, window_size):
        lines, columns, start_y, start_x = window_size

        self.window = cu.newwin(lines, columns, start_y, start_x)
        self.window.scrollok(True)
        self.window.border()
        self.window.noutrefresh()
        cu.doupdate()

        self.cursor_x = self.cursor_y = 1
        # -2 because of borders
        self.writtable_cols = columns - 2
        self.writtable_lines = lines - 2
        self.scrolled_lines = 0
        self.text = []


    def _scroll_forward(self):
        self.window.scroll()
        self.window.move(self.cursor_y, 1)
        self.window.clrtoeol()  # Clear scrolled bottom border
        self.window.border()
        self.window.addch(0, self.writtable_cols+1, "↑")
        self.scrolled_lines += 1


    def _scroll_backwards(self):
        self.window.addstr(1, 1, "".join(self.text[-self.writtable_cols:]))
        self.cursor_y = 1
        self.cursor_x = self.writtable_cols
        self.scrolled_lines -= 1
        if self.scrolled_lines == 0:
            self.window.border()  # Delete arrow

    def add_char(self, ch):
        if self.cursor_x - 1>= self.writtable_cols:
            self.cursor_x = 1
            if self.cursor_y < self.writtable_lines:
                self.cursor_y += 1
            else:
                self._scroll_forward()
        self.window.addch(self.cursor_y, self.cursor_x, ch)
        self.cursor_x += 1
        self.window.noutrefresh()
        cu.doupdate()
        self.text.append(ch)


    def delete_last_char(self):
        # Do nothing if textbox is empty
        if self.scrolled_lines == 0 and self.cursor_x == 1 and self.cursor_y == 1:
            return
        # Jump to previous line if at the beggining of the line
        if self.cursor_x == 1:
            self.cursor_y -= 1
            self.cursor_x = self.writtable_cols + 1
        self.cursor_x -= 1
        self.window.addch(self.cursor_y, self.cursor_x, " ")
        self.text.pop()
        # Scroll backwards if there are hidden lines
        if self.scrolled_lines > 0 and self.cursor_x == 1 and self.cursor_y ==1:
            self._scroll_backwards()
            self.cursor_x += 1
        self.window.noutrefresh()
        cu.doupdate()


    def delete_text(self):
        self.window.erase()
        self.window.border()
        self.window.noutrefresh()
        cu.doupdate()
        self.cursor_x = self.cursor_y = 1
        self.scrolled_lines = 0
        self.text.clear()


    def get_text(self):
        if Config.get_instance().get_emoji_convert_codes():
            return emoji.emojize("".join(self.text))
        else:
            return "".join(self.text)
