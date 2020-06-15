"""Custom types for use with TypedFlags."""
from argparse import Action, ArgumentTypeError
from typing import Any, Callable, NewType, Mapping, Union

__all__ = ["StoreDictKeyPair", "PositiveInt", "maybe_convert"]


class StoreDictKeyPair(Action):
    """Action for parsing dictionaries on the commandline."""

    def __init__(
        self, option_strings: Any, key_type: type, value_type: type, *args: Any, **kwargs: Any
    ):
        self._key_type = key_type
        self._value_type = value_type
        super().__init__(option_strings, *args, **kwargs)

    def __call__(self, parser: Any, namespace: Any, values: Any, option_string: Any = None) -> None:
        my_dict = {}
        for kv in values:
            k, v = kv.split("=")
            my_dict[self._key_type(k.strip())] = self._value_type(v.strip())
        setattr(namespace, self.dest, my_dict)


PositiveInt = NewType("PositiveInt", int)


def _to_positive_int(arg: str) -> PositiveInt:
    num = int(arg)
    if num > 0:
        return PositiveInt(num)
    raise ArgumentTypeError(f"{num} is not positive")


TYPE_TO_CONSTRUCTOR: Mapping[type, Callable[[str], Any]] = {
    PositiveInt: _to_positive_int,
}


def maybe_convert(arg_type: type) -> Union[type, Callable]:
    return TYPE_TO_CONSTRUCTOR.get(arg_type, arg_type)
