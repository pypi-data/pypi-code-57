# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from copy import copy
from contrast.extern.six import iteritems

from contrast.agent.assess.tag import ABOVE, BELOW, HIGH_SPAN, LOW_SPAN, WITHIN, WITHOUT


def intersection(tags, tag_ranges):
    """
    Return a list of tags trimmed down to the specified tag ranges.
    If a single tag has intersections with several ranges, the tag is split
    into the appropriate number of new tags.

    To clarify, for each tag in tags, we find its intersection with each
    tag in tag_ranges and combine those results.
    """
    if not tags:
        return []

    result = []
    for tag in tags:
        parts = []
        if tag.length <= 0:
            continue
        for tag_range in tag_ranges:
            new_tag = copy(tag)
            if new_tag.intersect(tag_range):
                parts.append(new_tag)
        if len(parts) > 0:
            result.extend(combine(parts))

    return result


def is_covered(remaining_ranges, tag_ranges):
    if not remaining_ranges:
        return True

    tag = remaining_ranges[0]

    for item in tag_ranges:

        if tag.length <= 0:
            break

        comparison = tag.compare_range(item.start_index, item.end_index)

        if comparison in [BELOW, LOW_SPAN, WITHOUT]:
            return False

        if comparison == WITHIN:
            tag.set_start(0)
            tag.set_end(0)
        elif comparison == HIGH_SPAN:
            tag.set_start(item.end_index)
        elif comparison == ABOVE:
            continue

    if tag.length > 0:
        return False

    remaining_ranges.pop(0)

    return is_covered(remaining_ranges, tag_ranges)


def ordered_merge(tag_array, new_tag_array):
    if isinstance(new_tag_array, list):

        if not new_tag_array:
            return tag_array

        if not tag_array:
            return new_tag_array

        for new_item in new_tag_array:
            _ordered_merge(tag_array, new_item)

    else:
        if not new_tag_array:
            return tag_array

        if not tag_array:
            return [new_tag_array]

        _ordered_merge(tag_array, new_tag_array)

    return combine(tag_array)


def merge_tags(tags):
    if isinstance(tags, dict):
        for key, value in iteritems(tags):
            tags[key] = combine(value)
    else:
        # tags is list
        return combine(tags)


def _ordered_merge(tag_array, new_item):
    index = 0

    for existing in tag_array:

        if existing.start_index >= new_item.start_index:
            break

        if existing.overlaps(new_item):
            existing.merge(new_item)
            return

        index = index + 1

    tag_array.insert(index, new_item)

    return tag_array


def combine(tags):
    if not tags:
        return tags

    current = tags[0]
    combined = [current]

    for tag in tags[1:]:
        if tag.start_index <= current.end_index:
            if tag.end_index > current.end_index:
                current.set_end(tag.end_index)
        else:
            current = tag
            combined.append(current)

    tags = combined

    return tags
