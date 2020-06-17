# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Base middleware for peripheric frameworks integration
"""
import logging

from ...constants import ACTIONS
from ...exceptions import ActionBlock, ActionRedirect, AttackBlocked
from ..hook_point import (
    execute_failing_callbacks,
    execute_post_callbacks,
    execute_pre_callbacks,
)

LOGGER = logging.getLogger(__name__)


class BaseMiddleware(object):
    """ Middleware base class for frameworks middleware hooks
    """

    def __init__(self, strategy, observation_queue, queue):
        LOGGER.debug("%s for %s", self.__class__.__name__, strategy)
        self.strategy = strategy
        self.observation_queue = observation_queue
        self.queue = queue

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, repr(self.strategy))

    def execute_pre_callbacks(self, args=None, record_attack=True):
        """ Execute pre callbacks. Only process valid action, in this context it's raising.
        """
        action = execute_pre_callbacks(
            self.strategy.strategy_key, self.strategy, self, args=args
        )

        action_status = action.get("status")

        if not action_status:
            return args

        elif action_status == ACTIONS["RAISE"]:
            LOGGER.debug(
                "Callback %s detected an attack", action.get("rule_name")
            )
            if record_attack:
                raise AttackBlocked(action.get("rule_name"))

        elif action_status == ACTIONS["ACTION_BLOCK"]:
            if record_attack:
                raise ActionBlock(action.get("action_id"))

        elif action_status == ACTIONS["ACTION_REDIRECT"]:
            if record_attack:
                raise ActionRedirect(action.get("action_id"), action["target_url"])

        elif action_status == ACTIONS["MODIFY_ARGS"]:
            return action.get("args")

        return args

    def execute_post_callbacks(self, response, args=None, record_attack=True):
        """ Execute post callbacks. Only process valid action, in this context it's raising.
        """
        action = execute_post_callbacks(
            self.strategy.strategy_key,
            self.strategy,
            self,
            result=response,
            args=args,
        )

        action_status = action.get("status")

        if not action_status:
            return response

        elif action_status == ACTIONS["RAISE"]:
            LOGGER.debug(
                "Callback %s detected an attack", action.get("rule_name")
            )
            if record_attack:
                raise AttackBlocked(action.get("rule_name"))

        elif action_status == ACTIONS["OVERRIDE"]:
            return action.get("new_return_value")

        return response

    def execute_failing_callbacks(self, exception, args=None):
        """ Execute failing callbacks. Only process valid action, in this context it's None.
        """
        if isinstance(exception, Exception):
            exception = (exception.__class__, exception, None)

        action = execute_failing_callbacks(
            self.strategy.strategy_key,
            self.strategy,
            self,
            exc_info=exception,
            args=args,
        )

        action_status = action.get("status")
        if action_status and action_status == ACTIONS["OVERRIDE"]:
            return action.get("new_return_value")
