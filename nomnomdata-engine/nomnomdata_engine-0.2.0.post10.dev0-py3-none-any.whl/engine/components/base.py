from abc import ABCMeta, abstractmethod
from typing import List


class ParameterType(metaclass=ABCMeta):
    """
    ParameterType is the base class for all parameter types.
    Should never be directly instantiated.
    """

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


class Parameter:
    """[summary]

        :param type: [description]
        :param name: [description]
        :param display_name: [description], defaults to ""
        :param help_header_id: [description], defaults to None
        :param help_md_path: [description], defaults to None
        :param required: [description], defaults to False
        :param description: [description], defaults to ""
        :param default: [description], defaults to None
    """

    def __init__(
        self,
        type: ParameterType,
        name: str,
        display_name: str = "",
        help_header_id: str = None,
        help_md_path: str = None,
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
    """[summary]

        :param name: [description], defaults to "general"
        :type name: str, optional
        :param display_name: [description], defaults to "General Parameters"
        :type display_name: str, optional
        :param description: [description], defaults to ""
        :type description: str, optional
        :param collapsed: [description], defaults to False
        :type collapsed: bool, optional
        :param shared_parameter_group_uuid: [description], defaults to ""
        :type shared_parameter_group_uuid: str, optional
    """

    def __init__(
        self,
        *args: List[Parameter],
        name: str = "general",
        display_name: str = "General Parameters",
        description: str = "",
        collapsed: bool = False,
        shared_parameter_group_uuid: str = "",
    ):

        self.parameters = args
        self.collapsed = collapsed
        self.shared_parameter_group_uuid = shared_parameter_group_uuid
        self.description = description
        self.name = name
        self.display_name = display_name
        self.type = "group"

    def serialize(self):
        result = {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "type": self.type,
            "collapsed": self.collapsed,
            "parameters": [p.serialize() for p in self.parameters],
        }
        if self.shared_parameter_group_uuid:
            result["shared_parameter_group_uuid"] = (self.shared_parameter_group_uuid,)
        return result


class Connection(ParameterType):
    def __init__(
        self,
        connection_type_uuid: str,
        parameter_groups: List[ParameterGroup],
        description: str = "",
        alias: str = "",
        categories: List[str] = None,
    ):
        self.type = "connection"
        self.connection_type_uuid = connection_type_uuid
        self.parameter_groups = parameter_groups
        self.description = description
        self.alias = alias
        self.categories = categories

    @property
    def all_parameters(self):
        return {p.name: p for pg in self.parameter_groups for p in pg.parameters}

    def serialize(self):
        return {"connection_type_uuid": self.connection_type_uuid}
