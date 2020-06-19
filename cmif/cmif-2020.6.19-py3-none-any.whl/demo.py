#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo XML data in CMI format
"""

from .retrieve import remote_file

WIELAND = "https://correspsearch.net/storage/WielandBW-1.xml"
GOTTSCHED = "https://raw.githubusercontent.com/" + \
    "saw-leipzig/cmif-gottsched/master/letters.xml"


def wieland():
    """
    get data of Wieland's Briefe (1750-1760) as demo for CMI-format
    """
    return remote_file(WIELAND)


def gottsched():
    """
    get data of Gottsched's Briefwechsel as demo for CMI-format
    """
    return remote_file(GOTTSCHED)
