# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import subprocess

from contrast.extern.wrapt import register_post_import_hook

import contrast
from contrast.agent.assess import patch_manager
from contrast.agent.settings_state import SettingsState
from contrast.applies.cmdi import apply_rule as apply_cmdi_rule
from contrast.applies.deserialization import protect_rule as apply_deserialization_rule
from contrast.utils.decorators import fail_safely
from contrast.utils.patch_utils import patch_cls_or_instance

CALL = "call"
INIT = "__init__"
CHECK_CALL = "check_call"
CHECK_OUTPUT = "check_output"
SUBPROCESS = "subprocess"
POPEN = "Popen"
UNKNOWN = "UNKNOWN"


@fail_safely("Failed to get command")
def get_command(args, kwargs):
    command = None
    if args:
        command = args[0]
    elif kwargs:
        command = kwargs.get("args")
    return command


def call(original_call, patch_policy=None, *args, **kwargs):
    """
    First argument should be a string command or a list of parts of a command to be combined
    """
    context = contrast.CS__CONTEXT_TRACKER.current()

    if context and SettingsState().is_protect_enabled():
        command = get_command(args, kwargs)
        apply_deserialization_rule(context, command, UNKNOWN)

    return apply_cmdi_rule(SUBPROCESS, CALL, original_call, args, kwargs)


def check_output(original_check_output, patch_policy=None, *args, **kwargs):
    """
    First argument should be a string command or a list of parts of a command to be combined
    """

    context = contrast.CS__CONTEXT_TRACKER.current()

    if context and SettingsState().is_protect_enabled():
        command = get_command(args, kwargs)
        apply_deserialization_rule(context, command, UNKNOWN)

    return apply_cmdi_rule(
        SUBPROCESS, CHECK_OUTPUT, original_check_output, args, kwargs
    )


def check_call(original_open, patch_policy=None, *args, **kwargs):
    """
    First argument should be a string command or a list of parts of a command to be combined
    """
    context = contrast.CS__CONTEXT_TRACKER.current()

    if context and SettingsState().is_protect_enabled():
        command = get_command(args, kwargs)
        apply_deserialization_rule(context, command, UNKNOWN)

    return apply_cmdi_rule(SUBPROCESS, CHECK_CALL, original_open, args, kwargs)


def __init__(orig_init, patch_policy=None, *args, **kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()

    if context and SettingsState().is_protect_enabled():
        command = get_command(args, kwargs)
        apply_deserialization_rule(context, command, UNKNOWN)

    return apply_cmdi_rule(
        "{}.{}".format(SUBPROCESS, POPEN), INIT, orig_init, args, kwargs
    )


def patch_subprocess(subprocess_module):
    patch_cls_or_instance(subprocess_module, CALL, call)
    patch_cls_or_instance(subprocess_module, CHECK_CALL, check_call)
    patch_cls_or_instance(subprocess_module, CHECK_OUTPUT, check_output)
    patch_cls_or_instance(subprocess_module.Popen, INIT, __init__)


def register_patches():
    register_post_import_hook(patch_subprocess, "subprocess")


def reverse_patches():
    patch_manager.reverse_patches_by_owner(subprocess)
    patch_manager.reverse_patches_by_owner(subprocess.Popen)
