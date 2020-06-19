from functools import update_wrapper
from typing import Type

from .registry import register_deserializer, register_serializer, deserialize
from .signatures import Serializer, Deserializer

# pylint: disable=invalid-name,redefined-builtin

def serializer(type: Type):
    '''Decorator that registers a function as a serializer for a type.

    See:`examples.simple`.
    '''
    def wrapper(func: Serializer):
        update_wrapper(wrapper, func)
        register_serializer(type, func)
        return func
    return wrapper

def deserializer(type: Type):
    '''Decorator that registers a function as a deserializer for a type.
    The decorated function receives a `deserialize` method that takes a single
    argument - the data to deserialize to `type`.

    See:`examples.simple`.
    '''
    def wrapper(func: Deserializer):
        update_wrapper(wrapper, func)
        register_deserializer(type, func)
        def ds(data_dict) -> type:
            return deserialize(type, data_dict)
        setattr(func, 'deserialize', ds)
        return func
    return wrapper

def serialization(Cls):
    '''Marks a class for serialization.

    See:`examples.simple`
    '''
    # pylint: disable=unnecessary-lambda
    register_serializer(Cls, lambda raw_data: Cls.__serializer__(raw_data))
    register_deserializer(Cls, lambda raw_data: Cls.__deserializer__(raw_data))
    return Cls
