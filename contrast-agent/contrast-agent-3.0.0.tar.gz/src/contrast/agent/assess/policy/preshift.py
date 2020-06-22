# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
class Preshift(object):
    """
    Holder class for information prior to shifting
    """

    def __init__(self):
        self.obj = None
        self.obj_length = 0
        self.args = []
        self.arg_lengths = 0
        self.kwargs = {}
