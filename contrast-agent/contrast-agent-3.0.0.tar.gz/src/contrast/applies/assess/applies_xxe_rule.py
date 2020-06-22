# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent import scope
from contrast.agent.assess.policy import Policy
from contrast.agent.assess.policy.trigger_policy import TriggerPolicy
from contrast.utils.decorators import fail_safely

import logging

logger = logging.getLogger("contrast")

XXE_RULE = "xxe"


@fail_safely("Error running XXE assess rule")
def apply_rule(module, method, result, args, kwargs):
    policy = Policy()
    trigger_rule = policy.triggers.get(XXE_RULE)

    if not trigger_rule:
        return

    trigger_nodes = trigger_rule.find_trigger_nodes(module, method)

    with scope.trigger_scope():
        TriggerPolicy.apply(trigger_rule, trigger_nodes, result, args, kwargs)
