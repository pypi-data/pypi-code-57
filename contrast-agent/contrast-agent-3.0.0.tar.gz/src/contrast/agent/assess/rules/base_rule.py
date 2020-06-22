# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.six import iteritems

from contrast.agent.settings_state import SettingsState
from contrast.agent.assess.policy_constants import CURRENT_FINDING_VERSION
from contrast.api.dtm_pb2 import Finding
from contrast.utils.digest_utils import Digest
from contrast.utils.string_utils import protobuf_safe

import logging

logger = logging.getLogger("contrast")


class BaseRule(object):
    """
    Base rule object that all assess rules will inherit
    """

    @property
    def name(self):
        return "assess-base-rule"

    @property
    def disabled(self):
        """
        Property indicating whether rule is disabled

        A rule is disabled if either of the following is true:
            1. The rule name is listed under `assess.rules.disabled_rules` in the config
            2. The rule is listed as disabled in application settings from teamserver
        """
        settings = SettingsState()

        disabled_rules = settings.config.get("assess.rules.disabled_rules", None)

        if disabled_rules is None:
            disabled_rules = settings.application_settings.disabled_assess_rules

        return bool(disabled_rules) and self.name in disabled_rules

    def create_finding(self, properties, **kwargs):
        """
        Build finding with properties and rule-specific data

        @param properties: Properties belonging to object that triggered finding
        @param **kwargs: Placeholder for keyword args used by child classes
        """
        settings = SettingsState()

        finding = Finding()
        finding.rule_id = protobuf_safe(self.name)
        finding.version = CURRENT_FINDING_VERSION
        finding.session_id = settings.session_id

        for key, value in iteritems(properties):
            finding.properties[key] = value

        hash_code = self._generate_preflight_hash(**kwargs)

        finding.hash_code = hash_code
        finding.preflight = ",".join([self.name, hash_code])

        logger.debug("Created finding for %s", self.name)
        logger.debug("initial preflight value: %s", finding.preflight)

        return finding

    def _generate_preflight_hash(self, **kwargs):
        hasher = Digest()
        hasher.update(self.name)

        self.update_preflight_hash(hasher, **kwargs)

        return hasher.finish()

    def update_preflight_hash(self, hasher, **kwargs):
        """
        Update preflight hash with additional rule-specific data

        Child classes should override this method in order to customize the
        kind of data that is used to generate the preflight hash.

        @param hasher: Hash class to be updated with additional data
        @param **kwargs: Placeholder for keyword args used by child classes
        """
        raise NotImplementedError
