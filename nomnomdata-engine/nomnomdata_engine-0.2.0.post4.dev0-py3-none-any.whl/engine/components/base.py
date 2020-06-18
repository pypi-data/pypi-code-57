from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List


class ParameterType(metaclass=ABCMeta):
    @property
    @abstractmethod
    def type(self):
        pass

    def validate(self, val):
        pass

    def serialize(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def convert(self, val):
        return val


@dataclass
class Help:
    header_id: str = None
    md_path: Path = None

    def serialize(self):
        if self.header_id:
            return {"header_id": self.header_id}
        elif self.md_path:
            return {"file": str(self.md_path)}


class Parameter:
    type: ParameterType
    name: str
    help: Help
    display_name: str
    required: bool
    description: str
    default: object

    def __init__(
        self,
        type: ParameterType,
        name: str,
        display_name: str = "",
        help: Help = None,
        required: bool = False,
        description: str = "",
        default: object = None,
    ):
        self.type = type
        self.name = name
        self.help = help
        self.display_name = display_name or self.name.capitalize()
        self.required = required
        self.description = description
        self.default = default

    def serialize(self):
        result = {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "type": self.type.type,
            "required": self.required,
        }
        if self.help:
            result["help"] = self.help.serialize()
        if self.default:
            result["default"] = self.default
        result.update(self.type.serialize())
        return result

    def validate(self, val):
        return self.type.validate(val)

    def convert(self, val):
        return self.type.convert(val)

    def __str__(self):
        return f"{self.type.__class__.__name__} Parameter"

    def __repr__(self):
        return f"<{self.type.__class__.__name__} Parameter>"


class ParameterGroup:
    type = "group"
    parameters = List[Parameter]
    collapsed: bool
    shared_parameter_group_uuid: str
    description: str
    name: str
    display_name: str

    def __init__(
        self,
        *args: List[Parameter],
        display_name: str = "",
        name: str = "General",
        collapsed: bool = False,
        shared_parameter_group_uuid: str = "",
        description: str = "",
    ):
        self.parameters = args
        self.collapsed = collapsed
        self.shared_parameter_group_uuid = shared_parameter_group_uuid
        self.description = description
        self.name = name
        self.display_name = display_name

    def serialize(self):
        result = {
            "name": self.name,
            "display_name": self.display_name or self.name.capitalize(),
            "description": self.description,
            "type": self.type,
            "collapsed": self.collapsed,
            "parameters": [p.serialize() for p in self.parameters],
        }
        if self.shared_parameter_group_uuid:
            result["shared_parameter_group_uuid"] = (self.shared_parameter_group_uuid,)
        return result


@dataclass
class Connection(ParameterType):
    type = "connection"
    connection_type_uuid: str
    parameter_groups: List[ParameterGroup]
    description: str = ""
    alias: str = ""
    categories: List[str] = None

    @property
    def all_parameters(self):
        return {p.name: p for pg in self.parameter_groups for p in pg.parameters}

    def serialize(self):
        return {"connection_type_uuid": self.connection_type_uuid}
