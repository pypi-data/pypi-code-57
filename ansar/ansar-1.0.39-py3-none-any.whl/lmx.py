# Author: Scott Woods <scott.suzuki@gmail.com>
# MIT License
#
# Copyright (c) 2017, 2018, 2019, 2020 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Implementation of the XML codec. Refer to;

* https://www.w3.org/XML/
* https://en.wikipedia.org/wiki/XML


.. autoclass:: CodecXml

.. autofunction:: word_to_xml

.. autofunction:: xml_to_word
"""
__docformat__ = 'restructuredtext'

import base64
import uuid
import types

#
#
from xml.etree.ElementTree import Element, SubElement
from defusedxml.ElementTree import parse, ParseError
from defusedxml.ElementTree import fromstring, tostring
from defusedxml import DTDForbidden, EntitiesForbidden, ExternalReferenceForbidden

from xml.dom import minidom
#from xml.etree.ElementTree import SubElement #, tostring

from .memory import *
from .convert import *
from .runtime import *
from .message import *
from .codec import *


__all__ = [
    'word_to_xml',
    'xml_to_word',
    'CodecXml'
]

# Transform word to tree of XML elements.
#def w2e_pass(c, p, t):
#    return p

def w2e_bool(c, w):
    e = Element('boolean')
    if w:
        v = 'true'
    else:
        v = 'false'
    e.set('value', v)
    return e

def w2e_int(c, w):
    e = Element('integer')
    e.set('value', '%d' % (w,))
    return e

def w2e_float(c, w):
    e = Element('float')
    e.set('value', '%f' % (w,))
    return e

def w2e_str(c, w):
    e = Element('string')
    e.text = w
    return e

def w2e_list(c, w):
    e = Element('list')
    for i, a in enumerate(w):
        s = word_to_element(c, a)
        e.append(s)
    return e

def w2e_dict(c, w):
    e = Element('message')
    for k, v in w.items():
        s = word_to_element(c, v)
        s.set('name', k)
        e.append(s)
    return e

def w2e_none(c, w):
    e = Element('null')
    return e

# Map the python+memory pair to a dedicated
# transform function.
w2e = {
    bool: w2e_bool,
    int: w2e_int,
    float: w2e_float,
    str: w2e_str,
    list: w2e_list,
    dict: w2e_dict,
    NoneType: w2e_none,
}

def word_to_element(c, w):
    '''
    Transform the generic data to rather
    inconvenient XML form.
    '''
    try:
        a = getattr(w, '__class__')
    except AttributeError:
        a = None
    
    if a is None:
        raise TypeError('word with specification "%s" is unusable' % (b.__name__,))

    try:
        f = w2e[a]
    except KeyError:
        raise TypeError('no transformation for data/specification %s/%s' % (a.__name__, b.__name__))

    # Apply the transform function
    return f(c, w)

# Generate XML text representation of a
# generic word.
def word_to_xml(c, w):
    '''
    Generate the XML representation of a generic word.

    If the codec `pretty_format` property is true, this
    function will produce a more human-readable rendering
    of XML.

    Parameters:

    - `c`, the active codec.
    - `w`, the generic word to be represented.

    Returns:

    A string containing valid XML.
    '''
    # Yet another representation :-(
    # Application to generic to
    # Element (tree) to text.
    e = word_to_element(c, w)

    # But wait... More silliness to
    # get a industry-standard library
    # to add the XML declaration and
    # perform a pretty-print.
    elementary = tostring(e, 'utf-8')
    reparsed = minidom.parseString(elementary)
    # Cant use defused parser here.
    # toprettyxml method doesnt exist.
    # reparsed = fromstring(rough)
    if c.pretty_format:
        return reparsed.toprettyxml(indent="  ")
    return reparsed.toxml()

# Decoding - from parsing of JSON to transformation
# into app data items.

def xml_to_word(c, x):
    '''
    Produce a generic word from the parsing of a
    text XML representation.
     
    Parameters:

    - `c`, the active codec.
    - `x`, the XML text.

    Returns:

    A generic word.
    '''
    try:
        e = fromstring(x, forbid_dtd=True, forbid_entities=True, forbid_external=True)
    except ParseError as t:
        raise ValueError(str(t))
    except DTDForbidden as t:
        raise ValueError(str(t))
    except EntitiesForbidden as t:
        raise ValueError(str(t))
    except ExternalReferenceForbidden as t:
        raise ValueError(str(t))

    w = element_to_word(c, e)
    return w

# From generic data (after parsing) to final python
# representation in the application.

def e2w_boolean(c, e):
    v = e.get('value')
    return v == 'true'

def e2w_integer(c, e):
    v = e.get('value')
    return int(v)

def e2w_float(c, e):
    v = e.get('value')
    return float(v)

def e2w_string(c, e):
    return e.text

def e2w_list(c, e):
    v = [element_to_word(c, s) for s in e]
    return v

def e2w_message(c, e):
    v = {s.get('name'): element_to_word(c, s) for s in e}
    return v

def e2w_null(c, w):
    return None

#
#
e2w = {
    'boolean': e2w_boolean,
    'integer': e2w_integer,
    'float': e2w_float,
    'string': e2w_string,
    'list': e2w_list,
    'message': e2w_message,
    'null': e2w_null,
}

#
#
def element_to_word(c, e):
    '''
    '''
    a = e.tag     # The XML element.

    try:
        f = e2w[a]
    except KeyError:
        raise TypeError('no transformation for data/specification %s/%s' % (a, b.__name__))

    return f(c, e)

# Define the wrapper around the JSON encoding
# primitives.
class CodecXml(Codec):
    '''Encoding and decoding of XML representations.

    This class is an alternative to the :ref:`JSON codec<codec-json>`, in those
    places where an ``encoding`` parameter is passed into the library.
    '''
    EXTENSION='xml'

    def __init__(self, return_proxy=None, local_termination=None, pretty_format=False, decorate_names=True):
        Codec.__init__(self,
            CodecXml.EXTENSION,
            word_to_xml,
            xml_to_word,
            return_proxy, local_termination, pretty_format, decorate_names)
