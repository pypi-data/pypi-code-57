# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""Central location for commonly used mocks"""
import mock

from contrast.agent.assess.apply_trigger import build_finding
from contrast.agent.assess.policy.trigger_policy import TriggerPolicy

apply_trigger = mock.patch(
    "contrast.agent.assess.policy.trigger_policy.TriggerPolicy.apply",
    side_effect=TriggerPolicy.apply,
)
build_finding = mock.patch(
    "contrast.agent.assess.apply_trigger.build_finding", side_effect=build_finding
)
