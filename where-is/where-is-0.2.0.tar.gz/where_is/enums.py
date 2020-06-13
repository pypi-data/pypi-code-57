# where-is is a program/library that helps you find config files
# Copyright (C) 2020  ALinuxPerson
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
from typing import Union
from enum import Enum

class StructureType(Enum):
    PROPERTY: Union[str, Enum] = "property"
    MANIFEST: Union[str, Enum] = "manifest"

class FileSystemStructureType(Enum):
    FILE: Union[str, Enum] = "files"
    FOLDER: Union[str, Enum] = "folders"
    ALL: Union[str, Enum] = "all"

class Colors(Enum):
    ERROR: Union[str, Enum] = "✗: "
    WARNING: Union[str, Enum] = "⚠: "
    INFO: Union[str, Enum] = "🛈: "
    SUCCESS: Union[str, Enum] = "✓: "
    DEBUG: Union[str, Enum] = "🢡: "