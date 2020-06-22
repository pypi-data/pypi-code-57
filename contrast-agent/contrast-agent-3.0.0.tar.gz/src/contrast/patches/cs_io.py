# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import functools
from contrast.extern.wrapt import register_post_import_hook

from contrast.agent.assess import patch_manager
from contrast.utils.assess.stream_utils import stream_patch_body
from contrast.assess_extensions import cs_str

import logging

logger = logging.getLogger("contrast")


def build_patch(orig_func, method_name):
    def patched_func(self, *args, **kwargs):
        bound_method = functools.partial(orig_func, self)
        return stream_patch_body(method_name, bound_method, self, *args, **kwargs)

    patched_func.__name__ = method_name
    return patched_func


def patch_method(io_type, method_name):
    orig_func = getattr(io_type, method_name)
    if patch_manager.is_patched(orig_func):
        return

    new_func = build_patch(orig_func, method_name)
    cs_str.set_attr_on_type(io_type, method_name, new_func)
    patch_manager.register_patch(io_type, method_name, orig_func)


def patch_getvalue(io_module):
    # TODO: PYT-335 make these hooks reversible
    patch_method(io_module.StringIO, "getvalue")
    patch_method(io_module.BytesIO, "getvalue")


def patch_io(io_module):
    """
    Apply patches to methods of builtin stream types
    """
    for io_type in [io_module.StringIO, io_module.BytesIO]:
        patch_method(io_type, "write")

    # No need to hook StringIO.writelines because it is implemented as str.join under
    # the hood, so we already propagate for free. Unfortunately this might make the
    # reporting look a little odd, so we maybe should consider another solution later.
    patch_method(io_module.BytesIO, "writelines")

    # This patch exists solely for the purposes of working around our inability
    # to patch getvalue in StringIO and BytesIO using funchook.
    patch_getvalue(io_module)


def register_patches():
    register_post_import_hook(patch_io, "io")
