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

    @property
    def shared_object_type_uuid(self):
        return None

    def validate(self, val):
        pass

    def convert(self, val):
        return val


class Parameter:
    """
        Parameter for use in a ParameterGroup, also contains options
        to control the look in the Nominode UI

        :param type:
            Set the type to allow validation of the parameter and
            so the UI understands how to render this parameter.
            Example valid parameter type :class:`~nomnomdata.engine.parameters.String`
        :param name:
            Parameter name, will be the key used in the final result passed to
            your function.
        :param display_name:
            The name of the parameter to be displayed to the user.
        :param help_header_id:
            Header ID in any MD file declared in upper scope that will be
            linked to this parameter.
        :param help_md_path:
            Full path to an MD file that will be linked
            to this parameter. Cannot be used with help_header_id.
        :param required:
            Setting this to true will require the user to set a value for this parameter,
            defaults to False
        :param description:
            The long form description the UI will diplay next
            to the parameter
        :param default:
            Default value of the parameter will be set as on task creation,
            valid values vary by the ParameterType you use, defaults to nothing
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
        if help_header_id and help_md_path:
            raise ValueError("Cannot use both help_header_id and help_md_path")
        if help_header_id:
            self.help = {"header_id": help_header_id}
        elif help_md_path:
            self.help = {"file": help_md_path}
        else:
            self.help = None
        self.display_name = display_name or self.name.capitalize()
        self.required = required
        self.description = description
        self.default = default

    def validate(self, val):
        return self.type.validate(val)

    def convert(self, val):
        return self.type.convert(val)

    def __str__(self):
        return f"{self.type.__class__.__name__} Parameter"

    def __repr__(self):
        return f"<{self.type.__class__.__name__} Parameter>"


class ParameterGroup:
    """ParameterGroup acts as a logical and visual grouping for parameters

        :param name:
            Unique key for this group, defaults to "general"
        :warning: you cannot use parameter groups with the same name on one action
        :param display_name:
            Display name to render in the UI, defaults to "General Parameters"
        :param description: UI description for this parameter group, defaults to ""
        :param collapsed:
            If the UI should collapse this parameter group when rendering,
            defaults to False
        :param shared_parameter_group_uuid:
            UUID of the shared parameter group defined for this parameter,
            can be safely left undefined in 95% of cases
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


class Connection(ParameterType):
    """
        Connections are generally used for authentication credentials,
        parameters will be stored encrypted on the Nominode instead of in plain text and can require
        seperate permissions to be viewed or used.


        :param connection_type_uuid:
            Unique ID associated with this Connection
        :param parameter_groups:
            ParameterGroups in this connection
        :param description:
            Description of the connection to be rendered on the UI, defaults to ""
        :param alias:
            Short(er) alias for the connection
        :param categories:
            Categories this connection belongs to, for easier sorting in the UI.
    """

    type = "connection"

    def __init__(
        self,
        connection_type_uuid: str,
        parameter_groups: List[ParameterGroup],
        description: str = "",
        alias: str = "",
        categories: List[str] = None,
    ):

        self.connection_type_uuid = connection_type_uuid
        self.parameter_groups = parameter_groups
        self.description = description
        self.alias = alias
        self.categories = categories

    @property
    def all_parameters(self):
        return {p.name: p for pg in self.parameter_groups for p in pg.parameters}
