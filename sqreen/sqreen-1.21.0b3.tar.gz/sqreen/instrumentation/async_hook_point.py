# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
"""Asynchronous variant of hook_point."""

import logging
import sys

from .._vendors.wrapt import FunctionWrapper
from ..constants import ACTIONS
from ..exceptions import ActionBlock, ActionRedirect, AttackBlocked
from .hook_point import (
    execute_failing_callbacks,
    execute_post_callbacks,
    execute_pre_callbacks,
    valid_args,
)

LOGGER = logging.getLogger(__name__)


def async_hook_point(strategy, hook_name, hook_method, original):
    """Asynchronous variant of hook_point."""
    from asyncio import coroutine

    @coroutine
    def wrapper(wrapped, instance, args, kwargs):
        LOGGER.debug(
            "Checking before async hook point of %s for %s/%s",
            strategy,
            hook_name,
            hook_method,
        )
        strategy.before_hook_point()
        key = (hook_name, hook_method)

        # Call pre callbacks.
        action = execute_pre_callbacks(key, strategy, instance, args, kwargs)

        if action.get("status") == ACTIONS["RAISE"]:
            LOGGER.debug(
                "Callback %s detected an attack", action.get("rule_name")
            )
            raise AttackBlocked(action.get("rule_name"))
        elif action.get("status") == ACTIONS["ACTION_BLOCK"]:
            LOGGER.debug(
                "Action %s blocked the request", action.get("action_id")
            )
            raise ActionBlock(action.get("action_id"))
        elif action.get("status") == ACTIONS["ACTION_REDIRECT"]:
            LOGGER.debug(
                "Action %s redirected the request to %r",
                action.get("action_id"),
                action["target_url"],
            )
            raise ActionRedirect(action.get("action_id"), action["target_url"])
        elif action.get("status") == ACTIONS["OVERRIDE"]:
            return action.get("new_return_value")
        elif action.get("status") == ACTIONS["MODIFY_ARGS"]:
            if valid_args(action["args"]):
                args, kwargs = action["args"]

        # Call the original method.
        retry = True
        while retry is True:
            try:
                retry = False
                # Try to call the original coroutine.
                result = yield from wrapped(*args, **kwargs)
            except Exception:
                # In case of error, call fail callbacks with exception infos.
                exc_info = sys.exc_info()

                # Either raise an exception, set a return value or retry.
                action = execute_failing_callbacks(
                    key, strategy, instance, exc_info, args, kwargs
                )

                if action.get("status") == ACTIONS["RAISE"]:
                    LOGGER.debug(
                        "Callback %s detected an attack",
                        action.get("rule_name"),
                    )
                    raise AttackBlocked(action.get("rule_name"))
                elif action.get("status") == ACTIONS["RETRY"]:
                    retry = True
                elif action.get("status") == ACTIONS["OVERRIDE"]:
                    return action.get("new_return_value")

                # Be sure to raise if no retry or override.
                if retry is False:
                    raise

        # Then call post callback in reverse order to simulate decorator
        # behavior.
        action = execute_post_callbacks(
            key, strategy, instance, result, args, kwargs
        )

        if action.get("status") == ACTIONS["RAISE"]:
            LOGGER.debug(
                "Callback %s detected an attack", action.get("rule_name")
            )
            raise AttackBlocked(action.get("rule_name"))
        elif action.get("status") == ACTIONS["OVERRIDE"]:
            return action.get("new_return_value")

        # Return the original value.
        return result

    return FunctionWrapper(original, wrapper)
