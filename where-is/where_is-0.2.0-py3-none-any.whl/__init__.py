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
from where_is import utils, __version__ as version
from typing import List, Type
from enum import Enum
import traceback
import platform
import sys

def error_handler(error_type: Type[Exception], exception: Exception, exception_traceback):
    os_name, _, os_release, os_version, arch, processor = tuple(platform.uname())
    utils.colored_output("An unhandled exception has been raised!\n\n", color=enums.Colors.ERROR)
    utils.colored_output("".join(traceback.format_tb(exception_traceback)), enums.Colors.ERROR)
    utils.colored_output(f"{error_type.__name__}: {exception}\n\n", color=enums.Colors.ERROR)
    utils.colored_output(f"System information: \n"
                         f"where-is version: {version.__version__}\n"
                         f"Python version: {platform.python_version()}\n"
                         f"OS Name: {os_name}\n"
                         f"OS Release: {os_release}\n"
                         f"OS Version: {os_version}\n"
                         f"CPU Architecture: {arch}\n"
                         f"Processor: {processor}", enums.Colors.ERROR)
    utils.colored_output(f"Please report this exception with the system information in the github issues page:\n"
                         f"https://github.com/what-to-code-complete/where-is/issues", enums.Colors.INFO)
    sys.exit(2)
sys.excepthook = error_handler  # type: ignore

from where_is import enums, structure

class WhereIs:
    def __init__(self, source: str, structure_type: Enum = enums.StructureType.MANIFEST):
        self.source = source
        self.structure_type = structure_type
        if self.structure_type == enums.StructureType.MANIFEST:
            self.manifests: structure.Manifests = structure.Manifests()
        else:
            self.property: structure.Property = structure.Property(self.source)

    @property
    def location(self) -> List[str]:
        if self.structure_type == enums.StructureType.MANIFEST:
            all_manifests: List[structure.Manifest] = self.manifests.manifests
            for manifest in all_manifests:
                if manifest.name == self.source:
                    return manifest.location
            else:
                return []
        else:
            ret: List[str] = []
            for manifest in self.property.inherits:
                ret.extend(manifest.location)

            return ret

    def __repr__(self):
        return f"{self.__class__.__name__}(source='{self.source}', structure_type={self.structure_type})"
