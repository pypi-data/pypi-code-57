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
from where_is import enums
from enum import Enum

class WhereIs:
    def __init__(self, source: str,
                 structure_type: Enum = enums.StructureType.MANIFEST,
                 file_system_structure_type: Enum = enums.FileSystemStructureType.ALL
                 ):
        self.source = source
        self.structure_type = structure_type
        self.fs_struct_type = file_system_structure_type

    def __repr__(self):
        return f"{self.__class__.__name__}(source='{self.source}', structure_type={self.structure_type}," \
               f" file_system_structure_type={self.fs_struct_type})"
