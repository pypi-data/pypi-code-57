# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast.extern.wrapt import register_post_import_hook

from contrast.agent.assess import patch_manager
from contrast.applies.deserialization import apply_rule
from contrast.utils.patch_utils import patch_cls_or_instance

DUMP = "dump"
DUMPS = "dumps"
LOAD = "load"
LOADS = "loads"

PICKLE = "pickle"
DESERIALIZER = PICKLE


def dump(original_dump, patch_policy=None, *args, **kwargs):
    return apply_rule(original_dump, DESERIALIZER, args[0], args, kwargs)


def load(original_load, patch_policy=None, *args, **kwargs):

    read_obj = args[0]

    try:
        seek_loc = read_obj.tell()
    except Exception:
        seek_loc = 0

    try:
        data = read_obj.read()
    except Exception:
        data = ""

    try:
        read_obj.seek(seek_loc)
    except Exception:
        pass

    return apply_rule(original_load, DESERIALIZER, data, args, kwargs)


def loads(original_loads, patch_policy=None, *args, **kwargs):
    return apply_rule(original_loads, DESERIALIZER, args[0], args, kwargs)


def patch_pickle(pickle_module):
    patch_cls_or_instance(pickle_module, DUMP, dump)
    patch_cls_or_instance(pickle_module, DUMPS, dump)

    patch_cls_or_instance(pickle_module, LOAD, load)
    patch_cls_or_instance(pickle_module, LOADS, loads)


def register_patches():
    register_post_import_hook(patch_pickle, "pickle")


def reverse_patches():
    pickle = sys.modules.get("pickle")
    if not pickle:
        return

    for name in [DUMP, DUMPS, LOAD, LOADS]:
        patch_manager.reverse_patch(pickle, name)
