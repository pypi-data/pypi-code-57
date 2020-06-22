# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern import six
from contrast.extern.wrapt import register_post_import_hook

from contrast.assess_extensions import cs_str
from contrast.utils.patch_utils import patch_cls_or_instance

import logging

logger = logging.getLogger("contrast")


START_METHOD = "start"
BOOTSTRAP_METHOD = "_bootstrap_inner" if six.PY3 else "_Thread__bootstrap_inner"


def start(orig_func, patch_policy, self, *args, **kwargs):
    import threading

    try:
        # Save the scope of the current (creating) thread to copy to new thread
        self.cs__parent_scope = cs_str.get_thread_scope()
        # This is used by the context manager
        self.cs__parent_id = threading.current_thread().ident
    except Exception:
        logger.exception("Failed to instrument thread start")

    return orig_func(self, *args, **kwargs)


def _bootstrap_inner(orig_func, patch_policy, self, *args, **kwargs):
    # The new thread inherits the scope from the thread that created it
    try:
        cs_str.set_thread_scope(self.cs__parent_scope)
    except Exception:
        logger.exception("Failed to set thread scope")

    result = orig_func(self, *args, **kwargs)

    try:
        cs_str.destroy_thread_scope()
    except Exception:
        logger.exception("Failed to tear down thread scope")

    # We expect result to be None, but this is done for consistency/safety
    return result


def patch_threading(threading_module):
    patch_cls_or_instance(threading_module.Thread, START_METHOD, start)
    # This instruments the method that actually runs inside the system thread
    patch_cls_or_instance(threading_module.Thread, BOOTSTRAP_METHOD, _bootstrap_inner)


def register_patches():
    register_post_import_hook(patch_threading, "threading")
