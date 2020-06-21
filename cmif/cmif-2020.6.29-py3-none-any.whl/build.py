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
    | create TEI element <bibl> with given text, @type and (optional) @xml:id
    | if @xml:id is None a uuid is being generated
    | if domain is None the uuid will be random
    | if domain is not None the uuid will be static
    """
    bibl = etree.Element("bibl")
    if attrib_type not in ["print", "online", "hybrid"]:
        print("@type has to be 'print', 'online' or 'hybrid'!")
        return None
    bibl.set("type", attrib_type)
    bibl.text = elem_text
    if attrib_xml_id is None:
        attrib_xml_id = tei_bibl_id(domain=domain)
    bibl.set(ns_xml("id"), attrib_xml_id)
    return bibl


def tei_bibl_id(domain=None):
    """
    | generate uuid for @xml:id of TEI element <bibl> by given domain
    | if domain is None a random uuid is being generated
    """
    found = False
    if domain is not None:
        while not found:
            domain_uuid = str(uuid.uuid3(uuid.NAMESPACE_URL, domain))
            if domain_uuid[0].isalpha():
                return domain_uuid
            domain_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, domain))
            if domain_uuid[0].isalpha():
                return domain_uuid
            domain_uuid = str(uuid.uuid3(uuid.NAMESPACE_OID, domain))
            if domain_uuid[0].isalpha():
                return domain_uuid
            domain_uuid = str(uuid.uuid3(uuid.NAMESPACE_X500, domain))
            if domain_uuid[0].isalpha():
                return domain_uuid
            domain_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, domain))
            if domain_uuid[0].isalpha():
                return domain_uuid
            domain_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, domain))
            if domain_uuid[0].isalpha():
                return domain_uuid
            domain_uuid = str(uuid.uuid5(uuid.NAMESPACE_OID, domain))
            if domain_uuid[0].isalpha():
                return domain_uuid
            domain_uuid = str(uuid.uuid5(uuid.NAMESPACE_X500, domain))
            if domain_uuid[0].isalpha():
                return domain_uuid
            if not found:
                print("could not create uuid valid as xml:id from given domain!")
                print("try another one? meanwhile generating a random uuid...")
            while not found:
                domain_uuid = str(uuid.uuid4())
                if domain_uuid[0].isalpha():
                    return domain_uuid
    else:
        print("no domain given! generating a random uuid...")
        while not found:
            domain_uuid = str(uuid.uuid4())
            if domain_uuid[0].isalpha():
                return domain_uuid


def tei_profile_desc(children=None):
    """
    create TEI element <profileDesc> with (optional) children
    """
    profile_desc = etree.Element("profileDesc")
    add_children(profile_desc, children)
    return profile_desc


def tei_corresp_desc(attrib_key="", attrib_ref="",
                     attrib_source="", children=None):
    """
    create TEI element <correspDesc> with @ref, @source and (optional) children
    """
    corresp_desc = etree.Element("correspDesc")
    add_attrib(corresp_desc, "key", attrib_key)
    add_attrib(corresp_desc, "ref", attrib_ref)
    add_attrib(corresp_desc, "source", attrib_source)
    add_children(corresp_desc, children)
    return corresp_desc


def tei_corresp_action(attrib_type, children=None):
    """
    create TEI element <correspAction> with @type and (optional) children
    """
    corresp_action = etree.Element("correspAction")
    if attrib_type not in ["sent", "received", "transmitted",
                           "forwarded", "redirected"]:
        print("can not create <correspAction> with given value of @type!")
        print("possible values for @type:")
        print("'sent', 'received', 'transmitted', 'redirected or 'forwarded'")
        return None
    corresp_action.set("type", attrib_type)
    add_children(corresp_action, children)
    return corresp_action


def tei_date(attrib_when="", attrib_from="", attrib_to="",
             attrib_not_before="", attrib_not_after="",
             attrib_evidence=None, attrib_cert=None):
    """
    | create TEI element <date> with @when, @from, @to, @notBefore or @notAfter
    | and (optional) @evidence and @cert
    """
    date = etree.Element("date")
    if attrib_when == attrib_from == attrib_to == \
            attrib_not_before == attrib_not_after and attrib_to == "":
        print("please pass either @when, @from, @to, @notBefore or @notAfter!")
        return None
    add_attrib(date, "when", attrib_when)
    add_attrib(date, "from", attrib_from)
    add_attrib(date, "to", attrib_to)
    add_attrib(date, "notBefore", attrib_not_before)
    add_attrib(date, "notAfter", attrib_not_after)
    if attrib_evidence is not None:
        if attrib_evidence in ["internal", "external", "conjecture"]:
            add_attrib(date, "evidence", attrib_evidence)
        else:
            print("can not set @evidence with given value!")
            print("possible values for @evidence:")
            print("'internal', 'external' or 'conjecture'")
    if attrib_cert is not None:
        if attrib_cert in ["low", "medium", "high", "unknown"]:
            add_attrib(date, "cert", attrib_cert)
        else:
            print("can not set @cert with given value!")
            print("possible values for @cert:")
            print("'high', 'medium', 'low' or 'unknown'")
    return date


def tei_place_name(elem_text, attrib_ref="",
                   attrib_evidence=None, attrib_cert=None):
    """
    | create TEI element <placeName> with given element text, @ref
    | and (optional) @evidence and @cert
    """
    place_name = etree.Element("placeName")
    place_name.text = elem_text
    add_attrib(place_name, "ref", attrib_ref)
    if attrib_evidence is not None:
        if attrib_evidence in ["internal", "external", "conjecture"]:
            add_attrib(place_name, "evidence", attrib_evidence)
        else:
            print("can not set @evidence with given value!")
            print("possible values for @evidence:")
            print("'internal', 'external' or 'conjecture'")
    if attrib_cert is not None:
        if attrib_cert in ["low", "medium", "high", "unknown"]:
            add_attrib(place_name, "cert", attrib_cert)
        else:
            print("can not set @cert with given value!")
            print("possible values for @cert:")
            print("'high', 'medium', 'low' or 'unknown'")
    return place_name


def tei_pers_name(elem_text, attrib_ref="",
                  attrib_evidence=None, attrib_cert=None):
    """
    | create TEI element <persName> with given element text, @ref
    | and (optional) @evidence and @cert
    """
    pers_name = etree.Element("persName")
    pers_name.text = elem_text
    add_attrib(pers_name, "ref", attrib_ref)
    if attrib_evidence is not None:
        if attrib_evidence in ["internal", "external", "conjecture"]:
            add_attrib(pers_name, "evidence", attrib_evidence)
        else:
            print("can not set @evidence with given value!")
            print("possible values for @evidence:")
            print("'internal', 'external' or 'conjecture'")
    if attrib_cert is not None:
        if attrib_cert in ["low", "medium", "high", "unknown"]:
            add_attrib(pers_name, "cert", attrib_cert)
        else:
            print("can not set @cert with given value!")
            print("possible values for @cert:")
            print("'high', 'medium', 'low' or 'unknown'")
    return pers_name


def tei_org_name(elem_text, attrib_ref="",
                 attrib_evidence=None, attrib_cert=None):
    """
    | create TEI element <orgName> with given element text, @ref
    | and (optional) @evidence and @cert
    """
    org_name = etree.Element("orgName")
    org_name.text = elem_text
    add_attrib(org_name, "ref", attrib_ref)
    if attrib_evidence is not None:
        if attrib_evidence in ["internal", "external", "conjecture"]:
            add_attrib(org_name, "evidence", attrib_evidence)
        else:
            print("can not set @evidence with given value!")
            print("possible values for @evidence:")
            print("'internal', 'external' or 'conjecture'")
    if attrib_cert is not None:
        if attrib_cert in ["low", "medium", "high", "unknown"]:
            add_attrib(org_name, "cert", attrib_cert)
        else:
            print("can not set @cert with given value!")
            print("possible values for @cert:")
            print("'high', 'medium', 'low' or 'unknown'")
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


def tostr(element):
    """
    convert given element to str
    """
    return etree.tostring(element).decode().strip()


def pretty(element):
    """
    pretty print given elements
    """
    print(tostr(element))
