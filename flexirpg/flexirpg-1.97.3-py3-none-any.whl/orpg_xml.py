# Copyright (C) 2000-2001 The OpenRPG Project
#
#        openrpg-dev@lists.sourceforge.net
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# --
#
# File: orpg_xml.py
# Author: Chris Davis
# Maintainer:
# Version:
#   $Id: orpg_xml.py,v 1.12 2007/07/19 20:33:10 digitalxero Exp $
#
# Description: xml utilies
#

import xml.dom
import string
import traceback
import sys

def toxml(root,pretty=0):
    if pretty:
        return root.toprettyxml(indent='  ')
    else:
        return root.toxml()

def _strip_text_nodes(node):
    child = node.firstChild
    while child:
        next_child = child.nextSibling
        if child.nodeType == xml.dom.Node.TEXT_NODE:
            child.data = child.data.strip()
            if child.data == "":
                node.removeChild(child)
        else:
            _strip_text_nodes(child)
        child = next_child

def _parse_xml(parse_func, parse_param):
    try:
        doc = parse_func(parse_param)
        doc.normalize()
        _strip_text_nodes(doc)
        return doc
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return None

def parseXml(s):
    return _parse_xml(xml.dom.minidom.parseString, s.encode('utf-8'))

def parse_file(filename):
    return _parse_xml(xml.dom.minidom.parse, filename)

def safe_get_text_node(xml_dom):
    """ returns the child text node or creates one if doesnt exist """
    t_node = xml_dom.firstChild
    if t_node == None:
        doc = xml_dom
        while doc.nodeType != xml.dom.Node.DOCUMENT_NODE:
            doc = doc.parentNode
        t_node = doc.createTextNode("")
        t_node = xml_dom.appendChild(t_node)
    return t_node

def bool_attrib(xml_dom, attrib_name, default_if_missing):
    """Get an XML attribute as a bool.

    Returns:
       The XML attribute converted to a bool, or 'default_if_missing'
       if the attribute does not exist.
    """
    if xml_dom.hasAttribute(attrib_name):
        attrib = xml_dom.getAttribute(attrib_name)
        return attrib.lower() == "true" or attrib == "1"
    else:
        return default_if_missing
