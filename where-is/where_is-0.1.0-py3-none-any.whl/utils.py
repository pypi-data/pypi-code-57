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
from typing import Dict
import platform
import os

def config_location(os_platform: str = platform.system()) -> str:
    switch_case: Dict[str, str] = {
        "Linux": f"{os.environ['HOME']}/.config/where-is",
        "Windows": f"{os.getenv('LOCALAPPDATA')}/where-is",
        "Darwin": f"{os.environ['HOME']}/Library/Preferences/where-is"
    }

    return switch_case[os_platform]
