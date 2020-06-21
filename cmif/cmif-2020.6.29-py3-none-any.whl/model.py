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


def validate(root):
    """
    validate XML data of given root against RNG schema
    """
    schema = rng()
    result = schema.validate(root)
    if result:
        print("valid data in CMI format!")
    else:
        print("given data is invalid!")
        print("error log:")
        print(schema.error_log)
