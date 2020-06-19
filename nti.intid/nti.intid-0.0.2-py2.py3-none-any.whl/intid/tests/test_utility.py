#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods
# pylint: disable=attribute-defined-outside-init

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import raises
from hamcrest import calling
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property
does_not = is_not

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.testing.base import AbstractTestBase

import struct

from zc.intid import IIdAddedEvent
from zc.intid import IIdRemovedEvent

from zc.intid.interfaces import IntIdInUseError

from zope import interface

from zope.component import eventtesting

from zope.location.interfaces import ILocation

from persistent import Persistent

from nti.intid.interfaces import IIntIds

from nti.intid.utility import IntIds


@interface.implementer(ILocation)
class P(Persistent):
    pass


class ConnectionStub(object):
    next = 1

    database_name = 'ConnectionStub'

    def db(self):
        return self

    def add(self, ob):
        ob._p_jar = self
        ob._p_oid = struct.pack(">I", self.next)
        self.next += 1

    def register(self, *args, **kwargs):
        pass


class TestUtility(AbstractTestBase):

    def setUp(self):
        super(TestUtility, self).setUp()
        eventtesting.setUp()

    def test_interface(self):
        u = IntIds("_ds_id")
        assert_that(u, validly_provides(IIntIds))
        assert_that(u, verifiably_provides(IIntIds))
        assert_that(repr(u), is_not(none()))

    def test_non_keyreferences(self):
        u = IntIds("_ds_id")
        obj = object()
        assert_that(u.queryId(obj), is_(none()))
        assert_that(u.unregister(obj), is_(none()))
        assert_that(calling(u.getId).with_args(obj), raises(KeyError))

    def test_event(self):
        u = IntIds("_ds_id")

        obj = P()
        stub = ConnectionStub()
        stub.add(obj)
        assert_that(stub.db(), is_(stub))

        assert_that(obj, 
                    has_property('_p_jar', is_(stub)))

        count = 1
        assert_that(calling(u.getId).with_args(obj), raises(KeyError))
        assert_that(calling(u.getId).with_args(P()), raises(KeyError))

        assert_that(u.queryId(obj), is_(none()))
        assert_that(u.queryId(obj, 42), is_(42))
        assert_that(u.queryId(P(), 42), is_(42))
        assert_that(u.queryObject(42), is_(none()))
        assert_that(u.queryObject(42, obj), is_(obj))

        uid = u.register(obj)
        assert_that(u.getObject(uid), is_(obj))
        assert_that(u.queryObject(uid), is_(obj))
        assert_that(u.getId(obj), is_(uid))
        assert_that(u.queryId(obj), is_(uid))
        assert_that(eventtesting.getEvents(IIdAddedEvent), has_length(count))

        uid2 = u.register(obj)
        assert_that(uid, is_(uid2))

        u.unregister(obj)
        assert_that(calling(u.getObject).with_args(uid), raises(KeyError))
        assert_that(calling(u.getId).with_args(obj), raises(KeyError))
        assert_that(eventtesting.getEvents(IIdRemovedEvent), has_length(count))

        next_id = u._v_nextid
        assert_that(u.randomize(), is_not(next_id))

    def test_force(self):
        u = IntIds("_ds_id")
        obj = P()
        obj._ds_id = 100
        stub = ConnectionStub()
        stub.add(obj)
        
        u.force_register(100, obj)
        assert_that(calling(u.force_register).with_args(100, P()), 
                    raises(IntIdInUseError))
        
        assert_that(calling(u.force_unregister).with_args(200, obj), 
                    raises(KeyError))

        assert_that(calling(u.force_unregister).with_args(100, P()), 
                    raises(KeyError))

        u.force_unregister(100, obj, True)
