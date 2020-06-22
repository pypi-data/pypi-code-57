# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.apply_trigger import cs__apply_trigger
from contrast.agent.assess.policy import Policy
from contrast.utils.decorators import fail_safely


@fail_safely("Error running NoSQLi assess rule")
def apply_rule(context, database, action, sql, result, args, kwargs):
    if sql is None:
        return

    context.activity.query_count += 1
    context.activity.technologies[database] = True

    policy = Policy()

    nosqli_trigger_rule = policy.triggers["nosql-injection"]

    # TODO: refactor this applicator to handle multiple rules
    trigger_nodes = nosqli_trigger_rule.find_trigger_nodes(database, action)

    if not trigger_nodes:
        return

    cs__apply_trigger(
        context,
        nosqli_trigger_rule,
        trigger_nodes[0],
        sql,
        None,
        result,
        None,
        args,
        kwargs,
    )
