# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.protect.rule.xxe_rule import Xxe
from contrast.utils.decorators import fail_safely

import logging

logger = logging.getLogger("contrast")


@fail_safely("Failed to run protect XXE Rule")
def apply_rule(context, framework, xml):
    if not xml or not framework:
        return

    from contrast.agent.settings_state import SettingsState

    rule = SettingsState().defend_rules[Xxe.NAME]

    if not rule or not rule.enabled:
        return

    rule.infilter(context, xml, framework=framework)
