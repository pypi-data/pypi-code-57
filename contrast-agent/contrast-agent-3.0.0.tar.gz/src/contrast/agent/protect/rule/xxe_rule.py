# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import re

from contrast.agent.protect.rule.base_rule import BaseRule
from contrast.agent.protect.rule.xxe.entity_wrapper import EntityWrapper
from contrast.api.dtm_pb2 import RaspRuleSample, UserInput, XxeMatch, XxeWrapper
from contrast.utils.stack_trace_utils import StackTraceUtils


class Xxe(BaseRule):
    """
    XXE Protection rule
    """

    NAME = "xxe"
    INPUT_NAME = "XML Prolog"

    EXTERNAL_ENTITY_PATTERN = re.compile(
        r"<!ENTITY\s+[a-zA-Z0-f]+\s+(?:SYSTEM|PUBLIC)\s+(.*?)>"
    )

    def __init__(self, settings):
        BaseRule.__init__(self, settings)

        self.prolog_xml = None

    def is_prefilter(self):
        return False

    def is_postfilter(self):
        return False

    def find_attack(self, context, xml, **kwargs):
        if self.protect_excluded_by_code():
            return

        last_idx = 0
        declared_entities = []
        entities_resolved = []

        for match in self.EXTERNAL_ENTITY_PATTERN.finditer(xml):
            last_idx = match.end(0)

            entity_wrapper = EntityWrapper(match.group())
            if entity_wrapper.is_external_entity is False:
                continue

            declared_entities.extend([self._build_match(match.group(), last_idx)])
            entities_resolved.extend([self._build_wrapper(entity_wrapper)])

        self.prolog_xml = xml[:last_idx]

        attack = self.build_attack_with_match(
            context,
            None,
            None,
            xml,
            declared_entities=declared_entities,
            entities_resolved=entities_resolved,
        )
        return attack

    def _build_match(self, match_string, end_idx):
        match = XxeMatch()
        match.end_idx = end_idx
        match.start_idx = end_idx - len(match_string)
        return match

    def _build_wrapper(self, entity_wrapper):
        wrapper = XxeWrapper()
        wrapper.system_id = entity_wrapper.system_id
        wrapper.public_id = entity_wrapper.public_id
        return wrapper

    def build_sample(self, context, evaluation, url, **kwargs):
        sample = self.build_base_sample(context, evaluation)
        declared_entities = kwargs["declared_entities"]
        if declared_entities:
            sample.xxe.declared_entities.extend(declared_entities)

        entities_resolved = kwargs["entities_resolved"]
        if entities_resolved:
            sample.xxe.entities_resolved.extend(entities_resolved)

        sample.xxe.xml = self.prolog_xml
        return sample

    def build_base_sample(self, context, evaluation):
        sample = RaspRuleSample()
        sample.stack_trace_elements.extend(StackTraceUtils.build(ignore=True))

        sample.user_input.CopyFrom(self.build_user_input(context, evaluation))

        return sample

    def build_user_input(self, context, evaluation):
        ui = UserInput()
        ui.key = self.INPUT_NAME
        ui.input_type = UserInput.UNKNOWN
        ui.value = self.prolog_xml
        return ui
