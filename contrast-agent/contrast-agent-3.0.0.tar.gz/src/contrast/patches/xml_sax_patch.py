# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
TODO: this patch is only necessary for the protect rule. The assess rule is completely
handled by policy.
"""
from contrast.extern.wrapt import register_post_import_hook

from contrast.applies.common.applies_xxe_rule import apply_rule
from contrast.utils.patch_utils import patch_cls_or_instance

MODULE = "xml.sax"
PARSE = "parse"
PARSESTRING = "parseString"


def parse(original_parse, patch_policy=None, *args, **kwargs):
    return apply_rule(MODULE, PARSE, original_parse, args, kwargs)


def parse_string(original_parsestring, patch_policy=None, *args, **kwargs):
    return apply_rule(MODULE, PARSESTRING, original_parsestring, args, kwargs)


def patch_xml(sax_module):
    # TODO add after file/io support
    # patch_cls_or_instance(sax_module, PARSE, parse_string)
    patch_cls_or_instance(sax_module, PARSESTRING, parse_string)


def register_patches():
    register_post_import_hook(patch_xml, MODULE)
