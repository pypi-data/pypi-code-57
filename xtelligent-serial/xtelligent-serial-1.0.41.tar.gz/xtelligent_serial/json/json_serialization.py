from json import dumps, loads
from typing import Type

# pylint: disable=redefined-builtin

from .. import serialize, deserialize, JSONSerializable

def to_json(target: JSONSerializable, **kwargs) -> str:
    '''Serializes the target object to JSON.

    Example:
        >>> from xtelligent_serial.json import to_json
        >>> to_json({'x': 1})
        '{"x": 1}'
    '''
    d = serialize(target)
    return dumps(d, **kwargs)

def from_json(type: Type, json_text: str, **kwargs) -> JSONSerializable:
    '''Deserializes a JSONSerializable instance from JSON.

    Example:
        >>> from xtelligent_serial import serialization
        >>> from xtelligent_serial.json import from_json
        >>> @serialization
            class Boo:
                def __init__(self, x):
                    self.x = x
                @classmethod
                def __serializer__(cls, instance):
                    return {'x': instance.x}
                @classmethod
                def __deserializer__(cls, raw_data):
                    return cls(raw_data['x']) # pylint: disable=not-callable
        >>> b = from_json(Boo, '{"x": 4}')
        <__main__.Boo object at 0x7fcfcdcb4fa0>
        >>> b.x
        4
    '''
    d = loads(json_text, **kwargs)
    return deserialize(type, d)
