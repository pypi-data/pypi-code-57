from __future__ import annotations

from argparse import ArgumentParser
from collections import OrderedDict
from copy import deepcopy
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    Set,
    Type,
    TypeVar,
    get_args,
    get_origin,
    get_type_hints,
)

from .utils import (
    get_dest,
    get_string_literals,
    is_literal_type,
    is_option_arg,
    is_optional_type,
    is_union_type,
    type_to_str,
)
from .types import StoreDictKeyPair, maybe_convert

__all__ = ["TypedFlags"]

TFType = TypeVar("TFType", bound="TypedFlags")
_DictType = TypeVar("_DictType", Dict[str, Any], "OrderedDict[str, Any]")


class TypedFlags(ArgumentParser):
    """TypedFlags is a typed argument parser that wraps Python's built-in ArgumentParser."""

    def __init__(self, *args, **kwargs):
        """Initializes the TypedFlags instance.

        Args:
            args: Arguments passed to the super class ArgumentParser.
            kwargs: Keyword arguments passed to the super class ArgumentParser.
        """
        # Whether the arguments have been parsed (i.e. if parse_args has been called)
        self._parsed = False

        # Set extra arguments to empty list
        self.extra_args = []

        # Create argument buffer
        self.argument_buffer = OrderedDict()

        # Get annotations from self and all super classes up through tap
        self._annotations = self._get_annotations()

        # Initialize the super class, i.e. ArgumentParser
        super().__init__(*args, **kwargs)

        # Add arguments to self
        self.add_arguments()  # Adds user-overridden arguments to the arguments buffer
        self._add_arguments()  # Adds all arguments in order to self

    def _add_argument(self, *name_or_flags, **kwargs) -> None:
        """Adds an argument to self (i.e. the super class ArgumentParser).

        Sets the following attributes of kwargs when not explicitly provided:
        - type: Set to the type annotation of the argument.
        - default: Set to the default value of the argument (if provided).
        - required: True if a default value of the argument is not provided, False otherwise.
        - action: Set to "store_true" if the argument is a required bool or a bool with default value False.
                  Set to "store_false" if the argument is a bool with default value True.
        - nargs: Set to "*" if the type annotation is List[str], List[int], or List[float].
        - help: Set to the argument documentation from the class docstring.

        Args:
            name_or_flags: Either a name or a list of option strings, e.g. foo or -f, --foo.
            kwargs: Keyword arguments.
        """
        # Get variable name
        variable = get_dest(*name_or_flags, **kwargs)

        # Get default if not specified
        if hasattr(self, variable):
            kwargs["default"] = kwargs.get("default", getattr(self, variable))

        # Set required if option arg
        if is_option_arg(*name_or_flags) and variable != "help":
            kwargs["required"] = kwargs.get("required", not hasattr(self, variable))

        # Set help if necessary
        if "help" not in kwargs:
            kwargs["help"] = "("

            # Type
            if variable in self._annotations:
                kwargs["help"] += type_to_str(self._annotations[variable]) + ", "

            # Required/default
            if kwargs.get("required", False):
                kwargs["help"] += "required"
            else:
                kwargs["help"] += "default="
                default = kwargs.get("default", None)
                kwargs["help"] += f"'{default}'" if isinstance(default, str) else str(default)

            kwargs["help"] += ")"

            # # Description
            # if variable in self.class_variables:
            #     kwargs['help'] += ' ' + self.class_variables[variable]['comment']

        # Set other kwargs where not provided
        if variable in self._annotations:
            # Get type annotation
            var_type = self._annotations[variable]

            # If type is not explicitly provided, set it if it's one of our supported default types
            if "type" not in kwargs:
                if (optional_type := is_optional_type(var_type)) is not None:
                    var_type = optional_type

                origin: Optional[type] = get_origin(var_type)

                # First check whether it is a literal type or a boxed literal type
                if origin is Literal:  # type: ignore[comparison-overlap]
                    kwargs["choices"] = get_string_literals(var_type, variable)
                    var_type = str

                elif origin in (list, set):
                    arg = get_args(var_type)[0]
                    if is_literal_type(arg):
                        # unpack the outer type and then the literal
                        kwargs["choices"] = get_string_literals(get_args(var_type)[0], variable)
                        kwargs["type"] = str
                        kwargs["nargs"] = kwargs.get("nargs", "*")
                    else:
                        # If List type, extract type of elements in list and set nargs
                        kwargs["type"] = maybe_convert(arg)
                        kwargs["nargs"] = kwargs.get("nargs", "*")

                elif origin is dict:
                    key_type, value_type = get_args(var_type)
                    kwargs["action"] = StoreDictKeyPair
                    kwargs["nargs"] = kwargs.get("nargs", "*")
                    kwargs["type"] = str
                    kwargs["key_type"] = maybe_convert(key_type)
                    kwargs["value_type"] = maybe_convert(value_type)

                elif origin is None:
                    # If bool then set action, otherwise set type
                    if var_type == bool:
                        kwargs["type"] = eval
                        kwargs["choices"] = [True, False]
                    else:
                        kwargs["type"] = maybe_convert(var_type)
                        if var_type == float:
                            kwargs["metavar"] = "FLOAT"
                        elif var_type == int:
                            kwargs["metavar"] = "INT"
                else:
                    raise ValueError(
                        f'Variable "{variable}" has type "{var_type}" which is not supported by default.\n'
                        f"Please explicitly add the argument to the parser by writing:\n\n"
                        f"def add_arguments(self) -> None:\n"
                        f'    self.add_argument("--{variable}", type=func, {"required=True" if kwargs["required"] else f"default={getattr(self, variable)}"})\n\n'
                        f'where "func" maps from str to {var_type}.'
                    )

        super().add_argument(*name_or_flags, **kwargs)

    def add_argument(self, *name_or_flags, **kwargs) -> None:
        """Adds an argument to the argument buffer, which will later be passed to _add_argument."""
        variable = get_dest(*name_or_flags, **kwargs)
        self.argument_buffer[variable] = (name_or_flags, kwargs)

    def _add_arguments(self) -> None:
        """Add arguments to self in the order they are defined as class variables (so the help string is in order)."""
        # Add class variables (in order)
        for variable in self._annotations:
            if variable in self.argument_buffer:
                name_or_flags, kwargs = self.argument_buffer[variable]
                self._add_argument(*name_or_flags, **kwargs)
            else:
                self._add_argument(f'--{variable.replace("_", "-")}')

        # Add any arguments that were added manually in add_arguments but aren't class variables (in order)
        for variable, (name_or_flags, kwargs) in self.argument_buffer.items():
            if variable not in self._annotations:
                self._add_argument(*name_or_flags, **kwargs)

    def add_arguments(self) -> None:
        """Explicitly add arguments to the argument buffer if not using default settings."""

    def process_args(self) -> None:
        """Perform additional argument processing and/or validation."""

    def parse_args(
        self: TFType, args: Optional[Sequence[str]] = None, known_only: bool = False
    ) -> TFType:
        """Parses arguments, sets attributes of self equal to the parsed arguments, and processes arguments.

        Args:
            args: List of strings to parse. The default is taken from `sys.argv`.
            known_only: If true, ignores extra arguments and only parses known arguments. Unparsed
                arguments are saved to self.extra_args.
        Returns:
            self, which is a Tap instance containing all of the parsed args.
        """
        # Parse args using super class ArgumentParser's parse_args or parse_known_args function
        if known_only:
            default_namespace, self.extra_args = super().parse_known_args(args)
        else:
            default_namespace = super().parse_args(args)

        # Copy parsed arguments to self
        for variable, value in vars(default_namespace).items():
            # Conversion from list to set
            if variable in self._annotations and get_origin(self._annotations[variable]) is set:
                value = set(value)

            # Set variable in self (and deepcopy)
            setattr(self, variable, deepcopy(value))

        # Process args
        self.process_args()

        # Indicate that args have been parsed
        self._parsed = True

        return self

    @classmethod
    def _get_from_self_and_super(
        cls, extract_func: Callable[[type], dict], dict_type: Type[_DictType]
    ) -> _DictType:
        """Return a dictionary mapping variable names to values.

        Variables and values are extracted from classes using key starting
        with this class and traversing up the super classes up through Tap.

        If super class and sub class have the same key, the sub class value is used.

        Super classes are traversed through breadth first search.

        Args:
            extract_func: A function that extracts from a class a dictionary mapping variables to values.
            dict_type: The type of dictionary to use (e.g. dict, OrderedDict, etc.)
        Returns:
            A dictionary mapping variable names to values from the class dict.
        """
        visited: Set[type] = set()
        super_classes = [cls]
        dictionary = dict_type()

        while len(super_classes) > 0:
            super_class = super_classes.pop(0)

            if super_class not in visited and issubclass(super_class, TypedFlags):
                super_dictionary = extract_func(super_class)

                # Update only unseen variables to avoid overriding subclass values
                for variable, value in super_dictionary.items():
                    if variable not in dictionary:
                        dictionary[variable] = value
                for variable in super_dictionary.keys() - dictionary.keys():
                    dictionary[variable] = super_dictionary[variable]

                super_classes += list(super_class.__bases__)
                visited.add(super_class)

        return dictionary

    def _get_class_dict(self) -> Dict[str, Any]:
        """Return a dictionary mapping class variable names to values from the class dict."""
        class_dict = self._get_from_self_and_super(extract_func=vars, dict_type=dict,)
        return {
            var: val
            for var, val in class_dict.items()
            if not (var.startswith("_") or callable(val) or isinstance(val, staticmethod))
        }

    def _get_annotations(self) -> Dict[str, Any]:
        """Return a dictionary mapping variable names to their type annotations."""
        all_annotations = self._get_from_self_and_super(extract_func=get_type_hints, dict_type=dict)
        return {k: v for k, v in all_annotations.items() if not k.startswith("_")}

    def _get_argument_names(self) -> Set[str]:
        """Returns a list of variable names corresponding to the arguments."""
        return set(self._get_class_dict().keys()) | set(self._annotations.keys())

    def as_dict(self) -> Dict[str, Any]:
        """Returns the member variables corresponding to the class variable arguments.

         :return: A dictionary mapping each argument's name to its value.
         """
        if not self._parsed:
            raise ValueError("You should call `parse_args` before retrieving arguments.")

        return {var: getattr(self, var) for var in self._get_argument_names()}

    def __str__(self) -> str:
        """Returns a string representation of self.

        Returns:
            A formatted string representation of the dictionary of all arguments.
        """
        args_dict = self.as_dict()
        formatted = []
        for k in sorted(args_dict):
            v = args_dict[k]
            formatted.append(f'{k}="{v}"' if isinstance(v, str) else f"{k}={v}")
        return "Namespace(" + ", ".join(formatted) + ")"

    def convert_arg_line_to_args(self, arg_line: str) -> List[str]:
        """Parse each line like a YAML file."""
        arg_line = arg_line.split("#", maxsplit=1)[0]  # split off comments
        if not arg_line.strip():  # empty line
            return []
        key, value = arg_line.split(sep=":", maxsplit=1)
        key = key.rstrip()
        value = value.strip()
        if key[0] == " ":
            key = key.strip()
            return [f"{key}={value}"]
        if not value:  # no associated value
            values = []
        elif value[0] == '"' and value[-1] == '"':  # if wrapped in quotes, don't split further
            values = [value[1:-1]]
        else:
            values = value.split()
        if len(values) == 1 and values[0] in ("true", "false"):
            values = [values[0].title()]
        key = key.replace("_", "-")
        return [f"--{key}"] + values
