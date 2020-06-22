# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import re

from contrast.agent.assess.adjusted_span import AdjustedSpan
from contrast.agent.assess.policy.propagation_node import PropagationNode
from contrast.agent.assess.utils import (
    build_preshift,
    copy_events,
    copy_tags_in_span,
    copy_tags_to_offset,
    get_properties,
    get_last_event_id,
    track_string,
    update_properties,
)

from contrast.extern.functools_lru_cache import lru_cache

from .split_propagator import SplitPropagator


@lru_cache(maxsize=10)
def get_regex_policy_node(method_name):

    group_node = PropagationNode(
        "re", "Match", True, "group", "OBJ", "RETURN", "REGEX_GROUP"
    )
    groups_node = PropagationNode(
        "re", "Match", True, "groups", "OBJ", "RETURN", "REGEX_GROUP"
    )
    groupdict_node = PropagationNode(
        "re", "Match", True, "groupdict", "OBJ", "RETURN", "REGEX_GROUP"
    )

    node_map = dict(group=group_node, groups=groups_node, groupdict=groupdict_node)
    return node_map.get(method_name)


def propagate_group_string(
    method_name, target, source_properties, span, preshift, retval
):

    policy_node = get_regex_policy_node(method_name)
    if policy_node is None:
        return

    target_properties = copy_tags_in_span(target, source_properties, span)

    parent_ids = [get_last_event_id(source_properties)]

    copy_events(target_properties, source_properties)

    target_properties.build_event(
        policy_node,
        target,
        preshift.obj,
        retval,
        preshift.args,
        preshift.kwargs,
        parent_ids,
    )


def propagate_group(self_obj, target, *args):
    """
    Propagator for re.Match.group()

    self_obj:
        re.Match object
    target:
        str result of calling .group()
    """
    source_properties = get_properties(self_obj.string)
    if source_properties is None:
        return

    # If no args are given, we simply process the 0th group, which is the
    # match for the entire pattern.
    if not args:
        args = [0]

    # If fewer than two args are given, the result is a single string match.
    # Otherwise, the result is an iterable of strings.
    if len(args) < 2:
        target = [target]

    preshift = build_preshift(self_obj.string, args, {})

    for string, group in zip(target, args):
        propagate_group_string(
            "group", string, source_properties, self_obj.span(group), preshift, target
        )


def propagate_groups(self_obj, target, *args):
    """
    Propagator for re.Match.groups()

    self_obj:
        re.Match object
    target:
        tuple of str objects; result of calling .group()
    """
    # If there were no groups, this will be an empty tuple
    if not target:
        return

    source_properties = get_properties(self_obj.string)
    if source_properties is None:
        return

    preshift = build_preshift(self_obj.string, args, {})

    for string, span in zip(target, self_obj.regs[1:]):
        propagate_group_string(
            "groups", string, source_properties, span, preshift, target
        )


def propagate_groupdict(self_obj, target, *args):
    """
    Propagator for re.Match.groupdict()

    self_obj:
        re.Match object
    target:
        dict with group names as keys and matched strings as values
    """
    # If there were no named groups, this will be an empty tuple
    if not target:
        return

    source_properties = get_properties(self_obj.string)
    if source_properties is None:
        return

    preshift = build_preshift(self_obj.string, args, {})

    for name, value in target.items():
        propagate_group_string(
            "groupdict", value, source_properties, self_obj.span(name), preshift, target
        )


def propagate_sub_tags(
    target_properties,
    orig_properties,
    repl_properties,
    string,
    count,
    source_matches,
    repl_results,
):

    source_offset = 0
    target_offset = 0

    for i in range(count):
        match = source_matches[i]
        # Copy any tags from the source string prior to the match
        if orig_properties is not None:
            span = AdjustedSpan(source_offset, match.start())
            source_tags = orig_properties.tags_at_range(span)
            copy_tags_to_offset(target_properties, source_tags, target_offset)

        target_offset += match.start() - source_offset
        source_offset = match.end()

        # Copy any tags from the replacement string
        if repl_properties[i] is not None:
            copy_tags_to_offset(
                target_properties, repl_properties[i].tags, target_offset
            )

        target_offset += len(repl_results[i])

    if source_offset < len(string) and orig_properties is not None:
        old_span = AdjustedSpan(source_offset, len(string))
        source_tags = orig_properties.tags_at_range(old_span)
        copy_tags_to_offset(target_properties, source_tags, target_offset)


def propagate_sub_events(
    target_properties,
    orig_properties,
    repl_properties,
    target,
    args,
    kwargs,
    method_name,
):

    parent_ids = []
    if orig_properties is not None:
        parent_ids.append(get_last_event_id(orig_properties))

    copy_events(target_properties, orig_properties)

    for props in repl_properties:
        copy_events(target_properties, props)
        if props is not None:
            parent_ids.append(get_last_event_id(props))

    node = PropagationNode(
        "re", "", False, method_name, "ARG_1,ARG_2", "RETURN", "REGEX_SUB"
    )
    target_properties.build_event(node, target, None, target, args, kwargs, parent_ids)


def propagate_sub(
    target, repl_results, pattern, repl, string, count, flags, method_name
):
    """
    Propagator for re.sub and re.subn
    """
    source_matches = list(re.finditer(pattern, string, flags))
    # No propagation necessary because no replacement occurred
    if len(source_matches) == 0:
        return

    if count > 0:
        count = min(len(source_matches), count)
    else:
        count = len(source_matches)

    # If the repl was not a callable, then the replacement string is the same
    # for each occurrence of the pattern
    if repl_results is None:
        repl_results = [repl] * len(source_matches)

    orig_properties = get_properties(string)
    repl_properties = [get_properties(x) for x in repl_results]
    if orig_properties is None and not any(repl_properties):
        return

    target_properties = get_properties(target) or track_string(target)

    propagate_sub_tags(
        target_properties,
        orig_properties,
        repl_properties,
        string,
        count,
        source_matches,
        repl_results,
    )

    args = (pattern, repl, string)
    kwargs = dict(count=count, flags=flags)
    propagate_sub_events(
        target_properties,
        orig_properties,
        repl_properties,
        target,
        args,
        kwargs,
        method_name,
    )

    target_properties.cleanup_tags()
    update_properties(target, target_properties)


class RegexSplitPropagator(SplitPropagator):
    @property
    def needs_propagation(self):
        if not self.preshift:
            return False

        return self.any_source_tracked

    def _get_flags(self):
        if len(self.preshift.args) == 4:
            return self.preshift.args[-1]
        return self.preshift.kwargs.get("flags", 0)

    def propagate(self):
        pattern, string = self.preshift.args[:2]
        flags = self._get_flags()

        source_properties = get_properties(string)
        if source_properties is None:
            return

        source_offset = 0
        target_index = 0

        while target_index < len(self.target):
            # If the pattern passed to re.split contains any groupings, then
            # those groupings need to be propagated appropriately.
            match = re.match(pattern, string[source_offset:], flags=flags)
            if match is not None:
                for target, span in zip(self.target[target_index:], match.regs[1:]):
                    target_properties = copy_tags_in_span(
                        target, source_properties, span, offset=source_offset
                    )
                    copy_events(target_properties, source_properties)
                    target_index += 1
                source_offset += len(match.group())

            target = self.target[target_index]
            span = (source_offset, source_offset + len(target))
            target_properties = copy_tags_in_span(target, source_properties, span)
            copy_events(target_properties, source_properties)

            source_offset += len(target)
            target_index += 1
