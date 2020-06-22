# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern import six

import contrast
from contrast.agent.protect.rule.cmdi_rule import CmdInjection
from contrast.agent.settings_state import SettingsState
from contrast.utils.decorators import fail_safely

import logging

logger = logging.getLogger("contrast")

VALID_TYPES = six.string_types + (six.binary_type, list, tuple)


@fail_safely("Failed to run protect Command Injection Rule")
def protect_rule(context, method, command):
    """
    This receives a command from the patched classes and checks the infilter method for CommandInjection

    SecurityException will be thrown if an attacker is found
    """
    rule = SettingsState().defend_rules[CmdInjection.NAME]

    if not rule or not rule.enabled:
        return

    if isinstance(command, six.string_types):
        original_command = command
    elif isinstance(command, list):
        original_command = " ".join(command)
    else:
        logger.debug(
            "WARNING: unknown input type %s for cmdi command %s", type(command), command
        )
        return

    rule.infilter(
        context, original_command, method=method, original_command=original_command
    )


def apply_rule(module, method, orig_func, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()

    if context is not None and SettingsState().is_protect_enabled():
        command = get_command(module, method, args, kwargs)
        if command is not None:
            protect_rule(context, method, command)

    return orig_func(*args, **kwargs)


def _get_subprocess_popen_command(args, kwargs):
    """Get original command string/list from subprocess.Popen.__init__"""
    return args[1] if len(args) > 1 else kwargs.get("args")


def _get_command_for_method(module, method, args, kwargs):
    """Get original command string/list from os and subprocess functions"""
    if args:
        return args[0]

    if module == "os" and method == "popen":
        name = "cmd"
    elif module == "subprocess":
        name = "args"
    else:
        name = "command"

    return kwargs.get(name)


@fail_safely("Failed to extract command for CMDi rule")
def get_command(module, method, args, kwargs):
    """
    Get the user-supplied command from the args or kwargs.

    Note that in theory, the user can supply the command via both
    args and kwargs, such as
        `os.popen(command, cmd=command)`
    This would raise an error when calling the original_func.
    Here we just look for one of the commands.

    NOTE: All of this will be replaced by protect policy
    """
    if module == "subprocess.Popen":
        command = _get_subprocess_popen_command(args, kwargs)
    else:
        command = _get_command_for_method(module, method, args, kwargs)

    if not command or not isinstance(command, VALID_TYPES):
        return

    return command
