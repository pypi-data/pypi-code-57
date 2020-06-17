# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Instrumentation helpers
"""
import threading

LOCAL = threading.local()


def guard_call(key, callback, *args, **kwargs):
    """ Conditionnaly call callback checking that it cannot be called
    recursively
    """
    # Set guard_call_set if not present, required for multi-threaded env
    if not hasattr(LOCAL, "guard_call_set"):
        LOCAL.guard_call_set = set()

    if key in LOCAL.guard_call_set:
        return {"status": "not_executed"}

    LOCAL.guard_call_set.add(key)

    try:
        output = callback(*args, **kwargs)
        return output
    finally:
        try:
            LOCAL.guard_call_set.remove(key)
        except KeyError:
            pass
