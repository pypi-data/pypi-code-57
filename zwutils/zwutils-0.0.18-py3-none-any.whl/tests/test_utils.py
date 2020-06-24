# -*- coding: utf-8 -*-
import pytest
import time

import zwutils.comm as comm

class TestUtils:
    # pylint: disable=no-member
    def test_dict2attr(self):
        r = comm.dict2attr({
            'ks': 'v1',
            'kn': 2,
            'ka': [1, '2'],
            'kd': {'1':1, '2':2},
            'knone': None
        })
        r2 = comm.dict2attr(None)
        assert r.ks == 'v1'
    
    def test_attr2dict(self):
        o = type('', (), {})()
        o.a1 = 'a'
        o.a2 = 'b'
        r = comm.attr2dict(o)
        assert r['a1'] == 'a'

    def test_extend_attr(self):
        b = {'a':'a', 'b':'b'}
        e = {'b':'bb', 'c':'c', 'd':1}
        o = comm.extend_attrs(comm.dict2attr(b), e)
        assert o.b == 'bb' and o.c == 'c' and o.d == 1
        o = comm.extend_attrs(b, e)
        assert o.b == 'bb' and o.c == 'c' and o.d == 1
        o = comm.extend_attrs(comm.dict2attr(b), comm.dict2attr(e))
        assert o.b == 'bb' and o.c == 'c' and o.d == 1

        o = comm.extend_attrs(None, e)
        assert o.b == 'bb' and o.c == 'c' and o.d == 1
        o = comm.extend_attrs(comm.dict2attr(b), None)
        assert o.a == 'a' and o.b == 'b'

    def test_update_attrs(self):
        b = {'a':'a', 'b':'b'}
        e = {'b':'bb', 'c':'c'}
        o = comm.update_attrs(comm.dict2attr(b), e)
        assert o.b == 'bb' and not hasattr(o, 'c')
        o = comm.update_attrs(b, e)
        assert o.b == 'bb' and not hasattr(o, 'c')
        o = comm.update_attrs(comm.dict2attr(b), comm.dict2attr(e))
        assert o.b == 'bb' and not hasattr(o, 'c')

        o = comm.update_attrs(None, e)
        assert not hasattr(o, 'b') and not hasattr(o, 'c')
        o = comm.update_attrs(comm.dict2attr(b), None)
        assert o.a == 'a' and o.b == 'b'
    
    def test_contains_digits(self):
        assert comm.contains_digits('aaabb, 332 44 -adaf')
        assert not comm.contains_digits('aaabb,-adaf')

