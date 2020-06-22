# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
from contrast.extern.six import PY3


class HardcodedKeyHolder(object):
    # Should be found
    STR_KEY = "foo"
    BLAH_KEY = b"foo" if PY3 else bytearray("foo")
    BLAH_AES = b"foo" if PY3 else bytearray("foo")
    DES_BLAH = b"foo" if PY3 else bytearray("foo")
    IVASDF = b"foo" if PY3 else bytearray("foo")
    BLAH_SECRET = b"foo" if PY3 else bytearray("foo")
    KEY_STRING = b"foo" if PY3 else "foo"
    VALUE_PREFIX = "__foo"

    # Should not be found - values
    KEY_INT = 12345
    KEY_EMPTY = []
    KEY_NON_BYTES = ["asdf"]
    CONTENT_CODES = [200, 300, 400, 5000]
    __KEY_PREFIX = "foo"
    KEY_REASSIGN = BLAH_KEY

    os.environ.setdefault("KEY_FUNCTION", "foo")
    KEY_FUNCTION = os.environ.get("KEY_FUNCTION")
