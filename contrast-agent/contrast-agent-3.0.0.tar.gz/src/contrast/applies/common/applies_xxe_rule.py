# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern import six

import contrast
from contrast.agent import scope
from contrast.agent.assess.policy.methods import skip_analysis
from contrast.agent.settings_state import SettingsState
from contrast.applies.assess.applies_xxe_rule import apply_rule as assess_rule
from contrast.applies.protect.applies_xxe_rule import apply_rule as protect_rule

VALID_TYPES = six.string_types + (six.binary_type, list, tuple)

METHOD_TO_KWARG_MAP = {"fromstring": "text", "parseString": "string"}


def apply_rule(module, method, orig_func, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()

    xml = get_user_input(method, args, kwargs)

    if context is not None and SettingsState().is_protect_enabled():
        protect_rule(context, module, xml)

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


def get_user_input(method, args, kwargs):
    if args:
        return args[0]
    if kwargs:
        kwarg = METHOD_TO_KWARG_MAP[method]
        return kwargs.get(kwarg)
