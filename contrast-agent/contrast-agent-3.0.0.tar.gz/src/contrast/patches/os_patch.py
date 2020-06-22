# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os

from contrast.extern.wrapt import register_post_import_hook

from contrast.agent.assess import patch_manager
from contrast.applies.cmdi import apply_rule
from contrast.utils.patch_utils import patch_cls_or_instance

OS = "os"
POPEN = "popen"
SYSTEM = "system"


def popen(original_popen, patch_policy=None, *args, **kwargs):
    """
    First argument should be a string command or a list of parts of a command to be combined.

    It is recommended that subprocess is used in the Python documentation. These extra patches should cover us though.

    Example:
        os.popen("ls -lsa")
    """
    return apply_rule(OS, POPEN, original_popen, args, kwargs)


def system(original_system, patch_policy=None, *args, **kwargs):
    """
    First argument should be a string command or a list of parts of a command to be combined.

    It is recommended that subprocess is used in the Python documentation. These extra patches should cover us though.

    Example:
        os.system("ps -p 2993 -o time --no-headers")
    """
    return apply_rule(OS, SYSTEM, original_system, args, kwargs)


def patch_system(os_module):
    patch_cls_or_instance(os_module, SYSTEM, system)
    # NOTE this is deprecated but I'll leave it in for now
    patch_cls_or_instance(os_module, POPEN, popen)


def register_patches():
    register_post_import_hook(patch_system, OS)


def reverse_patches():
    patch_manager.reverse_patches_by_owner(os)
