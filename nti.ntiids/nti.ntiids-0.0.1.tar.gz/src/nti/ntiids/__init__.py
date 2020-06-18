#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Importing this module has the side-effect of calling :func:`nti.ntiids.oids.set_hook`.
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import zope.i18nmessageid

MessageFactory = zope.i18nmessageid.MessageFactory('nti.ntiids')

# Set the correct OID hookable function
# This must be below the MessageFactory because the factory is
# imported by other modules.
from nti.ntiids.oids import set_hook # pylint:disable=wrong-import-position
set_hook()
del set_hook
