# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import inspect

from contrast.extern.wrapt import register_post_import_hook

from contrast.agent.assess.policy import propagation_policy
from contrast.utils.assess.stream_utils import BaseStreamProxy, stream_patch_body
from contrast.utils.patch_utils import patch_cls_or_instance

import logging

logger = logging.getLogger("contrast")


def build_patch(self, orig_func, method_name):
    def patched_func(*args, **kwargs):
        return stream_patch_body(method_name, orig_func, self, *args, **kwargs)

    patched_func.__name__ = method_name
    return patched_func


class StringIOProxy(BaseStreamProxy):
    """
    Base class for stream types from the cStringIO module (Py2 only)
    """

    CS__METHOD_NAMES = BaseStreamProxy.CS__METHOD_NAMES + ["getvalue"]

    getvalue = None

    def __init__(self, wrapped):
        super(StringIOProxy, self).__init__(wrapped)
        for method_name in self.CS__METHOD_NAMES:
            orig_func = getattr(self, method_name)
            new_func = build_patch(self, orig_func, method_name)
            setattr(self, method_name, new_func)


class InputType(StringIOProxy):
    """Proxy class for cStringIO.InputType"""


class OutputType(StringIOProxy):
    """Proxy class for CstringIO.OutputType"""

    CS__METHOD_NAMES = StringIOProxy.CS__METHOD_NAMES + ["write", "writelines"]

    write = None
    writelines = None


def wrap_stream(stream):
    from cStringIO import InputType as OrigInputType

    return (
        InputType(stream) if isinstance(stream, OrigInputType) else OutputType(stream)
    )


def patched_StringIO(orig_func, patch_policy=None, *args, **kwargs):
    orig_stream = orig_func(*args, **kwargs)

    try:
        proxied_stream = wrap_stream(orig_stream)
        frame = inspect.currentframe()
        propagation_policy.create_stream_source_event(
            proxied_stream, frame.f_back, args, kwargs
        )
        return proxied_stream
    except Exception:
        logger.exception("Failed to propagate cStringIO.StringIO creation")

    return orig_stream


def patch_cStringIO(cStringIO_module):
    # cStringIO.StringIO is actually a factory function, not a class
    patch_cls_or_instance(cStringIO_module, "StringIO", patched_StringIO)


def register_patches():
    register_post_import_hook(patch_cStringIO, "cStringIO")
