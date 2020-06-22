# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.six import integer_types

import contrast
from contrast.agent.assess.adjusted_span import AdjustedSpan
from contrast.agent.assess.policy_constants import OBJECT, RETURN
from contrast.utils.assess.duck_utils import safe_obj_length
from contrast.utils.assess.tag_utils import merge_tags


def build_preshift(self_obj, args=None, kwargs=None):
    """
    self_obj: self
    args: arguments in method
    kwargs: keyword arguments in method
    """
    # Avoid circular import from policy module
    from contrast.agent.assess.policy.preshift import Preshift

    preshift = Preshift()
    preshift.obj = self_obj
    preshift.obj_length = safe_obj_length(self_obj)
    preshift.args = args or []
    preshift.arg_lengths = [safe_obj_length(value) for value in preshift.args]
    preshift.kwargs = kwargs or {}

    return preshift


def get_properties(value):
    return contrast.STRING_TRACKER.get(value, None)


def update_properties(value, properties):
    contrast.STRING_TRACKER.update_properties(value, properties)


def clear_properties():
    contrast.STRING_TRACKER.clear()


def cs__tracked(value):
    props = get_properties(value)
    return props is not None and props.is_tracked()


def track_string(value):
    return contrast.STRING_TRACKER.track(value)


def in_string_tracker(value):
    return value in contrast.STRING_TRACKER


def cs__reset_properties(value):
    from contrast.agent.assess.properties import Properties

    contrast.STRING_TRACKER.__setitem__(value, Properties(value))


def copy_events(target_props, source_props):
    if source_props is None or target_props is source_props:
        return

    for event in source_props.events:
        target_props.events.append(event)


def cs__copy_from(value, self_obj, shift=0, skip_tags=None):
    if self_obj is value:
        return

    # TODO make sure tracked later
    if not cs__tracked(self_obj):
        return

    obj_props = get_properties(self_obj)
    self_props = get_properties(value)

    if obj_props == self_props:
        cs__reset_properties(value)

    copy_events(self_props, obj_props)

    for key in obj_props.tag_keys():
        if skip_tags and key in skip_tags:
            continue

        new_tags = []

        obj_props_tags = obj_props.fetch_tags(key)

        for tag in obj_props_tags:
            new_tags.append(tag.copy_modified(shift))

        existing_tags = self_props.fetch_tags(key)

        if existing_tags:
            existing_tags.extend(new_tags)
        else:
            self_props.set_tag(key, new_tags)


def cs__splat_tags(value, ret, source=None):
    if source is None:
        source = value

    length = len(ret)

    for key in get_properties(source).tag_keys():

        existing_props = get_properties(ret)

        if not existing_props:
            continue

        existing_tags = existing_props.fetch_tags(key)

        if existing_tags and len(existing_tags) > 1:
            del existing_tags[len(existing_tags) - 1]

            span = existing_tags[0]

            span.repurpose(0, length)
        else:
            span = AdjustedSpan(0, length)

            ret_properties = get_properties(ret)
            ret_properties.add_tag(key, span)

            update_properties(ret, ret_properties)

        if not cs__tracked(ret):
            return


def value_of_source(source, self_obj, ret, args, kwargs):
    if source == OBJECT:
        return self_obj

    if source == RETURN:
        return ret

    if not args:
        return self_obj

    if args and isinstance(source, integer_types) and source < len(args):
        return args[source]

    if kwargs and source in kwargs:
        return kwargs[source]

    return


def cs__apply_tags(node, target, span=None):
    target_properties = get_properties(target)
    if not target_properties:
        return

    span = span or AdjustedSpan(0, len(target))
    for tag in node.tags:
        target_properties.add_tag(tag, span)


def cs__apply_untags(node, target):
    target_properties = get_properties(target)

    if target_properties:
        for tag in node.untags:
            target_properties.delete_tag(tag)


def get_self_for_method(patch_policy, args):
    """
    Retrieves self for a method's PatchLocationPolicy,

    If any node in the policy has a False instance_method attribute return None
    """
    for node in patch_policy.all_nodes():
        if not node.instance_method:
            return None

    return args[0] if args else None


def get_last_event_id(source_properties):
    if source_properties.events and source_properties.events[-1]:
        last_event = source_properties.events[-1]
        return last_event.event_id
    return None


def get_last_event_ids_from_sources(sources):
    """
    Gathers from given sources the parent IDs that should be used for an event
    """
    id_list = []

    for source in sources:
        source_properties = get_properties(source)
        if source_properties is None:
            continue

        event_id = get_last_event_id(source_properties)
        if event_id is not None and event_id not in id_list:
            id_list.append(event_id)

    return id_list


def copy_tags_in_span(target, source_properties, span, offset=0):
    """
    Given source properties, copies tags at a given span to the target
    """
    span = AdjustedSpan(*tuple(x + offset for x in span))
    source_tags = source_properties.tags_at_range(span)
    if not source_tags:
        return get_properties(target)

    target_properties = track_string(target)
    if target_properties is None:
        return get_properties(target)

    for name, tags in source_tags.items():
        for tag in tags:
            target_properties.add_existing_tag(name, tag)

    merge_tags(target_properties.tags)
    update_properties(target, target_properties)
    return target_properties


def copy_tags_to_offset(target_properties, source_tags, target_offset):
    """
    Given source tags, copy to target properties at offset.

    The caller is responsible for updating the string tracker if necessary.
    """
    for name, tags in source_tags.items():
        for tag in tags:
            new_tag = tag.copy_modified(target_offset)
            target_properties.add_existing_tag(name, new_tag)
