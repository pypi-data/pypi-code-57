from dataclasses import dataclass

import pytest
from xtelligent_serial import (deserializer, serializer,
                               serialization, SequenceOf)
from xtelligent_serial.json import to_json


@serialization
class Boo:
    def __init__(self, x):
        self.root = x

    @property
    def y(self):
        return self.root * 2

    @classmethod
    def __serializer__(cls, instance):
        return {'x': instance.root, 'y': instance.y}

    @classmethod
    def __deserializer__(cls, raw_data):
        return cls(raw_data['x'])  # pylint: disable=not-callable


class Yah:
    def __init__(self, x):
        self.root = x

    @property
    def y(self):
        return self.root * 2


@serializer(Yah)
def serialize_yah(yah: Yah):
    return {'x': yah.root, 'y': yah.y}


@deserializer(Yah)
def deserialize_yah(raw_data) -> Yah:
    return Yah(raw_data['x'])


@dataclass
class NoneAble:
    x: object


@dataclass
class CA:
    a: int


@dataclass
class CB:
    ca: CA


@dataclass
class DeepClass:
    n: NoneAble
    cb: CB


@pytest.fixture
def deep_json():
    return '''
{
    "n": {"x": "hello"},
    "cb": {"ca": {"a": 2112}}
}
    '''


@dataclass
class DCContainer:
    items: SequenceOf[DeepClass]


@pytest.fixture
def container_class_json():
    dcc = DCContainer([
        DeepClass(NoneAble(None), CB(CA(100))),
        DeepClass(NoneAble(5.5), CB(CA(101))),
    ])
    return to_json(dcc)
