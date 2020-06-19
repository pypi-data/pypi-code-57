#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that

from persistent import Persistent

from zope import component
from zope import interface

from zope.intid.interfaces import IIntIds

from zope.location.interfaces import ILocation

from nti.intid.common import addIntId
from nti.intid.common import removeIntId

from nti.intid.tests import WithMockDS
from nti.intid.tests import IntIdTestCase

from nti.intid.tests import mock_db_trans


@interface.implementer(ILocation)
class User(Persistent):

    __parent__ = None

    def __init__(self, username):
        self.__name__ = username


class TestCommon(IntIdTestCase):

    @WithMockDS
    def test_add_remove(self):
        with mock_db_trans() as conn:
            intids = component.getUtility(IIntIds)
            user = User('ichigo@bleach.com')
            conn.add(user)
            addIntId(user)
            assert_that(intids.queryId(user), is_not(none()))

            removeIntId(user)
            assert_that(intids.queryId(user), is_(none()))
