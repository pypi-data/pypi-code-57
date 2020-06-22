# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.protect.rule.base_rule import BaseRule, UserInput
from contrast.utils.decorators import set_context

import logging

logger = logging.getLogger("contrast")


class MethodTampering(BaseRule):
    NAME = "method-tampering"
    USER_INPUT_KEY = UserInput.InputType.Name(UserInput.METHOD)
    BLOCK_MESSAGE = "Http Method Tampering triggered. Blocked request."

    def __init__(self, settings):
        BaseRule.__init__(self, settings)

    @set_context("in_postfilter")
    def postfilter(self, context):
        """
        At postfilter we generate activity if input analysis was found and depending on application response code.

        if response code is either 4xx or 5xx, application was not exploited (only probed) by an unexpected HTTP method.
        If response code is anything else, then an unexpected HTTP method successfully exploited the application.
        """
        logger.debug("PROTECT: Postfilter for %s", self.name)

        evaluations_for_rule = self.evaluations_for_rule(context)

        response_code = context.request.response_code()

        for evaluation in evaluations_for_rule:
            if str(response_code).startswith("4") or str(response_code).startswith("5"):
                attack = self.build_attack_without_match(
                    context,
                    None,
                    None,
                    method=evaluation.value,
                    response_code=response_code,
                )
            else:
                attack = self.build_attack_with_match(
                    context,
                    None,
                    None,
                    None,
                    method=evaluation.value,
                    response_code=response_code,
                )
            self._append_to_activity(context, attack)

    def build_sample(self, context, evaluation, candidate_string, **kwargs):
        sample = self.build_base_sample(context, None)

        method = kwargs.get("method", "")

        sample.method_tampering.method = method
        sample.method_tampering.response_code = kwargs.get("response_code", -1)
        sample.user_input.CopyFrom(self.build_user_input(context, method))

        return sample

    def build_user_input(self, context, method):
        ui = UserInput()
        ui.key = self.USER_INPUT_KEY
        ui.input_type = UserInput.METHOD
        ui.value = method
        return ui
