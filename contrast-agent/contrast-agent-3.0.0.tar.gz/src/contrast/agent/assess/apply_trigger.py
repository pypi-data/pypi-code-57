# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import re

from contrast.extern.six import iteritems, string_types

from contrast.agent.assess.contrast_event import ContrastEvent
from contrast.agent.assess.properties import Properties
from contrast.agent.assess.utils import get_properties
from contrast.agent.settings_state import SettingsState
from contrast.utils.assess.duck_utils import is_iterable, safe_iterator

import logging

logger = logging.getLogger("contrast")


def cs__apply_trigger(
    context, rule, node, orig_source, self_obj, ret, possible_key, args, kwargs
):
    if not context or not node:
        return

    if rule.disabled:
        return

    source = rule.extract_source(node, orig_source)

    if rule.dataflow and source is None:
        return

    if not node.dataflow_rule:
        if node.good_value:
            if not isinstance(source, string_types) or re.match(
                node.good_value, source
            ):
                return
        elif node.bad_value:
            if not isinstance(source, string_types) or not re.match(
                node.bad_value, source
            ):
                return

        build_finding(
            context, rule, node, orig_source, self_obj, ret, None, args, kwargs
        )

        return

    if rule.is_violated(node, source):
        build_finding(
            context, rule, node, orig_source, self_obj, ret, possible_key, args, kwargs
        )

    elif isinstance(source, dict):
        for key, value in iteritems(source):
            cs__apply_trigger(
                context, rule, node, key, self_obj, ret, None, args, kwargs
            )
            cs__apply_trigger(
                context, rule, node, value, self_obj, ret, key, args, kwargs
            )

    elif is_iterable(source):
        for value in safe_iterator(source):
            cs__apply_trigger(
                context, rule, node, value, self_obj, ret, None, args, kwargs
            )


def build_finding(
    context,
    rule,
    node,
    target,
    self_obj,
    ret,
    possible_key,
    args,
    kwargs,
    target_properties=None,
    frame=None,
):
    """
    Builds a finding and appends it to the current context

    :param context: current RequestContext
    :param rule: TriggerRule that was violated
    :param node: Weaver that was used to identify the source
    :param target: tracked item that triggered the rule
    :param self_obj: object of the the called node method ; could be None if it was a module-level function
    :param ret: return of the policy method
    :param possible_key: possible key of the value in the kwarg
    :param args: tuple of methods arguments
    :param kwargs: dictionary of methods keyword arguments
    :return: None
    """
    events = []
    properties = {}

    if target is not None and target_properties is None:
        # If the target is a stream that is being treated as a source, then we
        # build a new Properties object for it and add the stream's source
        # event to it. In this case the stream object itself is actually
        # triggering the rule, which means that no data was necessarily read
        # from the stream before triggering the rule.
        if getattr(target, "cs__source", False):
            target_properties = Properties(target)
            target_properties.add_event(target.cs__source_event)
        elif getattr(target, "cs__tracked", False):
            target_properties = target.cs__properties
        else:
            target_properties = get_properties(target)

    if target_properties is not None:
        events = [event.to_dtm_event() for event in target_properties.events]

        target_props = target_properties.properties
        if target_props:
            for key, value in iteritems(target_props):
                properties[key] = value

    parent_ids = (
        [target_properties.events[-1].event_id]
        if target_properties and target_properties.events
        else []
    )
    contrast_event = ContrastEvent(
        node, target, self_obj, ret, args, kwargs, parent_ids, possible_key, frame=frame
    ).to_dtm_event()

    events.append(contrast_event)

    if rule.dataflow:
        finding = rule.create_finding(properties, events=events)
    else:
        finding = rule.create_finding(properties, source=target)
        finding.events.extend(events)

    # if after creating the finding, we discover that this finding already exists
    # in context.activity, then do not add it and return early
    for curr_finding in context.activity.findings:
        if finding.hash_code == curr_finding.hash_code:
            return

    context.activity.findings.extend([finding])

    settings = SettingsState()
    context.activity.finding_tags = settings.config.get("assess.tags", "")
    logger.debug(
        "Trigger %s detected: %s triggered %s", node.name, str(id(target)), rule.name
    )
