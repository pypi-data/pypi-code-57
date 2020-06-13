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
from where_is import structure, exceptions, enums, utils, __version__ as version
from typing import List, Dict, Union
import sys

class ParsedArguments:
    def __init__(self,
                 struct_type: Union[enums.StructureType, str],
                 name: str,
                 data_type: Union[enums.FileSystemStructureType, str]
                 ):
        self.struct_type = struct_type
        self.name = name
        self.data_type = data_type
        self.manifests = structure.Manifests()
        self.shell_args: str = f"where-is {self.struct_type.value} {self.name} {self.data_type.value}"  # type: ignore
        self.verify()

    def verify(self):
        if not sys.argv[1:]:
            self.print_help()
        if self.struct_type not in ("property", "manifest"):
            self.error(f"'{self.struct_type}' is not a structure type!\n"
                       f"Choose from property or manifest")
        if self.name not in [manifest.name for manifest in self.manifests.manifests]:
            pass

    @staticmethod
    def print_help():
        utils.colored_output(f"""where-is version {version.__version__}
        
A program that helps you find config files (inspired by what-to-code)

Usage:
    where-is <structure-type: property, manifest> <name> <files, folders, all>
Usage Examples:
    where-is property shell files
    where-is manifest shell
    where-is bash folders
    where-is zsh""", enums.Colors.INFO)

    def _mistake_gen(self, mistake: str = "all") -> str:
        switch_case: Dict[str, int] = {
            "all": 0,
            "struct_type": 1,
            "name": 2,
            "data_type": 3
        }

        token: List[str] = self.shell_args.split()
        token.insert(switch_case[mistake] - 1 if switch_case[mistake] > 0 else 0, " >>>")
        token.insert(switch_case[mistake] + 1 if switch_case[mistake] > 0 else -1, "<<< ")

        return " ".join(token)

    def error(self, message: str, mistake: str = "all"):
        utils.colored_output(f"Argument error!\n"
                             f"The mistake (shell output is generated): {self._mistake_gen(mistake)}"
                             f"{message}", enums.Colors.ERROR)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(struct_type={self.struct_type}, name='{self.name}'," \
               f" data_type={self.data_type})"

class Arguments:
    def __init__(self, args: List[str] = None):
        self.args = args or sys.argv[1:]
        self.manifests: structure.Manifests = structure.Manifests()
        self.properties: structure.Properties = structure.Properties()

    # noinspection PyArgumentList
    @property
    def parse_args(self) -> ParsedArguments:
        ret: Dict[str, Union[enums.Enum, str]] = {
            "struct_type": "",
            "name": "",
            "data_type": ""
        }
        for argument in self.args:
            if argument in [struct_type.value for struct_type in enums.StructureType]:
                ret["struct_type"] = enums.StructureType(argument)
            if argument in [fs_struct.value for fs_struct in enums.FileSystemStructureType]:
                ret["data_type"] = enums.FileSystemStructureType(argument)
            self.args.remove(argument)

        ret["struct_type"] = ret["struct_type"] or enums.StructureType.MANIFEST
        ret["data_type"] = ret["data_type"] or enums.FileSystemStructureType.ALL

        try:
            ret["name"] = self.args[0]
        except IndexError:
            if len(self.args) == 0:
                pass
            else:
                raise exceptions.TokenError("name is unfilled") from None

        return ParsedArguments(**ret)  # type: ignore

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(args={self.args})"
