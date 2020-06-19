#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods
# pylint: disable=global-statement,broad-except
# pylint: disable=arguments-differ,no-member
import unittest

import BTrees

import zc.intid
import zope.intid
import zope.testing.cleanup
from zope.component.hooks import setHooks

from nti.site import testing as site_testing

class mock_db_trans(site_testing.persistent_site_trans):


    def on_connection_opened(self, conn):
        super(mock_db_trans, self).on_connection_opened(conn)
        from nti.intid.utility import IntIds
        folder = conn.root()[str(self.main_application_folder_name)]
        lsm = folder.getSiteManager()
        intids = IntIds('_ds_intid', family=BTrees.family64)
        intids.__name__ = '++etc++intids'
        intids.__parent__ = folder
        lsm.registerUtility(intids, provided=zope.intid.IIntIds)
        lsm.registerUtility(intids, provided=zc.intid.IIntIds)



WithMockDS = site_testing.uses_independent_db_site


class SharedConfiguringTestLayer(site_testing.SharedConfiguringTestLayer):

    set_up_packages = ('nti.intid',)

    @classmethod
    def setUp(cls):
        setHooks()
        cls.setUpPackages()

    @classmethod
    def tearDown(cls):
        cls.tearDownPackages()
        zope.testing.cleanup.cleanUp()

    @classmethod
    def testSetUp(cls, test=None):
        setHooks()

    @classmethod
    def testTearDown(cls):
        pass


class IntIdTestCase(unittest.TestCase):
    layer = SharedConfiguringTestLayer
