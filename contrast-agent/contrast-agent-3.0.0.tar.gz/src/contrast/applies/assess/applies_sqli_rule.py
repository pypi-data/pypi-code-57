# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
NOTE: This API is deprecated in favor of the one provided by
contrast.applies.sqli. It should be removed once all SQL patches have been
updated to use the new rule.
"""
from contrast.agent.assess.apply_trigger import cs__apply_trigger
from contrast.agent.assess.policy import Policy
from contrast.utils.decorators import fail_safely


@fail_safely("Error running SQLi assess rule")
def apply_rule(context, database, action, sql, self_obj, result, args, kwargs):
    if sql is None:
        return

    context.activity.query_count += 1
    context.activity.technologies[database] = True

    policy = Policy()

    sqli_trigger_rule = policy.triggers["sql-injection"]

    trigger_nodes = sqli_trigger_rule.find_trigger_nodes(database, action)

    if not trigger_nodes:
        return

    cs__apply_trigger(
        context,
        sqli_trigger_rule,
        trigger_nodes[0],
        sql,
        self_obj,
        result,
        None,
        args,
        kwargs,
    )
