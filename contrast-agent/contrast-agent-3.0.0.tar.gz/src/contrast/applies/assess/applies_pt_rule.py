# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent import scope
from contrast.agent.assess.policy import Policy
from contrast.agent.assess.policy.trigger_policy import TriggerPolicy
from contrast.utils.decorators import fail_safely


@fail_safely("Error running path traversal assess rule")
def apply_rule(module, method, result, args, kwargs):
    policy = Policy()
    trigger_rule = policy.triggers["path-traversal"]

    trigger_nodes = trigger_rule.find_trigger_nodes(module, method)

    with scope.trigger_scope():
        TriggerPolicy.apply(trigger_rule, trigger_nodes, result, args, kwargs)
