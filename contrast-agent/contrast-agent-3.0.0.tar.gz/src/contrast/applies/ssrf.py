# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast
from contrast.agent import scope
from contrast.agent.assess.policy import Policy
from contrast.agent.assess.policy.methods import skip_analysis
from contrast.agent.assess.policy.trigger_policy import TriggerPolicy
from contrast.agent.settings_state import SettingsState
from contrast.applies.protect.applies_ssrf_rule import apply_rule as protect_rule
from contrast.utils.decorators import fail_safely


@fail_safely("Error running SSRF assess rule")
def assess_rule(class_name, method_name, result, args, kwargs):
    policy = Policy()

    rule = policy.triggers["ssrf"]
    trigger_nodes = rule.find_trigger_nodes(class_name, method_name)

    with scope.contrast_scope():
        TriggerPolicy.apply(rule, trigger_nodes, result, args, kwargs)


def apply_rule(class_name, method_name, orig_func, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()

    if context is not None and SettingsState().is_protect_enabled() and len(args) > 2:
        from contrast.extern.six.moves import http_client as httplib

        connection = args[0]

        if isinstance(connection, httplib.HTTPSConnection):
            url = "https://" + connection.host + args[2]
        elif isinstance(connection, httplib.HTTPConnection):
            url = "http://" + connection.host + args[2]
        else:
            url = connection.host + args[2]

        protect_rule(url)

    try:
        result = orig_func(*args, **kwargs)
    except Exception:
        result = None
        raise
    finally:
        if not skip_analysis(context):
            assess_rule(class_name, method_name, result, args, kwargs)

    return result
