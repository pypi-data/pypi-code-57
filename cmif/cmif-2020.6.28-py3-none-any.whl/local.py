#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
read and write local XML data in CMI format
"""

import os

from lxml import etree


def writer(root, file="cmif.xml", path="."):
    """
    write given root element to file at path
    """
    parser = etree.XMLParser(remove_blank_text=True)
    root.addprevious(etree.Comment(" Built with Python package cmif. "))
    xml = etree.ElementTree(root, parser=parser)
    if not os.path.exists(path):
        os.makedirs(path)
    out = os.path.join(path, file)
    xml.write(out, pretty_print=True, encoding="UTF-8", xml_declaration=True)


def reader(filepath):
    """
    read xml data from given file path
    """
    return etree.parse(filepath).getroot()
