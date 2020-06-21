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

import os
import sys
import curses
import random
import pygame.mixer as mixer

import qobra.functions as f

sys.path.insert(1, os.path.expanduser("~/.config/qobra/"))

try:
    from config import (
        underline,
        shuffle_mode_fg,
        shuffle_mode_bg,
        normal_mode_fg,
        normal_mode_bg,
        statusbar_song_fg,
        statusbar_song_bg,
        paused_fg,
        paused_bg,
        playing_fg,
        playing_bg,
        songs_fg,
        songs_bg,
        current_song_fg,
        current_song_bg,
    )
except ImportError:
    try:
        from qobra.config import (
            underline,
            shuffle_mode_fg,
            shuffle_mode_bg,
            normal_mode_fg,
            normal_mode_bg,
            statusbar_song_fg,
            statusbar_song_bg,
            paused_fg,
            paused_bg,
            playing_fg,
            playing_bg,
            songs_fg,
            songs_bg,
            current_song_fg,
            current_song_bg,
        )
    except ImportError:
        raise ImportError("Couldn't find path to config file")


class Player:
    """Manages state of the program.

    Attributes:
    path -- the path to the user's music directory
    current -- index of the curent song in the current chunk
    chunk_index -- index of the current chunk
    pid -- process id of the last run mpg123 process
    playing -- boolean indicating whether a song is playing or not
    mode -- string indicating the play mode (Shuffle or Normal)
    playing_song -- name of the last played song
    songs -- list with the songs in path
    chunks -- sublists of songs divided in window-sized chunks
    curr_chunk -- current chunk
    curr_song -- name of the last visited song
    """
    def __init__(self, path, shuffle, stdscr, colors):
        self.stdscr = stdscr
        self.colors = colors
        self.window_height, self.window_width = self.stdscr.getmaxyx()

        self.current = 0
        self.chunk_index = 0
        self.pid = None
        self.playing = False
        self.mode = "Normal" if not shuffle else "Shuffle"
        self.playing_song = ""

        self.songs = [song.strip("\n") for song in os.listdir(path)]
        self.paths = [os.path.join(path, song) for song in self.songs]
        self.chunks = list(f.get_chunks(self.songs, self.window_height - 3))
        self.curr_chunk = self.chunks[self.chunk_index]
        self.curr_song = self.curr_chunk[self.current]

    def display_songs(self):
        """Loads songs to the screen.

        Display the songs contained in the current chunk. It
        starts drawing them 1 line after the window start to
        compensate for the border. The current song is given
        different colors.
        """
        x, y = 2, 1

        curses.init_pair(1, self.colors[current_song_fg],
                         self.colors[current_song_bg])
        curses.init_pair(2, self.colors[songs_fg], self.colors[songs_bg])

        has_underline = curses.A_UNDERLINE if underline else 0

        for idx, song in enumerate(self.curr_chunk):
            free_space = self.window_width - len(song) - 1 - x
            if idx == self.current:
                self.stdscr.addnstr(y, x, song + " " * free_space,
                                    self.window_width - 5,
                                    curses.color_pair(1))
            else:
                if idx < self.window_height:
                    self.stdscr.addnstr(
                        y,
                        x,
                        song + " " * free_space,
                        self.window_width - 5,
                        curses.color_pair(2) | has_underline,
                    )
            y += 1

    def statusbar(self):
        """Draw the statusbar at the bottom of the screen

        Display information about the current playing song,
        the playing status and the playing mode. It is drawn
        2 lines above the window bottom to compensate for the
        border.
        """
        y = self.window_height - 2

        curses.init_pair(4, self.colors[playing_fg], self.colors[playing_bg])
        curses.init_pair(5, self.colors[paused_fg], self.colors[paused_bg])
        curses.init_pair(6, self.colors[statusbar_song_fg],
                         self.colors[statusbar_song_bg])
        curses.init_pair(7, self.colors[normal_mode_fg],
                         self.colors[normal_mode_bg])
        curses.init_pair(8, self.colors[shuffle_mode_fg],
                         self.colors[shuffle_mode_bg])

        self.stdscr.addstr(
            y,
            2,
            "Playing" if self.playing else "Paused",
            curses.color_pair(4 if self.playing else 5) | curses.A_BOLD,
        )

        self.stdscr.addnstr(y, 10, self.playing_song, self.window_width - 20,
                            curses.color_pair(6) | curses.A_BOLD)

        self.stdscr.addstr(
            y,
            self.window_width - len(self.mode) - 1,
            self.mode,
            curses.color_pair(7 if self.mode == "Normal" else 8)
            | curses.A_BOLD,
        )

    def update_chunk_size(self, new_height):
        """Updates the chunk size on window resize

        Parameters:
        new_height -- the new height of the window
        """
        self.chunks = list(f.get_chunks(self.songs, new_height - 3))

    def update(self):
        """Play next song after current one ends

        Checks is self.playing is True and the mixer channel is not
        busy.
        """
        if self.playing and not self._channel.get_busy():
            if self.curr_song == self.songs[-1]:
                self.playing = False
            elif self.current < len(self.curr_chunk) - 1:
                self.current += 1
                self.play()
            elif self.chunk_index < len(self.chunks) - 1:
                self.current = 0
                self.chunk_index += 1
                self.curr_chunk = self.chunks[self.chunk_index]
                self.play()

    def play(self):
        """Plays current song

        Plays a song. Stop the mixer first to make sure no duplicate
        processes are running.
        """
        mixer.stop()
        if self.mode == "Shuffle":
            self.curr_song = self.shuffle()
        else:
            self.curr_song = self.curr_chunk[self.current]

        song_index = self.songs.index(self.curr_song)

        song = mixer.Sound(self.paths[song_index])
        self._channel = song.play()

        self.playing_song = self.curr_song
        self.playing = True

    def shuffle(self):
        """Set a random song to be the current one"""

        chosen_song = random.choice(self.songs)
        for x, chunk in enumerate(self.chunks):
            for y, song in enumerate(chunk):
                if song == chosen_song:
                    self.chunk_index = x
                    self.curr_chunk = self.chunks[self.chunk_index]
                    self.current = y

        return chosen_song

    def toggle_mode(self):
        """Toggles between Normal and Shuffle mode."""

        self.mode = "Normal" if self.mode == "Shuffle" else "Shuffle"

    def pause(self):
        """Toggles state of the player

        Pauses the mixer is self.playing is True, else unpauses it.
        """
        if self.playing:
            mixer.pause()
            self.playing = False
        else:
            mixer.unpause()
            self.playing = True

    def move_down(self):
        """Moves down a song.

        If the song is the last one in the current chunk,
        moves, to the first song in the next chunk, else
        it just moves to the next song.
        """

        if self.current < len(self.curr_chunk) - 1:
            self.current += 1
            self.curr_song = self.curr_chunk[self.current]
        elif self.chunk_index < len(self.chunks) - 1:
            self.current = 0
            self.chunk_index += 1
            self.curr_chunk = self.chunks[self.chunk_index]
            self.curr_song = self.curr_chunk[self.current]

    def move_up(self):
        """Moves up a song

        If the song is the current song is the first one
        in the current chunk, move to the last song in the
        previous chunk, else just move back a song.
        """

        if self.current > 0:
            self.current -= 1
            self.curr_song = self.curr_chunk[self.current]
        elif self.chunk_index != 0:
            self.chunk_index -= 1
            self.curr_chunk = self.chunks[self.chunk_index]
            self.current = len(self.curr_chunk) - 1
