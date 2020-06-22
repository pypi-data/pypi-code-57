# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import time

from contrast.extern.six import iteritems

from contrast.agent.assess.rules.base_rule import BaseRule as AssessBaseRule
from contrast.agent.settings_state import SettingsState
from contrast.api.settings_pb2 import (
    AgentSettings,
    ProtectionRule,
    VirtualPatchCondition,
)

from contrast.configuration import AgentConfig

import logging

logger = logging.getLogger("contrast")


class Csrf(AssessBaseRule):
    pass


SCORE_MAP = dict(LOW=1, MEDIUM=2, HIGH=3, CRITICAL=4)


class SettingsBuilder(object):
    DEFINITIONS = None

    DEFAULT_FEATURES = {
        "defend": {"enabled": True},
        "log_file": "contrast_test.log",
        "log_level": "INFO",
    }

    ASSESS_FEATURES_HASH = {"defend": {"enabled": False}, "assess": {"enabled": True}}

    DEFAULT_SETTINGS = {
        "protection_rules": [
            {
                "id": "path-traversal",
                "name": "Path Traversal",
                "mode": ProtectionRule.BLOCK,
            },
            {
                "id": "sql-injection",
                "name": "SQL Injection",
                "mode": ProtectionRule.BLOCK,
            },
            {
                "id": "reflected-xss",
                "name": "Cross-Site Scripting",
                "mode": ProtectionRule.BLOCK,
            },
            {
                "id": "xxe",
                "name": "XML External Entity Processing",
                "mode": ProtectionRule.BLOCK,
            },
        ],
        "virtual_patches": [
            {
                "name": "parameters",
                "headers": [],
                "parameters": [
                    {
                        "name": "foo",
                        "value": "bar",
                        "input_type": VirtualPatchCondition.PARAMETER,
                        "evaluation": VirtualPatchCondition.EQUALS,
                    }
                ],
                "urls": [],
                "key": "",
                "uuid": "uiop",
            },
            {
                "name": "parameters",
                "headers": [],
                "parameters": [
                    {
                        "name": "intel",
                        "value": "cpu",
                        "input_type": VirtualPatchCondition.PARAMETER,
                        "evaluation": VirtualPatchCondition.EQUALS,
                    }
                ],
                "urls": [],
                "key": "",
                "uuid": "post_uuid",
            },
            {
                "name": "headers",
                "headers": [
                    {
                        "name": "FOO",
                        "value": "bar",
                        "input_type": VirtualPatchCondition.HEADER,
                        "evaluation": VirtualPatchCondition.EQUALS,
                    }
                ],
                "parameters": [],
                "urls": [],
                "key": "",
                "uuid": "zxcv",
            },
            {
                "name": "urls",
                "headers": [],
                "parameters": [],
                "urls": [
                    {
                        "value": "test",
                        "input_type": VirtualPatchCondition.URL,
                        "evaluation": VirtualPatchCondition.CONTAINS,
                    }
                ],
                "key": "",
                "uuid": "qwer",
            },
            {
                "name": "url equals",
                "headers": [],
                "parameters": [],
                "urls": [
                    {
                        "value": "/vp_screener_endpoint/should/be/blocked",
                        "input_type": VirtualPatchCondition.URL,
                        "evaluation": VirtualPatchCondition.EQUALS,
                    }
                ],
                "key": "",
                "uuid": "derp",
            },
            {
                "name": "matches",
                "parameters": [
                    {
                        "name": "number",
                        "value": "[0-9]{3}",
                        "input_type": VirtualPatchCondition.PARAMETER,
                        "evaluation": VirtualPatchCondition.MATCHES,
                    }
                ],
                "headers": [],
                "urls": [],
                "key": "",
                "uuid": "matches-uuid",
            },
            {
                "name": "screener",
                "headers": [
                    {
                        "name": "Referrer",
                        "value": "123456789",
                        "input_type": VirtualPatchCondition.REFERER,
                        "evaluation": VirtualPatchCondition.CONTAINS,
                    }
                ],
                "parameters": [],
                "urls": [],
                "key": "",
                "uuid": "zzzz",
            },
        ],
        "disabled_assess_rules": ["test_application_disabled"],
    }

    def __init__(self):
        self._settings = None

    def settings(self, settings_dict=None, features_dict=None, defend_rules=None):
        self._settings = SettingsState(init_libs=False)
        self._settings.config = AgentConfig()

        if settings_dict or features_dict or defend_rules:
            agent_settings = self.service_response(
                settings_dict=self._defend_rule_settings(defend_rules),
                features_dict=features_dict,
            )
        else:

            agent_settings = self.service_response(
                settings_dict=self.DEFAULT_SETTINGS, features_dict=self.DEFAULT_FEATURES
            )

        self._settings.process_service_response(agent_settings)

        self._settings.set_assess_rules()
        self._settings.set_protect_rules()

        if defend_rules:
            needed_rules = [dr["id"] for dr in defend_rules]

            self._settings.defend_rules = {
                k: v
                for k, v in iteritems(self._settings.defend_rules)
                if k in needed_rules
            }

        return self._settings

    def build(self, settings_dict=None, features_dict=None, defend_rules=None):
        return self.settings(
            settings_dict=settings_dict,
            features_dict=features_dict,
            defend_rules=defend_rules,
        )

    def build_assess(self):
        settings = self.settings(features_dict=self.ASSESS_FEATURES_HASH)
        settings.server_features.defend.enabled = False
        settings.server_features.assess.enabled = True

        settings.config.put("assess.enable", True)
        settings.config.put("protect.enable", False)

        return settings

    def service_response(self, settings_dict=None, features_dict=None):
        obj = AgentSettings()
        obj.sent_ms = int(time.time() * 1000)

        SettingsBuilder.populate_from_dict(
            obj.server_features,
            features_dict if features_dict else self.DEFAULT_FEATURES,
        )

        SettingsBuilder.populate_from_dict(
            obj.application_settings,
            settings_dict if settings_dict else self.DEFAULT_SETTINGS,
        )

        return obj

    def build_assess_rules(self):
        self._settings.build_assess_rules()
        self._settings.assess_rules = {"csrf": Csrf(self._settings)}

    def _defend_rule_settings(self, defend_rules=None):
        if defend_rules:
            return {
                "protection_rules": [
                    SettingsBuilder._defend_rule_entry(rule) for rule in defend_rules
                ]
            }

        return self.DEFAULT_SETTINGS

    @staticmethod
    def _defend_rule_entry(rule):
        if isinstance(rule, dict):
            return rule

        return {"id": str(rule), "name": str(rule), "mode": ProtectionRule.BLOCK}

    @staticmethod
    def populate_from_dict(pb, values):
        """
        Initialize the given protobuf instance from a python dictionary
        """
        for key, value in iteritems(values):
            if isinstance(value, dict):
                SettingsBuilder.populate_from_dict(getattr(pb, key), value)
            elif isinstance(value, list):
                SettingsBuilder.populate_from_list(getattr(pb, key), value)
            else:
                try:
                    setattr(pb, key, value)
                except AttributeError:
                    logger.error(
                        "Unable to set protobuf instance %s : %s=%s",
                        type(pb),
                        key,
                        value,
                    )

        return pb

    @staticmethod
    def populate_from_list(pb, values):
        """
        Initialize the given protobuf instance from a python list
        """
        if len(values) > 0:
            if isinstance(values[0], dict):
                for value in values:
                    child = pb.add()
                    SettingsBuilder.populate_from_dict(child, value)
            else:
                pb.extend(values)
