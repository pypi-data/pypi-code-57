# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from collections import defaultdict


class AttributeDefaultDict(defaultdict):
    def __getitem__(self, name):
        if name in self:
            return defaultdict.__getitem__(self, name)

    def __getattr__(self, name):
        return self.__getitem__(name)

    def __setattr__(self, name, value):
        self[name] = value
