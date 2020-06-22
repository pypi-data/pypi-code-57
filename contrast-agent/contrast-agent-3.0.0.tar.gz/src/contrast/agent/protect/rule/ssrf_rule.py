# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.protect.rule.base_rule import BaseRule

import logging

logger = logging.getLogger("contrast")


class Ssrf(BaseRule):
    """
    Ssrf Protection rule
    """

    NAME = "ssrf"

    def __init__(self, settings):
        BaseRule.__init__(self, settings)

    def is_postfilter(self):
        return False

    BLOCK_MESSAGE = "SSRF rule triggered. Request blocked."

    def find_attack(self, context, url, **kwargs):
        if self.protect_excluded_by_code():
            return

        evaluations_for_rule = self.evaluations_for_rule(context)

        attack = None
        for evaluation in evaluations_for_rule:
            logger.debug("Inspecting: %s", evaluation)

            if url:
                if url.startswith(evaluation.value):
                    attack = self.build_attack_with_match(
                        context, evaluation, attack, url, **kwargs
                    )
            else:
                attack = self.build_attack_without_match(
                    context, evaluation, attack, **kwargs
                )

        return attack

    def build_sample(self, context, evaluation, url, **kwargs):
        sample = self.build_base_sample(context, evaluation)
        if url is not None:
            sample.ssrf.url = url
        return sample
