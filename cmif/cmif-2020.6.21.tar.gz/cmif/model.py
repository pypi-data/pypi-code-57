#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
schema models of CMI format
"""

from .local import reader

import os

from lxml.etree import RelaxNG


def odd():
    """
    get ODD specification of CMI format
    """
    return reader(os.path.join(os.path.dirname(__file__),
                               "standard/odd/cmi-customization.xml"))


def rng():
    """
    get RNG schema of CMI format
    """
    return RelaxNG(
            reader(os.path.join(os.path.dirname(__file__),
                                "standard/schema/cmi-customization.rng")))
