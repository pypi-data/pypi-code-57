#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract XML data in CMI format
"""

import re
from .build import ns_cs, ns_xml


def title(data):
    """
    extract text of TEI element <title>
    """
    return data.find(".//title", namespaces=data.nsmap).text


def editor(data, multi=False):
    """
    | extract TEI element <editor>
    | set multi to True if multiple editors exist
    """
    return data.find(".//editor", namespaces=data.nsmap) if not multi else \
        data.findall(".//editor", namespaces=data.nsmap)


def editor_name(data, multi=False):
    """
    | extract text of TEI element <editor>
    | set multi to True if multiple editors exist
    """
    return editor(data, multi=multi).text.strip() if not multi else \
        [e.text.strip() for e in editor(data, multi=multi)]


def editor_email(data, multi=False):
    """
    | extract text of TEI element <email> from parent <editor>
    | set multi to True if multiple editors exist
    """
    return editor(data, multi=multi).find(".//email", namespaces=data.nsmap).text if not multi else \
        [e.find(".//email", namespaces=data.nsmap).text for e in editor(data, multi=multi)]


def publisher(data):
    """
    extract text from child <ref> of TEI element <publisher>
    """
    return data.find(".//publisher/ref", namespaces=data.nsmap).text


def publisher_target(data):
    """
    extract @target from child <ref> of TEI element <publisher>
    """
    return data.find(".//publisher/ref", namespaces=data.nsmap).attrib["target"]


def idno(data):
    """
    extract text of TEI element <idno>
    """
    return data.find(".//idno", namespaces=data.nsmap).text


def date(data):
    """
    extract @when from TEI element <date>
    """
    return data.find(".//date", namespaces=data.nsmap).attrib["when"]


def license(data):
    """
    extract text of TEI element <license>
    """
    return data.find(".//licence", namespaces=data.nsmap).text


def license_target(data):
    """
    extract @target from TEI element <licence>
    """
    return data.find(".//licence", namespaces=data.nsmap).attrib["target"]


def bibl(data, multi=False):
    """
    | extract TEI element <bibl>
    | set multi to True if multiple references exist
    """
    return data.find(".//bibl", namespaces=data.nsmap) if not multi else \
        data.findall(".//bibl", namespaces=data.nsmap)


def bibl_id(data, multi=False):
    """
    | extract @xml:id from TEI element <bibl>
    | set multi to True if multiple references exist
    """
    bibl_data = bibl(data, multi=multi)
    return bibl_data.attrib[ns_xml("id")] if not multi else \
        [b.attrib[ns_xml("id")] for b in bibl_data]


def bibl_type(data, multi=False):
    """
    | extract @type from TEI element <bibl>
    | set multi to True if multiple references exist
    """
    bibl_data = bibl(data, multi=multi)
    return bibl_data.attrib["type"] if not multi else \
        [b.attrib["type"] for b in bibl_data]


def bibl_text(data, multi=False):
    """
    | extract text of TEI element <bibl>
    | set multi to True if multiple references exist
    """
    bibl_data = bibl(data, multi=multi)
    return re.sub("[ \r\n]+", " ", "".join([l for l in list(bibl_data.itertext())]).strip()) if not multi else \
        [re.sub("[ \r\n]+", " ", "".join([l for l in list(b.itertext())]).strip()) for b in bibl_data]


def correspdesc(data):
    """
    extract TEI elements <correspDesc>
    """
    return data.findall(".//correspDesc", namespaces=data.nsmap)


def correspdesc_source(data):
    """
    extract @source from TEI elements <correspDesc>
    """
    correspdesc_data = correspdesc(data)
    try:
        return [cd.attrib["source"].replace("#", "") for cd in correspdesc_data]
    except KeyError:
        pass
    try:
        return [cd.attrib[ns_cs("source")].replace("#", "") for cd in correspdesc_data]
    except KeyError:
        pass
    return None
