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
    try:
        return data.find(".//title", namespaces=data.nsmap).text
    except AttributeError:
        pass
    return None


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
    try:
        return editor(data, multi=multi).text.strip() if not multi else \
            [e.text.strip() for e in editor(data, multi=multi)]
    except AttributeError:
        pass
    return None


def editor_email(data, multi=False):
    """
    | extract text of TEI element <email> from parent <editor>
    | set multi to True if multiple editors exist
    """
    try:
        return editor(data, multi=multi).find(".//email", namespaces=data.nsmap).text if not multi else \
            [e.find(".//email", namespaces=data.nsmap).text for e in editor(data, multi=multi)]
    except AttributeError:
        pass
    return None


def publisher(data):
    """
    extract text from child <ref> of TEI element <publisher>
    """
    try:
        return data.find(".//publisher/ref", namespaces=data.nsmap).text
    except AttributeError:
        pass
    return None


def publisher_target(data):
    """
    extract @target from child <ref> of TEI element <publisher>
    """
    try:
        return data.find(".//publisher/ref", namespaces=data.nsmap).attrib["target"]
    except (AttributeError, KeyError):
        pass
    return None


def idno(data):
    """
    extract text from TEI element <idno>
    """
    try:
        return data.find(".//idno", namespaces=data.nsmap).text
    except AttributeError:
        pass
    return None


def date_attrib(data):
    """
    extract @ from TEI element <date>
    """
    try:
        return data.find(".//date", namespaces=data.nsmap).attrib
    except AttributeError:
        pass
    return None


def date_when(data):
    """
    extract @when from TEI element <date>
    """
    try:
        return data.find(".//date", namespaces=data.nsmap).attrib["when"]
    except (AttributeError, KeyError):
        pass
    return None


def date_from(data):
    """
    extract @when from TEI element <date>
    """
    try:
        return data.find(".//date", namespaces=data.nsmap).attrib["from"]
    except (AttributeError, KeyError):
        pass
    return None


def date_to(data):
    """
    extract @when from TEI element <date>
    """
    try:
        return data.find(".//date", namespaces=data.nsmap).attrib["to"]
    except (AttributeError, KeyError):
        pass
    return None


def date_not_before(data):
    """
    extract @when from TEI element <date>
    """
    try:
        return data.find(".//date", namespaces=data.nsmap).attrib["notBefore"]
    except (AttributeError, KeyError):
        pass
    return None


def date_not_after(data):
    """
    extract @when from TEI element <date>
    """
    try:
        return data.find(".//date", namespaces=data.nsmap).attrib["notAfter"]
    except (AttributeError, KeyError):
        pass
    return None


def license(data):
    """
    extract text of TEI element <licence>
    """
    try:
        return data.find(".//licence", namespaces=data.nsmap).text
    except AttributeError:
        pass
    return None


def license_target(data):
    """
    extract @target from TEI element <licence>
    """
    try:
        return data.find(".//licence", namespaces=data.nsmap).attrib["target"]
    except (AttributeError, KeyError):
        pass
    return None


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
    try:
        return bibl_data.attrib[ns_xml("id")] if not multi else \
            [b.attrib[ns_xml("id")] for b in bibl_data]
    except (AttributeError, KeyError):
        pass
    return None


def bibl_type(data, multi=False):
    """
    | extract @type from TEI element <bibl>
    | set multi to True if multiple references exist
    """
    bibl_data = bibl(data, multi=multi)
    try:
        return bibl_data.attrib["type"] if not multi else \
            [b.attrib["type"] for b in bibl_data]
    except (AttributeError, KeyError):
        pass
    return None


def bibl_text(data, multi=False):
    """
    | extract text of TEI element <bibl>
    | set multi to True if multiple references exist
    """
    bibl_data = bibl(data, multi=multi)
    try:
        return re.sub("[ \r\n]+", " ", "".join([l for l in list(bibl_data.itertext())]).strip()) if not multi else \
            [re.sub("[ \r\n]+", " ", "".join([l for l in list(b.itertext())]).strip()) for b in bibl_data]
    except AttributeError:
        pass
    return None


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
    return []


def correspdesc_key(data):
    """
    extract @source from TEI elements <correspDesc>
    """
    correspdesc_data = correspdesc(data)
    try:
        return [cd.attrib["key"].replace("#", "") for cd in correspdesc_data]
    except KeyError:
        pass
    return []


def correspaction(data):
    """
    extract TEI elements <correspAction>
    """
    return data.findall(".//correspAction", namespaces=data.nsmap)


def correspaction_type(data):
    """
    extract @type from TEI elements <correspAction>
    """
    correspaction_data = correspaction(data)
    try:
        return [ca.attrib["type"] for ca in correspaction_data]
    except (AttributeError, KeyError):
        pass
    return None


def pers_name(data):
    """
    extract text from TEI element <persName>
    """
    try:
        return data.find(".//persName", namespaces=data.nsmap).text
    except AttributeError:
        pass
    return None


def pers_name_ref(data):
    """
    extract @ref from TEI element <persName>
    """
    try:
        return data.find(".//persName", namespaces=data.nsmap).attrib["ref"]
    except (AttributeError, KeyError):
        pass
    return None


def place_name(data):
    """
    extract text from TEI element <placeName>
    """
    try:
        return data.find(".//placeName", namespaces=data.nsmap).text
    except AttributeError:
        pass
    return None


def place_name_ref(data):
    """
    extract @ref from TEI element <placeName>
    """
    try:
        return data.find(".//placeName", namespaces=data.nsmap).attrib["ref"]
    except (AttributeError, KeyError):
        pass
    return None
