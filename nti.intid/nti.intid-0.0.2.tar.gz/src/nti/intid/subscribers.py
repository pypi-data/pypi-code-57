#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Subscribers for events.

These are configured by loading this packages's ``configure.zcml``.
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component

from zope.component import handle

from zc.intid.interfaces import ISubscriberEvent


@component.adapter(ISubscriberEvent)
def subscriberEventNotify(event):
    """
    Event subscriber to dispatch
    :class:`zc.intid.interfaces.ISubscriberEvent` to interested
    adapters.

    The adapters are registered on ``event.object, event``.
    """
    handle(event.object, event)
