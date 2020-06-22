# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.six import PY3
from contrast.extern.wrapt import register_post_import_hook

from contrast.applies.common.applies_pt_rule import (
    apply_rule,
    METHOD_OPEN,
    MODULE_BUILTIN,
    MODULE_IO,
)
from contrast.utils.patch_utils import patch_cls_or_instance


def cs__open_builtin(original_open, patch_policy=None, *args, **kwargs):
    return apply_rule(MODULE_BUILTIN, METHOD_OPEN, original_open, args, kwargs)


def cs__open_io(original_open, patch_policy=None, *args, **kwargs):
    return apply_rule(MODULE_IO, METHOD_OPEN, original_open, args, kwargs)


# Python 2
def patch_builtin(builtin_module):
    patch_cls_or_instance(builtin_module, METHOD_OPEN, cs__open_builtin)


# Python 3
def patch_builtins(builtins_module):
    patch_cls_or_instance(builtins_module, METHOD_OPEN, cs__open_builtin)


def patch_io(io_module):
    patch_cls_or_instance(io_module, METHOD_OPEN, cs__open_io)


def register_patches():
    register_post_import_hook(patch_builtin, "__builtin__")

    if PY3:
        register_post_import_hook(patch_builtins, "builtins")
    else:
        # In PY3 io.open is builtins.open
        register_post_import_hook(patch_io, "io")
