# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
This module contains workarounds for the fact that some builtin methods appear
to be unpatchable using funchook for one reason or another.
"""
import sys

from contrast.extern.six import PY2, PY3, text_type

import contrast
from contrast.agent import scope
from contrast.agent.assess.policy.methods import skip_analysis
from contrast.agent.assess.policy import Policy
from contrast.agent.assess.policy.propagation_policy import (
    PROPAGATOR_ACTIONS,
    propagate,
)
from contrast.agent.assess.utils import build_preshift
from contrast.assess_extensions.cs_str import set_attr_on_type


import logging

logger = logging.getLogger("contrast")


PY38 = PY3 and sys.version_info[1] == 8


PATCH_MAP = {}

# It appears to be unsafe to store these pointers in a dict, so we are just
# being explicit about it here
orig_str_strip = str.strip
orig_str_lstrip = str.lstrip
orig_str_rstrip = str.rstrip
orig_bytes_strip = bytes.strip
orig_bytes_lstrip = bytes.lstrip
orig_bytes_rstrip = bytes.rstrip
orig_bytearray_join = bytearray.join
# This corresponds to str.partition in Py3 and unicode.partition in Py2
orig_unicode_partition = text_type.partition
orig_unicode_rpartition = text_type.rpartition
orig_str_format = str.format
if PY2:
    orig_unicode_format = text_type.format


def bytearray_join(self, *args, **kwargs):
    # Since we need to make reference to the input multiple times, convert the
    # first argument to a list and use that instead. This prevents any iterators
    # from being exhausted before we can make use of them in propagation.
    # For bytearray.join, args == (list_or_iterator_of_things_to_join,...)
    # Note that this is different from the C hooks for other join methods. In
    # those cases, the PyObject *args argument corresponds to just the list or
    # iterator itself, in contrast to a tuple that contains that list or
    # iterator. (Got that straight?)
    args_list = [list(args[0])] + list(args[1:])
    result = orig_bytearray_join(self, *args_list, **kwargs)

    context = contrast.CS__CONTEXT_TRACKER.current()
    if skip_analysis(context) or scope.in_scope():
        return result

    try:
        frame = sys._getframe()
        with scope.propagation_scope():
            propagate("join", result, self, result, frame, args_list, kwargs)
    except Exception:
        logger.exception("failed to propagate bytearray.join")
    finally:
        return result


def build_format_patch(orig_method):
    def str_format(self, *args, **kwargs):
        """
        Propagation hook for str.format

        This hook is a special case because we need to enable some propagation to occur
        while we evaluate whether to propagate this particular event. With the current
        general hook infrastructure, this is not possible, so we need to account for it
        here. Eventually it may be possible to fit this back into the more general
        infrastructure if we overhaul the way that scope works.
        """
        result = orig_method(self, *args, **kwargs)

        context = contrast.CS__CONTEXT_TRACKER.current()
        if skip_analysis(context) or scope.in_scope():
            return result

        try:
            with scope.contrast_scope():
                frame = sys._getframe()

                policy = Policy()
                preshift = build_preshift(self, args, kwargs)

            for node in policy.propagators_by_name["BUILTIN.str.format"]:
                propagator_class = PROPAGATOR_ACTIONS.get(node.action)
                if propagator_class is None:
                    continue

                propagator = propagator_class(node, preshift, result)

                # This evaluation must not occur in scope. This is what enables us
                # to perform any conversions from object to __str__ or __repr__,
                # while allowing propagation to occur through those methods if
                # necessary.
                if not propagator.needs_propagation:
                    continue

                with scope.contrast_scope():
                    propagator.track_and_propagate(result, frame)
        except Exception:
            logger.exception("failed to propagate str.format")
        finally:
            return result

    return str_format


def build_str_patch(orig_method, method_name):
    """
    Build the patch method that is used to replace the original implementation
    """

    def patched_method(self, *args, **kwargs):
        result = orig_method(self, *args, **kwargs)

        context = contrast.CS__CONTEXT_TRACKER.current()
        if skip_analysis(context) or scope.in_scope():
            return result

        try:
            frame = sys._getframe()
            with scope.propagation_scope():
                propagate(method_name, result, self, result, frame, args, kwargs)
        except Exception:
            name = orig_method.__class__.__name__
            logger.exception("failed to propagate %s.%s", name, method_name)
        finally:
            return result

    patched_method.__name__ = method_name
    return patched_method


def patch_py38_methods():
    """
    Apply patches for methods that can't be hooked with funchook in Py38

    Specifically, the `strip`, `lstrip`, and `rstrip` methods of both `str` and
    `bytes` can't be hooked with funchook, so we use `set_attr_on_type` here.
    """
    global PATCH_MAP

    for strtype in [str, bytes]:
        for method_name in ["strip", "lstrip", "rstrip"]:
            if (strtype, method_name) in PATCH_MAP:
                continue

            orig_method = getattr(strtype, method_name)
            new_method = build_str_patch(orig_method, method_name)
            set_attr_on_type(strtype, method_name, new_method)
            PATCH_MAP[(strtype, method_name)] = True


def patch_format_methods():
    global PATCH_MAP

    if (str, "format") not in PATCH_MAP:
        set_attr_on_type(str, "format", build_format_patch(orig_str_format))
        PATCH_MAP[(str, "format")] = True

    if PY2 and (text_type, "format") not in PATCH_MAP:
        set_attr_on_type(text_type, "format", build_format_patch(orig_unicode_format))
        PATCH_MAP[(text_type, "format")] = True


def patch_strtype_methods():
    """
    Apply patches for all methods that can't be hooked with funchook

    For reasons that are not well understood, funchook fails to apply patches
    to certain methods on certain platforms. Now that we can hook builtins
    directly from Python, we apply the workarounds here. There is probably a
    performance penalty for having these patches implemented purely in Python,
    but it's better than not hooking these methods at all.

    Currently the only versions affected are Py3 and higher, but if we ever
    have problems with Py2 hooks, those workarounds should be added here too.
    """
    global PATCH_MAP

    if (text_type, "partition") not in PATCH_MAP:
        new_partition = build_str_patch(orig_unicode_partition, "partition")
        new_rpartition = build_str_patch(orig_unicode_rpartition, "rpartition")
        set_attr_on_type(text_type, "partition", new_partition)
        set_attr_on_type(text_type, "rpartition", new_rpartition)
        PATCH_MAP[(text_type, "partition")] = True
        PATCH_MAP[(text_type, "rpartition")] = True

    patch_format_methods()

    # Patching bytearray.join with funchook does not work for any Py3 versions
    if PY3 and (bytearray, "join") not in PATCH_MAP:
        set_attr_on_type(bytearray, "join", bytearray_join)
        PATCH_MAP[(bytearray, "join")] = True

    if PY38:
        patch_py38_methods()


def unpatch_strtype_methods():
    """
    Replace all patched strtype methods with the original implementation
    """
    global PATCH_MAP

    set_attr_on_type(text_type, "partition", orig_unicode_partition)
    set_attr_on_type(text_type, "rpartition", orig_unicode_rpartition)
    set_attr_on_type(str, "format", orig_str_format)

    if PY2:
        set_attr_on_type(text_type, "format", orig_unicode_format)
    else:
        set_attr_on_type(bytearray, "join", orig_bytearray_join)

    if PY38:
        set_attr_on_type(str, "strip", orig_str_strip)
        set_attr_on_type(str, "lstrip", orig_str_lstrip)
        set_attr_on_type(str, "rstrip", orig_str_rstrip)
        set_attr_on_type(bytes, "strip", orig_bytes_strip)
        set_attr_on_type(bytes, "lstrip", orig_bytes_lstrip)
        set_attr_on_type(bytes, "rstrip", orig_bytes_rstrip)

    PATCH_MAP.clear()
