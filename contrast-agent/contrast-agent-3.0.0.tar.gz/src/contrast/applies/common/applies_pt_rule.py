# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast
from contrast.agent import scope
from contrast.agent.assess.policy.methods import skip_analysis
from contrast.agent.settings_state import SettingsState
from contrast.applies.protect.applies_pt_rule import apply_rule as protect_rule
from contrast.applies.assess.applies_pt_rule import apply_rule as assess_rule


MODULE_IO = "io"
MODULE_BUILTIN = "BUILTIN"
METHOD_OPEN = "open"


def apply_rule(module, method, orig_func, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()

    if context is not None and SettingsState().is_protect_enabled():
        protect_rule(context, method, args, kwargs)

    try:
        result = orig_func(*args, **kwargs)
    except Exception:
        result = None
        raise
    finally:
        if not skip_analysis(context):
            with scope.contrast_scope():
                assess_rule(module, method, result, args, kwargs)

    return result
