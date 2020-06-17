"""The scene walker function"""

import functools
from types import FunctionType
from typing import Any


def walk(clock: int, value: Any) -> Any:
    """Walk a scene, calling found callables"""

    return_value: Any = None

    if isinstance(value, (bool, int, float, str)):
        return_value = value
    elif isinstance(value, (FunctionType, functools.partial)):
        return_value = value(clock)
    elif isinstance(value, tuple):
        _return_value = list()
        for _value in value:
            _return_value.append(walk(clock, _value))
        return_value = tuple(_return_value)
    elif isinstance(value, dict):  # pylint: disable=R1705
        return_value = {}
        for _key, _value in value.items():
            return_value[_key] = walk(clock, _value)
    else:
        raise ValueError(f"Unfamiliar value of type {type(value)} supplied")

    return return_value
