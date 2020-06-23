#  Copyright (c) 2020 Chris Stranex
#  See LICENSE for licencing information.
#
#  There is NO WARRANTY, to the extent permitted by law.
#
from typing import NamedTuple, Dict


class MethodHandler(NamedTuple):
    method_name: str
    request: object
    response: object
    request_type: str
    response_type: str


MethodHandlers = Dict[str, MethodHandler]


def method(request, response, request_type, response_type, name, handlers, req_handler):
    """The generic rpc method decorator that defines methods for a particular rpc service"""

    def wrap(f):
        class_name = f.__qualname__.rsplit('.', 1)[0]
        if class_name not in handlers:
            handlers[class_name] = {}

        handlers[class_name][name or f.__name__] = MethodHandler(
            f.__name__,
            request,
            response,
            request_type,
            response_type
        )

        return req_handler(f)

    return wrap
