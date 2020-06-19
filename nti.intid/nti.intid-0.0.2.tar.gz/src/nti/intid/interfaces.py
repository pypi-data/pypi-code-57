#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interfaces for working with integer IDs.
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zc.intid.interfaces import IIntIdsSubclass
from zc.intid.interfaces import IIntIds as IZCIIntIds

from zope.location.interfaces import IContained

import zope.deferredimport
zope.deferredimport.initialize()
zope.deferredimport.deprecated(
    "Import from zope.intid.interfaces instead",
    IntIdMissingError='zope.intid.interfaces:IntIdMissingError',
    ObjectMissingError='zope.intid.interfaces:ObjectMissingError')

zope.deferredimport.deprecated(
    "Import from zc.intid.interfaces instead",
    IntIdAlreadyInUseError='zc.intid.interfaces:IntIdInUseError',
    IIntIdEvent='zc.intid.interfaces:ISubscriberEvent',
    IIntIdAddedEvent='zc.intid.interfaces:IAfterIdAddedEvent',
    IIntIdRemovedEvent='zc.intid.interfaces:IBeforeIdRemovedEvent',
    IntIdAddedEvent='zc.intid.interfaces:AfterIdAddedEvent',
    IntIdRemovedEvent='zc.intid.interfaces:BeforeIdRemovedEvent')

# pylint:disable=no-method-argument,no-self-argument

class IIntIds(IZCIIntIds, IIntIdsSubclass, IContained):
    """
    Advanced extensions to an integer ID catalog.

    Normal users will have no need of this interface.
    """

    def randomize():
        """
        Randomize the next id.

        Do not use this method.
        """

    def force_register(uid, ob, check=True):
        """
        Register an object.

        Do not use this method.

        :param uid: Registration id
        :param ob: Object to register
        :param check: Validation check flag
        """

    def force_unregister(uid, ob=None, notify=False, remove_attribute=True):
        """
        Unregister an object.

        Do not use this method.

        :param uid: Id to unregister
        :param ob: Obj to unregister [optional]
        :param notify: Flag to trigger an ``IIdRemovedEvent``
        :param notremove_attribute: Flag to remove intid attribute
        """
