# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.protect.rule.base_rule import BaseRule
from contrast.agent.protect.rule.deserialization.pickle_searcher import PickleSearcher
from contrast.agent.protect.rule.deserialization.yaml_searcher import YAMLSearcher
from contrast.api.dtm_pb2 import AttackResult, UserInput
from contrast.api.settings_pb2 import InputAnalysisResult
from contrast.utils.decorators import set_context
from contrast.utils.exceptions.security_exception import SecurityException
from contrast.utils.string_utils import ends_with_any

import logging

logger = logging.getLogger("contrast")


class Deserialization(BaseRule):
    """
    Deserialization Protection rule
    """

    NAME = "untrusted-deserialization"

    # pickle and pyyaml both use load
    METHODS = [
        "loads",
        "load",
        "construct_object",
        "construct_python_object_apply",
        "construct_mapping",
        "make_python_instance",
    ]
    FILENAMES = ["pickle.py", "yaml.constructor.py", "yaml.__init__.py"]

    UNKNOWN = "UNKNOWN"

    def __init__(self, settings):
        BaseRule.__init__(self, settings)

    @property
    def custom_searchers(self):
        return [PickleSearcher(), YAMLSearcher()]

    def is_prefilter(self):
        return False

    def is_postfilter(self):
        return False

    @set_context("in_infilter")
    def infilter(self, context, match_string, **kwargs):
        logger.debug("PROTECT: Infilter for %s", self.name)

        if self.check_for_deserialization(
            kwargs.get("stack_elements", []), kwargs.get("deserializer", "")
        ):
            self.report_attack_without_finding(context, match_string, **kwargs)

        return super(Deserialization, self).infilter(context, match_string, **kwargs)

    def find_attack(self, context, candidate_string, **kwargs):
        """
        Finds the attacker in the original string if present
        """
        if candidate_string is not None:
            logger.debug("Checking for %s in %s", self.name, candidate_string)

        if self.protect_excluded_by_code():
            return

        attack = None
        if self.evaluate_custom_searchers(candidate_string):
            evaluation = self.build_evaluation(candidate_string)
            attack = self.build_attack_with_match(
                context, evaluation, attack, candidate_string, **kwargs
            )

        return attack

    def report_attack_without_finding(self, context, value, **kwargs):
        evaluation = self.build_evaluation(value)
        attack = self.build_attack_with_match(
            context, evaluation, None, value, **kwargs
        )

        attack.response = AttackResult.BLOCKED

        self._append_to_activity(context, attack)

        raise SecurityException(
            self,
            "Found deserialization attempt in stack, triggered in infilter. Blocked.",
        )

    def check_for_deserialization(self, stack_elements, deserializer):
        found_on_stack = False

        for element in stack_elements[::-1]:
            lower_file_name = element.file_name.lower()

            if (
                element.method_name
                and element.method_name in self.METHODS
                and (
                    lower_file_name in self.FILENAMES
                    or ends_with_any(lower_file_name, self.FILENAMES)
                )
            ):
                found_on_stack = True
                break

        if found_on_stack and deserializer == self.UNKNOWN:
            return True

        return False

    def build_sample(self, context, evaluation, input_value, **kwargs):
        sample = self.build_base_sample(context, evaluation)

        sample.untrusted_deserialization.command = False

        if "deserializer" in kwargs:
            sample.untrusted_deserialization.deserializer = kwargs["deserializer"]

        return sample

    def evaluate_custom_searchers(self, attack_vector):
        searcher_score = 0
        for searcher in self.custom_searchers:
            impact = searcher.impact_of(attack_vector)

            if impact > 0:
                logger.debug("Match on custom searcher: %s", searcher.searcher_id)

                searcher_score += impact
                if searcher_score >= searcher.IMPACT_HIGH:
                    return True

        return False

    def build_evaluation(self, value):
        """
        Given a user-input value, aka gadget, create an InputAnalysisResult instance.

        :param value: the user input containing a Gadget
        :return: InputAnalysisResult for this input
        """
        ia_result = InputAnalysisResult()
        ia_result.rule_id = self.NAME
        ia_result.input_type = UserInput.UNKNOWN
        ia_result.value = value
        ia_result.key = self.NAME
        return ia_result
