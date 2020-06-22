# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from collections import OrderedDict, defaultdict
import json
from os import path

import contrast
from contrast.agent.assess.policy.patch_location_policy import PatchLocationPolicy
from contrast.agent.assess.policy.propagation_node import PropagationNode
from contrast.agent.assess.policy.source_node import SourceNode
from contrast.agent.assess.rules.dataflow_rule import DataflowRule
from contrast.agent.assess.rules.non_dataflow_rule import NonDataflowRule
from contrast.agent.assess.policy_constants import (
    PROPAGATION_KEY,
    SOURCES_KEY,
    TRIGGERS_KEY,
)
from contrast.agent.assess.rules.providers.hardcoded_key import HardcodedKey
from contrast.agent.assess.rules.providers.hardcoded_password import HardcodedPassword
from contrast.agent.settings_state import SettingsState
from contrast.utils.singleton import Singleton
from contrast.utils.decorators import fail_safely

import logging

logger = logging.getLogger("contrast")


POLICY_DATA_DIR = path.join(path.dirname(contrast.__file__), "data")


class Policy(Singleton):
    POLICY_JSON_PATH = path.join(POLICY_DATA_DIR, "policy.json")

    PROVIDER_CLASSES = [HardcodedKey, HardcodedPassword]

    def init(self):
        """
        Singletons should override init, not __init__.
        """
        self.sources = []
        self.propagators = []
        self.triggers = OrderedDict()
        self.providers = OrderedDict()

        self.propagators_by_name = defaultdict(list)
        # This is used to ensure that we only ever have one PatchLocationPolicy
        # instance per patch location.
        self.policy_by_name = OrderedDict()
        # This is used to represent a list of PatchLocationPolicy instances per each
        # module. It is what enables the application of module-level import hooks.
        self.policy_by_module = OrderedDict()

        self.policy_data = {}

        if SettingsState().is_assess_enabled():
            self.initialize()

    def process_node(self, node):
        """
        Create patch location policy for node and update lookup tables if necessary
        """
        patch_policy = self.policy_by_name.setdefault(
            node.name, PatchLocationPolicy(node)
        )
        patch_policy.add_node(node)

        policy_list = self.policy_by_module.setdefault(node.module, [])
        policy_list.append(patch_policy)

        return patch_policy

    def initialize(self):
        loaded_json = self._get_json_data()
        if not loaded_json:
            return

        self.policy_data = loaded_json

        self._load_sources()
        self._load_propagators()
        self._load_triggers()

        self._load_providers()

    def _load_sources(self):
        for framework, nodes in self.policy_data[SOURCES_KEY].items():
            for value in nodes:
                source_node = SourceNode.from_dict(framework, value)
                if source_node.version_mismatch:
                    continue

                if source_node.should_apply():
                    self.sources.append(source_node)
                    self.process_node(source_node)

    def _load_propagators(self):
        for item in self.policy_data[PROPAGATION_KEY]:
            prop = PropagationNode.from_dict(item)
            if prop.version_mismatch:
                continue

            self.propagators.append(prop)
            self.propagators_by_name[prop.name].append(prop)
            self.process_node(prop)

    def _load_triggers(self):
        for item in self.policy_data[TRIGGERS_KEY]:
            is_dataflow = item.get(DataflowRule.JSON_DATAFLOW, True)
            rule_cls = DataflowRule if is_dataflow else NonDataflowRule
            rule = rule_cls.from_dict(item)
            self.triggers[rule.name] = rule
            for node in rule.nodes:
                self.process_node(node)

    def _load_providers(self):
        for item in self.PROVIDER_CLASSES:
            instance = item()

            self.providers[instance.name] = instance

    @fail_safely("Failed to read policy json file")
    def _get_json_data(self):
        with open(self.POLICY_JSON_PATH) as json_file:
            return json.load(json_file)

    @fail_safely("Failed to add node to policy")
    def add_node(self, node, node_type):
        node.validate()
        if node_type == "dynamic_source":
            self.sources.append(node)
            return self.process_node(node)
