#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build XML data in CMI format
"""

import uuid
from lxml import etree

XML_NS = "http://www.w3.org/XML/1998/namespace"
TEI_NS = "http://www.tei-c.org/ns/1.0"
CS_NS = "http://www.bbaw.de/telota/correspSearch"
RNG_SCHEMA = "https://raw.githubusercontent.com/TEI-Correspondence-SIG/" + \
    "CMIF/master/schema/cmi-customization.rng"
PI_TEXT = "href=\""+RNG_SCHEMA+"\" type=\"application/xml\" schematypens" + \
    "=\"http://relaxng.org/ns/structure/1.0\""
CC_TEXT = "This file is licensed under the terms " \
            + "of the Creative-Commons-License CC-BY 4.0"
CC_URL = "https://creativecommons.org/licenses/by/4.0/"


def pi_rng():
    """
    create processing instruction <?xml-model?>
    """
    return etree.ProcessingInstruction("xml-model", PI_TEXT)


def ns_xml(attrib):
    """
    add xml namespace to given attribute
    """
    return "{" + XML_NS + "}" + attrib


def ns_cs(attrib):
    """
    add correspSearch namespace to given attribute
    """
    return "{" + CS_NS + "}" + attrib


def tei_root(children=None):
    """
    create TEI root element <TEI> with (optional) children
    """
    root = etree.Element("TEI")
    root.set("xmlns", TEI_NS)
    add_children(root, children)
    return root


def tei_header(children=None):
    """
    create TEI element <teiHeader> with (optional) children
    """
    header = etree.Element("teiHeader")
    add_children(header, children)
    return header


def tei_file_desc(children=None):
    """
    create TEI element <fileDesc> with (optional) children
    """
    file_desc = etree.Element("fileDesc")
    add_children(file_desc, children)
    return file_desc


def tei_title_stmt(children=None):
    """
    create TEI element <titleStmt> with (optional) children
    """
    title_stmt = etree.Element("titleStmt")
    add_children(title_stmt, children)
    return title_stmt


def tei_title(elem_text):
    """
    crate TEI element <title> with given element text
    """
    title = etree.Element("title")
    title.text = elem_text
    return title


def tei_editor(elem_text):
    """
    create TEI element <editor> with given element text
    """
    editor = etree.Element("editor")
    editor.text = elem_text
    return editor


def tei_email(elem_text):
    """
    create TEI element <email> with given element text
    """
    email = etree.Element("email")
    email.text = elem_text
    return email


def tei_publication_stmt(children=None):
    """
    create TEI element <publicationStmt> with (optional) children
    """
    publication_stmt = etree.Element("publicationStmt")
    add_children(publication_stmt, children)
    return publication_stmt


def tei_publisher(child_ref=None):
    """
    create TEI element <publisher> with (optional) child element <ref>
    """
    publisher = etree.Element("publisher")
    add_child(publisher, child_ref)
    return publisher


def tei_ref(elem_text, attrib_target):
    """
    create TEI element <ref> with @target
    """
    ref = etree.Element("ref")
    ref.set("target", attrib_target)
    ref.text = elem_text
    return ref


def tei_idno(elem_text, attrib_type="url"):
    """
    create TEI element <idno> with @type
    """
    idno = etree.Element("idno")
    idno.set('type', attrib_type)
    idno.text = elem_text
    return idno


def tei_availability(child_license=None):
    """
    create TEI element <availability> with (optional) child element <licence>
    """
    availability = etree.Element("availability")
    add_child(availability, child_license)
    return availability


def tei_license(elem_text="", attrib_target=""):
    """
    create TEI element <licence> with (optional) text and @target
    """
    if elem_text == "" and attrib_target == "":
        elem_text = CC_TEXT
        attrib_target = CC_URL
    license = etree.Element("licence")
    license.set("target", attrib_target)
    license.text = elem_text
    return license


def tei_source_desc(children=None):
    """
    create TEI element <sourceDesc> with (optional) children
    """
    source_desc = etree.Element("sourceDesc")
    add_children(source_desc, children)
    return source_desc


def tei_bibl(elem_text, attrib_type, attrib_xml_id=None, domain=None):
    """
    create TEI element <bibl> with given text and @type
    """
    bibl = etree.Element("bibl")
    bibl.set("type", attrib_type)
    bibl.text = elem_text
    if attrib_xml_id is None:
        attrib_xml_id = str(uuid.uuid3(uuid.NAMESPACE_URL, domain)) if domain \
            else str(uuid.uuid4())
    bibl.set(ns_xml("id"), attrib_xml_id)
    return bibl


def tei_profile_desc(children=None):
    """
    create TEI element <profileDesc>
    """
    profile_desc = etree.Element("profileDesc")
    add_children(profile_desc, children)
    return profile_desc


def tei_corresp_desc(attrib_key="", attrib_ref="",
                     attrib_source="", children=None):
    """
    create TEI element <correspDesc> with @ref
    """
    corresp_desc = etree.Element("correspDesc")
    add_attrib(corresp_desc, "key", attrib_key)
    add_attrib(corresp_desc, "ref", attrib_ref)
    add_attrib(corresp_desc, "source", attrib_source)
    add_children(corresp_desc, children)
    return corresp_desc


def tei_corresp_action(attrib_type, children=None):
    """
    create TEI element <correspAction> with @type
    """
    corresp_action = etree.Element("correspAction")
    corresp_action.set("type", attrib_type)
    add_children(corresp_action, children)
    return corresp_action


def tei_date(attrib_when="", attrib_from="", attrib_to="",
             attrib_not_before="", attrib_not_after=""):
    """
    create TEI element <date> with @when or @from and @to
    """
    date = etree.Element("date")
    add_attrib(date, "when", attrib_when)
    add_attrib(date, "from", attrib_from)
    add_attrib(date, "to", attrib_to)
    add_attrib(date, "notBefore", attrib_not_before)
    add_attrib(date, "notAfter", attrib_not_after)
    return date


def tei_place_name(elem_text, attrib_ref=""):
    """
    create TEI element <placeName> with given element text and @ref
    """
    place_name = etree.Element("placeName")
    place_name.text = elem_text
    add_attrib(place_name, "ref", attrib_ref)
    return place_name


def tei_pers_name(elem_text, attrib_ref=""):
    """
    create TEI element <persName> with given element text and @ref
    """
    pers_name = etree.Element("persName")
    pers_name.text = elem_text
    add_attrib(pers_name, "ref", attrib_ref)
    return pers_name


def tei_org_name(elem_text, attrib_ref=""):
    """
    create TEI element <orgName> with given element text
    """
    org_name = etree.Element("orgName")
    org_name.text = elem_text
    add_attrib(org_name, "ref", attrib_ref)
    return org_name


def tei_text_empty():
    """
    create TEI element <text> with child elements <body> and <p> (empty)
    """
    text = tei_text()
    body = tei_body()
    body.append(tei_p())
    text.append(body)
    return text


def tei_text():
    """
    create TEI element <text>
    """
    return etree.Element("text")


def tei_body():
    """
    create TEI element <body>
    """
    return etree.Element("body")


def tei_p():
    """
    create TEI element <p>
    """
    return etree.Element("p")


def add_pi(tree):
    """
    add processing instruction <?xml-model?> to given element tree
    """
    tree.getroot().addprevious(pi_rng())


def add_attrib(element, name, value):
    """
    add attribute to element if value != ""
    """
    if value != "":
        element.set(name, value)


def add_child(parent, element):
    """
    add element to parent if not None
    """
    if element is not None:
        parent.append(element)


def add_children(parent, elements):
    """
    add elements to parent if not None
    """
    if elements is not None:
        for child in elements:
            parent.append(child)


def pretty(elements):
    """
    pretty print given elements
    """
    print(etree.tostring(elements, pretty_print=True).decode().strip())


def tostr(element):
    """
    convert given element to str
    """
    return etree.tostring(element).decode().strip()
