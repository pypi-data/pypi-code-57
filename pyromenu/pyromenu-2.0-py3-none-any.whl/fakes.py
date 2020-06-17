"""
MIT License

Copyright (c) 2020 LidaRandom

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from typing import List

from pyrogram import KeyboardButton, Filters
from pyrogram.client.filters.filter import Filter

from .abc import Button, Row


class FakeButton(Button):
    def __hash__(self) -> int:
        return hash("fake button")

    def __eq__(self, other_button: Button) -> bool:
        return hash(self) == hash(other_button)

    @property
    def keyboard_button(self) -> KeyboardButton:
        return KeyboardButton("fake button")

    @property
    def update_filter(self) -> Filter:
        return Filters.create(func=lambda flt, msg: msg.text == "fake button")


class FakeRow(Row):
    @property
    def keyboard_row(self) -> List[KeyboardButton]:
        return [KeyboardButton("fake button"), KeyboardButton("fake button")]

    @property
    def buttons(self) -> List[Button]:
        return [FakeButton(), FakeButton()]


__all__ = ["FakeButton", "FakeRow"]
