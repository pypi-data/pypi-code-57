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

MODULE = "lxml.etree"
FROMSTRING = "fromstring"
PARSE = "parse"


def fromstring(original_fromstring, patch_policy=None, *args, **kwargs):
    """
    First argument should be an xml string
    """
    return apply_rule(MODULE, FROMSTRING, original_fromstring, args, kwargs)


def parse(original_parse, patch_policy=None, *args, **kwargs):
    """
    First argument should be an xml string
    """
    return apply_rule(MODULE, PARSE, original_parse, args, kwargs)


def patch_lxml(lxml_module):
    """
    Vulnerable to local xxe (lxml throws exception on external entity resolution attempts)
    """
    # TODO add after file/io support
    # patch_cls_or_instance(lxml_module, PARSE, parse)
    patch_cls_or_instance(lxml_module, FROMSTRING, fromstring)


def register_patches():
    register_post_import_hook(patch_lxml, MODULE)
