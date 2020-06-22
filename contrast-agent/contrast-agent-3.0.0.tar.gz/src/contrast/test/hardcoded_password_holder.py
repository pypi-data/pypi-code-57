# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
from contrast.extern.six import PY3


class HardcodedPasswordHolder(object):
    # Should be found
    PASSWORD = "foo"
    PASSKEY = "foo"
    PASSPHRASE = "foo"
    SECRET = "foo"
    PASSWORD_OK = b"foo" if PY3 else bytearray("foo")
    PASSWORD_UNDER = "__foo"

    # Should not be found - names
    PASSWORD_DATE = "foo"
    PASSWORD_FORGOT = "foo"
    PASSWORD_FORM = "foo"
    PASSWORD_ENCODE = "foo"
    PASSWORD_PATTERN = "foo"
    PASSWORD_PREFIX = "foo"
    PASSWORD_PROP = "foo"
    PASSWORD_SUFFIX = "foo"
    PASSWORD_URL = "foo"
    PASSWORD_BASE = "foo"
    PaSsWoRd_BaSe = "foo"
    PASSWORD_FILE = "foo"
    __PASSWORD = "foo"
    KEY_REASSIGN = PASSWORD

    # Should not be found - values
    PASSWORD_DOTS = "foo.bar"
    PASSWORD_UNDERSCORE = "foo_bar"
    PASSWORD_MIXED = "foo.bar_baz"
    PASSWORD_NUMBERS = 12345
    os.environ.setdefault("PASSWORD", "foo")
    PASSWORD = os.environ.get("PASSWORD")
