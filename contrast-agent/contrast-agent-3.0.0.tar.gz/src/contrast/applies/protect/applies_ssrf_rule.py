# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast
from contrast.agent.protect.rule.ssrf_rule import Ssrf
from contrast.utils.decorators import fail_safely

import logging

logger = logging.getLogger("contrast")


@fail_safely("Failed to run protect SSRF Rule")
def apply_rule(new_request):
    if not new_request:
        return

    context = contrast.CS__CONTEXT_TRACKER.current()

    if not context:
        return

    from contrast.agent.settings_state import SettingsState

    rule = SettingsState().defend_rules[Ssrf.NAME]

    if not rule or not rule.enabled:
        return

    rule.infilter(context, new_request)
