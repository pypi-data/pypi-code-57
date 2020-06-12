# where-is is a program/library that helps you find config files
# Copyright (C) <year>  <name of author>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import List
import sys

class Arguments:
    def __init__(self, args: List[str] = None):
        self.args = args or sys.argv[1:]
        if not self.verified:
            pass

    @property
    def verified(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(args={self.args})"
