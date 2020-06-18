#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import uuid
from datetime import datetime

from zope.security.management import system_user

from nti.ntiids.ntiids import make_ntiid
from nti.ntiids.ntiids import make_specific_safe

#: NTI provider
NTI = u'NTI'

#: System username
SYSTEM_USER_NAME = getattr(system_user, 'title').lower()

logger = __import__('logging').getLogger(__name__)


def generate_ntiid(nttype, provider=NTI, now=None):
    now = datetime.utcnow() if now is None else now
    dstr = now.strftime("%Y%m%d%H%M%S %f")
    rand = str(uuid.uuid4().time_low)
    specific = make_specific_safe(u"%s_%s_%s" % (SYSTEM_USER_NAME, dstr, rand))
    result = make_ntiid(provider=provider,
                        nttype=nttype,
                        specific=specific)
    return result
