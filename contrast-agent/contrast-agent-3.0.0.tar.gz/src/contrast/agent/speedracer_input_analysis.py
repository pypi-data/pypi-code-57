# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Functions for communication with speedracer to receive input analysis
"""

from contrast.api.settings_pb2 import ProtectionRule
from contrast.utils.exceptions.security_exception import SecurityException
from contrast.agent.settings_state import SettingsState

import logging

logger = logging.getLogger("contrast")


def get_input_analysis(request_context):
    logger.debug("Getting input analysis from speedracer ...")

    message = request_context.activity.http_request
    settings = SettingsState()

    responses = settings.client.send_messages_retry([message])
    speedracer_response = responses[0] if responses else None

    if not speedracer_response or not speedracer_response.protect_state:
        logger.debug("No response from speedracer: %s", speedracer_response)
        return

    if speedracer_response.input_analysis is None:
        logger.debug(
            "Speedracer returned nil input analysis - no evaluation for request"
        )

    request_context.do_not_track = speedracer_response.protect_state.track_request

    if speedracer_response.protect_state.security_exception:
        create_activity_from_speedracer_input_analysis(
            speedracer_response.input_analysis, request_context
        )
        raise SecurityException(
            request_context, "Speedracer said to block this request"
        )

    logger.debug("Speedracer input analysis: %s", speedracer_response.input_analysis)
    return speedracer_response.input_analysis


def create_activity_from_speedracer_input_analysis(
    speedracer_input_analysis, request_context
):
    """
    If speedracer returns any input analysis results, we should create
    attack result samples in case it did not create it.

    """
    if speedracer_input_analysis is None:
        return

    settings = SettingsState()

    for evaluation in speedracer_input_analysis.results:
        rule = settings.defend_rules[evaluation.rule_id]
        if rule.mode == ProtectionRule.BLOCK:
            # special case for rules (xss) that used to have infilter but now are only prefilter / BAP
            attack = rule.build_attack_with_match(
                request_context, evaluation, None, evaluation.value
            )
        else:
            attack = rule.build_attack_without_match(request_context, evaluation, None)
        request_context.activity.results.extend([attack])
