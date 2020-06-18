#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

import unittest
from datetime import datetime

from hamcrest import assert_that
from hamcrest import starts_with

from nti.ntiids.common import generate_ntiid

from nti.ntiids.tests import SharedConfiguringTestLayer


class TestCommon(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_generate_ntiid(self):
        ntiid = generate_ntiid(u'FOO', now=datetime.utcfromtimestamp(1000))
        assert_that(ntiid,
                    starts_with('tag:nextthought.com,2011-10:NTI-FOO-system_19700101001640_000000'))
