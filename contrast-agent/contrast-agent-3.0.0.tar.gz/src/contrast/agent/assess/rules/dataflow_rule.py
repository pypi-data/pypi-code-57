# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.trigger_rule import TriggerRule


class DataflowRule(TriggerRule):
    """
    Rule class used for all dataflow rules. Hash computation includes events.
    """

    def create_finding(self, properties, events=None):
        finding = super(TriggerRule, self).create_finding(properties, events=events)

        if events is not None:
            finding.events.extend(events)

        return finding

    def update_preflight_hash(self, hasher, events=None):
        """
        This gets called from `create_finding` in the base class

        It turns out that only three things differentiate dataflow findings:
            1. The name of the rule that was triggered
            2. The name and type of the source event(s)
            3. The request context

        Information from the current request is used to update the hash at the
        end of the request lifecycle in middleware.
        """
        for event in events or []:
            for source in event.event_sources:
                hasher.update(source.type)
                hasher.update(source.name)
