# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast
from contrast.agent import scope
from contrast.agent.assess.policy.methods import skip_analysis
from contrast.agent.settings_state import SettingsState
from contrast.applies.assess.applies_nosqli_rule import apply_rule as assess_rule
from contrast.applies.protect.applies_nosqli_rule import apply_rule as protect_rule


def apply_rule(database, action, orig_func, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()

    query = None
    if args:
        query = args[0]

    if context is not None and SettingsState().is_protect_enabled():
        protect_rule(database, action, query)

    try:
        result = orig_func(*args, **kwargs)
    except Exception:
        result = None
        raise
    finally:
        if not skip_analysis(context):
            with scope.contrast_scope():
                assess_rule(context, database, action, query, result, args, kwargs)

    return result
