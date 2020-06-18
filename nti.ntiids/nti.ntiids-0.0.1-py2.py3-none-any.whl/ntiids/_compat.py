#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cross-version and cross-implementation compatibility helpers.
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

text_type = unicode if str is bytes else str # pylint:disable=undefined-variable
string_types = (basestring,) if str is bytes else (str,) # pylint:disable=undefined-variable


def text_(s, encoding='utf-8', err='strict'):
    """
    Return a unicode version of an object.
    If the object is a byte sequence it's decoded first

    :param object s: The object to get an unicode representation of.
    :param str encoding: The encoding to be used if ``s`` is a byte sequence
    :param str err: The err handling scheme to be used if ``s`` is a byte sequence
    """
    s = s.decode(encoding, err) if isinstance(s, bytes) else s
    return text_type(s) if s is not None else None


def bytes_(s, encoding='utf-8', errors='strict'):
    """
    If ``s`` is an instance of ``text_type``, return
    ``s.encode(encoding, errors)``, otherwise return ``s``
    """
    if not isinstance(s, bytes) and s is not None:
        s = s.encode(encoding, errors)
    return s
