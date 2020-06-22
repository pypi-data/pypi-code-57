# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.utils.object_share import ObjectShare


def build_method_name(method_name):
    """
    Builds a name based on the method name

    Example:
        cs__assess_append
    """
    return ObjectShare.CONTRAST_ASSESS_METHOD_START + method_name
