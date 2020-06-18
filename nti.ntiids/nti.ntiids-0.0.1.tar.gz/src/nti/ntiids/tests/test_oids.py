#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import none
from hamcrest import assert_that
from hamcrest import has_entries
from hamcrest import has_property

import fudge
import unittest

from nti.externalization.extension_points import set_external_identifiers

from nti.ntiids.oids import to_external_ntiid_oid
from nti.ntiids.oids import setExternalIdentifiers

from nti.ntiids.tests import SharedConfiguringTestLayer


class TestOIDs(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_hookable(self):
        assert_that(set_external_identifiers,
                    has_property('implementation', is_(setExternalIdentifiers)))

    @fudge.patch('nti.ntiids.oids.toExternalOID')
    def test_to_external_ntiid_oid(self, mock_teo):
        mock_teo.is_callable().with_args().returns('0x01:666f6f')
        ntiid = to_external_ntiid_oid(object())
        assert_that(ntiid,
                    is_('tag:nextthought.com,2011-10:zope.security.management.system_user-OID-0x01:666f6f'))

        class O(object):
            creator = 'aizen'

        ntiid = to_external_ntiid_oid(O())
        assert_that(ntiid,
                    is_('tag:nextthought.com,2011-10:aizen-OID-0x01:666f6f'))

        ntiid = to_external_ntiid_oid(O(), mask_creator=True)
        assert_that(ntiid,
                    is_('tag:nextthought.com,2011-10:unknown-OID-0x01:666f6f'))

        class U(object):
            username = 'ichigo'

        class C(object):
            creator = U()

        ntiid = to_external_ntiid_oid(C())
        assert_that(ntiid,
                    is_('tag:nextthought.com,2011-10:ichigo-OID-0x01:666f6f'))

        mock_teo.is_callable().with_args().returns(None)
        ntiid = to_external_ntiid_oid(object())
        assert_that(ntiid, is_(none()))

    @fudge.patch('nti.ntiids.oids.toExternalOID')
    def test_set_external_identifiers(self, mock_teo):
        mock_teo.is_callable().with_args().returns('0x01:666f6f')

        class Context(object):
            id = 'my-id'
        context = Context()
        result = dict()
        setExternalIdentifiers(context, result)
        assert_that(result,
                    has_entries('NTIID', 'tag:nextthought.com,2011-10:zope.security.management.system_user-OID-0x01:666f6f',
                                'OID', 'tag:nextthought.com,2011-10:zope.security.management.system_user-OID-0x01:666f6f',
                                'ID', 'my-id'))

        ntiid = 'tag:nextthought.com,2011-10:zope.security.management.system_user-OID-0x01:666f6f'

        class Note(object):
            id = ntiid
        context = Note()
        result = dict(ID=ntiid)
        mock_teo.is_callable().with_args().returns('0x01:666f6f')
        setExternalIdentifiers(context, result)
        assert_that(result,
                    has_entries('NTIID', ntiid,
                                'OID', ntiid,
                                'ID', ntiid))

    def test_callable(self):
        class O(object):
            def to_external_ntiid_oid(self):
                return 'tag:nextthought.com,2011-10:system_user-OID-0x02:666f6f'

        ntiid = to_external_ntiid_oid(O())
        assert_that(ntiid,
                    is_('tag:nextthought.com,2011-10:system_user-OID-0x02:666f6f'))

    def test_volatile(self):
        class O(object):
            _v_to_external_ntiid_oid_False = 'tag:nextthought.com,2011-10:system_user-OID-0x03:777f6f'

        ntiid = to_external_ntiid_oid(O())
        assert_that(ntiid,
                    is_('tag:nextthought.com,2011-10:system_user-OID-0x03:777f6f'))
