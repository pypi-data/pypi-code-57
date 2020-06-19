from dataclasses import dataclass
from datetime import datetime, timedelta


from xtelligent_serial import (register_serializer, register_deserializer,
                               serialize, deserialize)

# pylint: disable=invalid-name


def dthandler(dt: datetime):
    return dt.isoformat()


def str2dt(datestr: str):
    return datetime.fromisoformat(datestr)


def test_registry1():
    assert serialize(1) == 1
    assert deserialize(int, 2) == 2
    register_serializer(datetime, dthandler)
    d = datetime.utcfromtimestamp(1590432436)
    datestr = serialize(d)
    assert datestr == '2020-05-25T18:47:16'
    register_deserializer(datetime, str2dt)
    d2 = deserialize(datetime, datestr)
    assert d == d2


@dataclass
class X:
    a: int
    b: str

    @property
    def c(self):
        return f'{self.a}:{self.b}'

    @property
    def d(self):
        td = timedelta(days=self.a)
        return datetime.utcfromtimestamp(1577836800) + td

    def e(self): # pylint: disable=no-self-use
        return '????'

    @property
    def thedict(self):
        return {'nested_a': self.a, 'nested_d': self.d}

    @property
    def thelist(self):
        return [self.a, self.b, self.c, self.d]


def ds_x(raw_data):
    return X(raw_data['a'], raw_data['b'])


def test_registry2():
    register_serializer(datetime, dthandler)
    d = serialize(X(0, 'zero'))
    print(d)
    assert d == {'a': 0, 'b': 'zero', 'c': '0:zero', 'd': '2020-01-01T00:00:00',
                 'thedict': {'nested_a': 0, 'nested_d': '2020-01-01T00:00:00'}, 'thelist': [0, 'zero', '0:zero', '2020-01-01T00:00:00']}
    register_deserializer(X, ds_x)
    x = deserialize(X, {'a': 2, 'b': 'bbb'})
    assert x.a == 2
    assert x.b == 'bbb'


class A:
    def __init__(self, m):
        self.it_is_m = m


@dataclass
class B:
    y: A
    z: str


def ser_a(inst: A):
    return {'m': inst.it_is_m}


def ds_a(raw_data):
    return A(raw_data['m'])


def ds_b(raw_data):
    return B(
        deserialize(A, raw_data['y']),
        raw_data['z'])


def test_reversable_serialization():
    register_serializer(A, ser_a)
    register_deserializer(A, ds_a)
    register_deserializer(B, ds_b)
    b = B(A(2112), 'right?')
    d = serialize(b)
    final = deserialize(B, d)
    assert final.z == b.z


@dataclass(frozen=True)
class SpaceTimeClass:
    d: datetime
    x: float
    y: float
    z: float


def test_auto_dataclass():
    inputs = {'d': datetime.utcfromtimestamp(
        1590448075).isoformat(), 'x': 1.0, 'y': 1.5, 'z': 2.0}
    register_deserializer(datetime, str2dt)
    result = deserialize(SpaceTimeClass, inputs)
    assert result.x == 1.0
    assert result.z == 2.0
    assert result.d == datetime.utcfromtimestamp(1590448075)


def test_none():
    n = serialize(None)
    assert n is None
    n2 = deserialize(int, n)
    assert n2 is None
