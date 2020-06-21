#   qobra is a simple terminal music player
#   Contribute at alexander@alexandergoussas.com

#   Copyright (C) 2020  Alexander Goussas
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""This module contains functions to handle the program's options and events,
plus all the functions that interact with the player to control its behaviour,
but that do not necessarily belong inside the Player class.

Functions:
handle_input -- handles key events
get_opts -- manages program options
get_chunks -- yields n sized list chunks
draw_window -- draws the window
resize_window -- handles window resizing
"""

import os
import sys
import argparse
import signal
import curses

sys.path.insert(1, os.path.expanduser("~/.config/qobra/"))

try:
    from config import window_fg, window_bg, bg_char, border, music_dir
except ImportError:
    from qobra.config import (window_fg, window_bg, bg_char, border, music_dir)


def get_opts():
    """Manages program options

    Manages program options and returns the path to the
    music directory or exits with an error code if the
    program was called with no arguments and a music
    directory is not defined in ~/.config/qobra/config.py.
    """

    parser = argparse.ArgumentParser(
        description="Simple terminal music player")

    parser.add_argument("directory",
                        help="Your music directory",
                        nargs="?",
                        default=os.path.expanduser(music_dir))

    parser.add_argument("-s",
                        "--shuffle",
                        help="start qobra in shuffle mode",
                        action="store_true",
                        default=False)

    args = parser.parse_args()

    return args.directory, args.shuffle


def handle_input(stdscr, player, searchbox):
    """Handle key events

    Parameters:
    stdscr -- the screen object
    player -- the player object
    """

    curses.halfdelay(1)
    c = stdscr.getch()

    if c == ord("q"):
        sys.exit()
    elif c == curses.KEY_RESIZE:
        resize_window(stdscr, player, searchbox)
    elif c == ord("l"):
        player.play()
    elif c == ord("p"):
        player.pause()
    elif c == ord("k"):
        player.move_up()
    elif c == ord("i"):
        player.move_up()
        player.play()
    elif c == ord("j"):
        player.move_down()
    elif c == ord("o"):
        player.move_down()
        player.play()
    elif c == ord("t"):
        player.toggle_mode()
    elif c == ord("/"):
        searchbox.draw_search_box()


def draw_window(stdscr, colors):
    """Draws the program window"""

    curses.init_pair(3, colors[window_fg], colors[window_bg])
    stdscr.bkgd(bg_char, curses.color_pair(3))

    if border: stdscr.border()


def resize_window(stdscr, player, searchbox):
    """Resizes the window.

    Updates the player chunk size to fit in the
    new window height, and makes sure the current
    song stays selected.
    """

    player.window_height, player.window_width = stdscr.getmaxyx()
    player.update_chunk_size(player.window_height)
    player.chunk_index = [
        player.chunks.index(x) for x in player.chunks if player.curr_song in x
    ][0]
    player.curr_chunk = player.chunks[player.chunk_index]
    player.current = player.curr_chunk.index(player.curr_song)

    searchbox.width = stdscr.getmaxyx()[1] - 11
    searchbox.y = stdscr.getmaxyx()[0] - 2


def get_chunks(list, n):
    """Yield n sized chunks of list

    Parameters:
    list -- list object to be divided in chunks
    n -- integer with the number of chunks to create
    """
    for i in range(0, len(list), n):
        yield list[i:i + n]
