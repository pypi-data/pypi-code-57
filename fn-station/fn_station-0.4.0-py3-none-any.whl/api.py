import inspect
import logging
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from typing import get_type_hints, Dict, Any

import marshmallow_dataclass
from marshmallow import ValidationError

from fn_station.utils import format_exception

log = logging.getLogger(__name__)


@dataclass
class HandledError(Exception):
    code: int
    message: str
    extra: Dict[str, Any] = field(default_factory=dict)


@lru_cache()
def dataclass_schema(cls):
    return marshmallow_dataclass.class_schema(cls)


def dataclass_schemas(func):
    hints = get_type_hints(func)
    for name in [*inspect.signature(func).parameters, "return"]:
        try:
            typ = hints[name]
        except KeyError:
            raise ValueError(f"Missing annotation for {name}")
        try:
            schema = dataclass_schema(typ)
        except Exception as e:
            raise TypeError(f"{name} is not a dataclass") from e
        yield name, schema


def error_response(code, message, **extra):
    return {
               "status": "error",
               "message": message,
               **extra,
           }, code


def validation_error_response(message):
    exception = sys.exc_info()[1]
    assert isinstance(exception, ValidationError)
    return error_response(400, message, info=exception.messages)


def exception_response(message):
    log.exception(message)
    exception = sys.exc_info()[1]
    return error_response(500, f"{message}: {format_exception(exception)}")


def respond(*args, **kwargs):
    try:
        return inner_respond(*args, **kwargs)
    except Exception:
        return exception_response("Internal error in framework")


def inner_respond(func, payload, schemas, return_schema):
    kwargs = {}
    for name, schema in schemas.items():
        try:
            value = payload[name]
        except KeyError:
            return error_response(400, f"Missing parameter {name}")

        try:
            value = schema().load(value)
        except ValidationError:
            return validation_error_response(f"Invalid value for parameter {name}")

        kwargs[name] = value

    try:
        result = func(**kwargs)
    except HandledError as e:
        return error_response(e.code, e.message, **e.extra)
    except Exception:
        return exception_response("Error in endpoint function")

    try:
        result = return_schema().dump(result)
    except ValidationError:
        return validation_error_response(f"Endpoint function returned invalid value")

    return {
               "status": "ok",
               "result": result,
           }, 200
