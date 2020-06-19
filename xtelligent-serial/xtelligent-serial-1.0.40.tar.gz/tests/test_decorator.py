from xtelligent_serial import (serialize, deserialize)

from .fixtures import Boo, Yah, NoneAble, deserialize_yah

def test_decorator1():
    d = serialize(Boo(2))
    assert d['y'] == 4
    b = deserialize(Boo, d)
    assert b.root == 2

def test_decorator2():
    yah = Yah(3)
    d = serialize(yah)
    assert isinstance(d, dict)
    y2 = deserialize(Yah, d)
    assert yah.root == y2.root
    assert getattr(deserialize_yah, 'deserialize')
    y3 = deserialize_yah.deserialize(d)
    assert yah.root == y3.root

def test_noneable():
    n1 = NoneAble(None)
    d = serialize(n1)
    assert d == {'x': None}
    n2 = deserialize(NoneAble, d)
    assert n2.x is None
