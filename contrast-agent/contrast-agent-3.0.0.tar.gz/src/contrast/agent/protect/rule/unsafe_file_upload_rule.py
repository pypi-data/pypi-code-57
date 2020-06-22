# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.protect.rule.base_rule import BaseRule
from contrast.api.settings_pb2 import ProtectionRule


class UnsafeFileUpload(BaseRule):
    """
    Unsafe File Upload rule to protect against potentially malicious
    files that get uploaded
    """

    NAME = "unsafe-file-upload"

    def __init__(self, settings):
        BaseRule.__init__(self, settings)

    @property
    def mode(self):
        return ProtectionRule.BLOCK_AT_PERIMETER
