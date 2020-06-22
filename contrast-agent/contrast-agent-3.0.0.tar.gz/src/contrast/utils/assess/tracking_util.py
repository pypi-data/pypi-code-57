# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import io

from contrast.extern.six import iteritems

from contrast.agent.assess.utils import cs__tracked
from contrast.utils.decorators import fail_safely
from contrast.utils.assess.duck_utils import safe_iterator

import logging

logger = logging.getLogger("contrast")


@fail_safely("Failed check if obj is tracked", log_level="debug", return_value=False)
def is_tracked(obj):
    if obj is None:
        return False

    if isinstance(obj, dict):
        for key, value in iteritems(obj):
            if is_tracked(key) or is_tracked(value):
                return True
    elif isinstance(obj, io.IOBase):
        return getattr(obj, "cs__tracked", False) or getattr(obj, "cs__source", False)
    # These are the only safe objects where we can guarantee that we won't
    # destructively modify the object such that the application may see
    # different results.
    elif isinstance(obj, (list, tuple)):
        return any(is_tracked(item) for item in safe_iterator(obj))
    else:
        return cs__tracked(obj)

    return False
