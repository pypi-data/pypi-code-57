"""
Placing common invoker functions here since lambda_util imports local and aws invokers so
importing lambda_util from either of those will create a circular ref
"""
import json
from typing import Union, Any


def try_json(source: str) -> Union[dict, str]:
    """
    Tries to coerce JSON from a body string if not None, returns original value on fail
    :param source:
    :return: Union[dict, str]
    """
    if not isinstance(source, str):
        return source
    try:
        return json.loads(source)
    except ValueError:
        return source


def pass_through(source: Any) -> Any:
    """
    Pass-through converter for unhandled mime-types
    :param source: Any
    :return: Any
    """
    return source


RESPONSE_CONVERTERS = {
    'text/html': pass_through,
    'text/plain': pass_through,
    'application/xml': pass_through
}
