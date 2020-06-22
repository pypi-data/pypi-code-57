# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from io import IOBase

from contrast.extern import six

import logging

logger = logging.getLogger("contrast")

string_types = (six.string_types) + (six.binary_type, bytearray)


def is_iterable(value):
    """
    :param value: any type
    :return: True if iterable type like list, dict but NOT string
             False if string or any other type like database collection types
                   (pymongo Collection implements iter but is not an iterable
    """

    try:
        it = iter(value)
        if not hasattr(it, "__next__" if six.PY3 else "next"):
            return False
    except TypeError:
        return False

    return not isinstance(value, string_types)


def is_filelike(value):
    if six.PY2:
        return isinstance(value, file)

    return isinstance(value, IOBase)


def safe_obj_length(value):
    try:
        return len(value)
    except (AttributeError, TypeError):
        return 0


def safe_iterator(it):
    try:
        orig_pos = 0
        can_seek = False

        if hasattr(it, "tell") and hasattr(it, "seek"):
            orig_pos = it.tell()
            can_seek = True

        for x in it:
            yield x
    except Exception:
        logger.debug("safe_iterator failed to iterate over %s", it)
    finally:
        if can_seek:
            it.seek(orig_pos)
