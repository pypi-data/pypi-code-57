# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Implements a single API for instrumenting all dbapi2-compliant modules
"""
from contrast.applies.sqli import apply_rule
from contrast.assess_extensions.cs_str import set_attr_on_type
from contrast.agent.assess import patch_manager


def _build_patch(database, action, orig_func):
    def patched_method(self, *args, **kwargs):
        return apply_rule(database, action, orig_func, self, *args, **kwargs)

    patched_method.__name__ = orig_func.__name__
    return patched_method


def _instrument_cursor_method(database, cursor, method_name):
    orig_method = getattr(cursor, method_name)
    new_method = _build_patch(database, method_name, orig_method)
    set_attr_on_type(cursor, method_name, new_method)
    patch_manager.register_patch(cursor, method_name, orig_method)


def instrument_cursor(database, cursor):
    """
    Instruments a dbapi2-compliant database cursor class

    @param database: Name of the database module being patched (e.g. "sqlite3")
    @param cursor: Reference to cursor class to be instrumented
    """
    _instrument_cursor_method(database, cursor, "execute")
    _instrument_cursor_method(database, cursor, "executemany")


def instrument_executescript(database, cursor):
    """
    Instruments the `executescript` method of a database cursor class

    The executescript method is non-standard but is provided by some drivers
    including sqlite3.

    @param database: Name of the database module being patched (e.g. "sqlite3")
    @param cursor: Reference to cursor class to be instrumented
    """
    _instrument_cursor_method(database, cursor, "executescript")
