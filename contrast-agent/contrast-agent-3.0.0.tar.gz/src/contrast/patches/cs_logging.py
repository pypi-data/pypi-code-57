# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Patch for logging module to implement deadzone for logging
"""
from contrast.extern.wrapt import register_post_import_hook

from contrast.agent import scope
from contrast.utils.patch_utils import patch_cls_or_instance


def emit(orig_func, patch_policy=None, *args, **kwargs):
    """
    Prevent recursive propagation when logging in assess

    We run the risk of recursively logging propagation events inside of log
    statements. This is because the logging module sometimes uses streams to
    output logs, and these logging events can inadvertently cause additional
    log output that we use for debugging within our assess code. We want to
    prevent this from occurring. Part of the reason for this is that we now
    instrument stream reads and writes, but we also are aware that StringIO
    is implemented with a lot of string building under the hood.

    The purpose of this patch is to make sure that we are in scope any time
    that log output is being produced.
    """
    with scope.contrast_scope():
        return orig_func(*args, **kwargs)


def patch_logging(logging_module):
    patch_cls_or_instance(logging_module.StreamHandler, "emit", emit)


def register_patches():
    register_post_import_hook(patch_logging, "logging")
