#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions for externalizing OIDs.

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from six import string_types

from zope.security.management import system_user

from nti.externalization.externalization import choose_field

from nti.externalization.extension_points import set_external_identifiers

from nti.externalization.interfaces import StandardExternalFields
from nti.externalization.interfaces import StandardInternalFields

from nti.externalization.oids import toExternalOID

from nti.externalization.proxy import removeAllProxies

from nti.ntiids.ntiids import TYPE_OID

from nti.ntiids.ntiids import make_ntiid
from nti.ntiids.ntiids import is_ntiid_of_type
from nti.ntiids.ntiids import make_provider_safe
from nti.ntiids.ntiids import is_valid_ntiid_string

StandardExternalFields_ID = StandardExternalFields.ID
StandardExternalFields_OID = StandardExternalFields.OID
StandardExternalFields_NTIID = StandardExternalFields.NTIID

StandardInternalFields_ID = StandardInternalFields.ID
StandardInternalFields_NTIID = StandardInternalFields.NTIID

MASKED_EXTERNAL_CREATOR = 'unknown'
DEFAULT_EXTERNAL_CREATOR = system_user.id

logger = __import__('logging').getLogger(__name__)


def to_external_ntiid_oid(contained, default_oid=None,
                          add_to_connection=False,
                          add_to_intids=False,
                          mask_creator=False,
                          use_cache=True):
    """
    :return: An NTIID string utilizing the object's creator and persistent
            id.
    :param str default_oid: The default value for the externalization of the OID.
            If this is ``None`` (the default), and no external OID can be found
            (using :func:`toExternalOID`), then this function will return None.
    :param add_to_connection: If the object is persistent but not yet added to a
            connection, setting this to true will attempt to add it to the nearest
            connection in its containment tree, thus letting it have an OID.
    :keyword bool mask_creator: If true (not the default), then the actual
            creator of the object will not be present in the NTIID string.
    """
    # pylint: disable=unused-variable
    __traceback_info__ = type(contained)

    if callable(getattr(contained, 'to_external_ntiid_oid', None)):
        return contained.to_external_ntiid_oid()

    # We really want the external OID, but for those weird time we may not be saved we'll
    # allow the ID of the object, unless we are explicitly overridden
    contained = removeAllProxies(contained)

    # By definition, these are persistent.Persistent objects, so a _v_ attribute
    # is going to be volatile and thread-local (or nearly). If the object cache
    # is in use, the worst that can happen is that the third part of the OID
    # is/not around for longer/less long than otherwise. (Which could potentially differ
    # from one worker to the next).
    # On large renderings, benchmarks show this can be worth ~10%
    cache_key = str('_v_to_external_ntiid_oid_%s' % mask_creator)
    if use_cache:
        ext_oid = getattr(contained, cache_key, None)
        if ext_oid:
            return ext_oid

    oid = toExternalOID(contained,
                        default=default_oid,
                        add_to_connection=add_to_connection,
                        add_to_intids=add_to_intids,
                        use_cache=use_cache)
    if not oid:
        return None

    if mask_creator:
        creator = MASKED_EXTERNAL_CREATOR
    else:
        creator = getattr(contained, 'creator', DEFAULT_EXTERNAL_CREATOR)

    if not isinstance(creator, string_types):
        creator = getattr(creator, 'username', DEFAULT_EXTERNAL_CREATOR)

    ext_oid = make_ntiid(provider=make_provider_safe(creator),
                         specific=oid,
                         nttype=TYPE_OID)
    try:
        setattr(contained, cache_key, ext_oid)
    except (AttributeError, TypeError):  # TypeError is a BrokenModified
        pass
    return ext_oid


def setExternalIdentifiers(context, result):
    result_id = choose_field(result, context, StandardExternalFields_ID,
                             fields=(StandardInternalFields_ID, StandardExternalFields_ID))
    # As we transition over to structured IDs that contain OIDs,
    # we'll try to use that for both the ID and OID portions
    if is_ntiid_of_type(result_id, TYPE_OID):
        # If we are trying to use OIDs as IDs, it's possible that the
        # ids are in the old, version 1 format, without an intid component.
        # If that's the case, then update them on the fly, but only for notes
        # because odd things happen to other  objects (chat rooms?)
        # if we do this to them
        if context.__class__.__name__ == 'Note':
            result_id = result[StandardExternalFields_ID]
            std_oid = to_external_ntiid_oid(context)
            if std_oid and std_oid.startswith(result_id):
                result[StandardExternalFields_ID] = std_oid
        oid = result[StandardExternalFields_OID] = result[StandardExternalFields_ID]
    else:
        oid = to_external_ntiid_oid(context, default_oid=None)
        if oid:
            result[StandardExternalFields_OID] = oid

    ntiid = oid
    choose_field(result, context, StandardExternalFields_NTIID,
                 fields=(StandardInternalFields_NTIID, StandardExternalFields_NTIID))
    # During the transition, if there is not an NTIID, but we can find one as the ID or OID,
    # provide that
    if StandardExternalFields_NTIID not in result:
        for field in (StandardExternalFields_ID, StandardExternalFields_OID):
            if is_valid_ntiid_string(result.get(field)):
                ntiid = result[StandardExternalFields_NTIID] = result[field]
                break
    return (oid, ntiid)


def set_hook():
    hook = getattr(set_external_identifiers, 'sethook')
    hook(setExternalIdentifiers)
