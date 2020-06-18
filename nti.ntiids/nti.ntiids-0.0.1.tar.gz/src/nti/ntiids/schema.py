#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Support for using NTIIDs in a zope schema.

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from nti.ntiids._compat import text_type
from nti.ntiids.ntiids import validate_ntiid_string

from nti.schema.field import ValidURI


class ValidNTIID(ValidURI):
    """
    A schema field that checks that the value is a correctly
    formed NTIID. (This does not perform any validation that the
    value is actually reachable or accessibly in a library or catalog.)
    """

    _type = text_type

    def fromUnicode(self, value):
        # The very first thing the superclass does is turn
        # the value into a bytestring again (under py2),
        # which is obviously wrong for us. So skip that.
        value = value.strip()
        self.validate(value)
        return value

    def _validate(self, value):
        super(ValidNTIID, self)._validate(value)
        validate_ntiid_string(value)
