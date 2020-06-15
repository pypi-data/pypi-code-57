from argparse import ArgumentParser
from typing import Any, List, Literal, Optional, Union, get_args, get_origin


def type_to_str(type_annotation: Union[type, Any]) -> str:
    """Gets a string representation of the provided type.

    :param type_annotation: A type annotation, which is either a built-in type or a typing type.
    :return: A string representation of the type annotation.
    """
    # Built-in type
    if type(type_annotation) == type:
        return type_annotation.__name__

    # Typing type
    return str(type_annotation).replace("typing.", "").replace("typing_extensions.", "")


def get_dest(*name_or_flags: Union[str, List[str]], **kwargs: Any) -> str:
    """Gets the name of the destination of the argument.

    Args:
        name_or_flags: Either a name or a list of option strings, e.g. foo or -f, --foo.
        kwargs: Keyword arguments.
    Returns:
        The name of the argument (extracted from name_or_flags)
    """
    if "-h" in name_or_flags or "--help" in name_or_flags:
        return "help"

    return ArgumentParser().add_argument(*name_or_flags, **kwargs).dest


def is_option_arg(*name_or_flags) -> bool:
    """Returns whether the argument is an option arg (as opposed to a positional arg).

    :param name_or_flags: Either a name or a list of option strings, e.g. foo or -f, --foo.
    :return: True if the argument is an option arg, False otherwise.
    """
    return any(name_or_flag.startswith("-") for name_or_flag in name_or_flags)


def get_string_literals(literal_type: type, variable: str) -> List[str]:
    """Extracts the values from a Literal type and ensures that the values are all strings."""
    choices = list(get_args(literal_type))
    if not all(isinstance(choice, str) for choice in choices):
        raise ValueError(
            f'The type for variable "{variable}" contains a non-string literal.\n'
            f"Currently only string literals are supported."
        )
    return choices


def is_literal_type(tp: type) -> bool:
    """Test if the type is a Literal type."""
    return get_origin(tp) is Literal


def is_union_type(tp: type) -> bool:
    """Test if the type is a union type."""
    return get_origin(tp) is Union


def is_optional_type(tp: type) -> Optional[type]:
    """Test if the type is a direct union with None, such as Optional[T]."""
    if not is_union_type(tp):
        return None
    args = get_args(tp)
    if len(args) == 2:
        if args[0] is type(None):  # noqa
            return args[1]
        elif args[1] is type(None):  # noqa
            return args[0]
    return None
