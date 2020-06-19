#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Common utilities.

Currently, there is nothing here.

See :mod:`zc.intid.subscribers`
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zc.intid.subscribers import addIntIdSubscriber
from zc.intid.subscribers import removeIntIdSubscriber


def addIntId(ob, event=None):
    """
    Deprecated alias for :func:`zc.intid.subscribers.addIntIdSubscriber`
    """
    addIntIdSubscriber(ob, event)
add_intid = addIntId


def removeIntId(ob, event=None):
    """
    Deprecated alias for :func:`zc.intid.subscribers.removeIntIdSubscriber`
    """
    removeIntIdSubscriber(ob, event)
remove_intid = removeIntId
