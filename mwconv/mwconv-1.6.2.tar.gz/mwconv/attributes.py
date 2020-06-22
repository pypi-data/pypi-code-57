# coding=utf-8
#
# Copyright © 2011, 2015 Itinken Limited
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function
from __future__ import unicode_literals

import six

from .token_scanner import TokType

allowed_attributes = [
    'abbr', 'align', 'alt', 'axis', 'bgcolor', 'border', 'cellpadding',
    'cellspacing',
    'char', 'charoff', 'cite', 'class', 'clear', 'col', 'colgroup', 'color',
    'colspan',
    'datetime', 'dir', 'face', 'frame', 'headers', 'height', 'href', 'id',
    'lang', 'noshade',
    'nowrap', 'rbspan', 'ref', 'rel', 'rowspan', 'rules', 'scope', 'size',
    'src', 'start',
    'style', 'summary', 'title', 'type', 'valign', 'value', 'width',

]


class Attribute(object):
    def __init__(self, key, value):
        self.key = key.strip()
        self.value = value


class Attributes(object):
    def __init__(self):
        self.atts_map = {}
        self.invalid_atts = {}

    def add(self, att):
        if att.key in allowed_attributes:
            self.atts_map[att.key] = att
        else:
            self.invalid_atts[att.key] = att

    def __iter__(self):
        return six.itervalues(self.atts_map)

    def pop(self, name, d=None):
        return self.atts_map.pop(name, d)

    def get(self, attname, value=None):
        """
        Get the value of the given attribute name, or the default value given.
        """
        att = self.atts_map.get(attname)
        if att:
            return att.value or value
        else:
            return value

    def has_invalid(self, attname):
        return self.invalid_atts.get(attname, self.atts_map.get(attname, None))

    def get_invalid(self, attname):
        att = self.atts_map.get(attname, self.invalid_atts.get(attname, None))
        if att:
            return att.value
        else:
            return None


class AttributeReader(object):
    """
    Read attributes.

    Since this doesn't fit well with the wiki text parsing, we deal in single characters
    rather than tokens.
    """

    def __init__(self, ws):
        self.ws = ws
        self.fill_token()
        self.tokind = 0

    def fill_token(self):
        """
        Get the next token so that we can start reading characters from it.
        """
        if self.ws.first_token_type() == TokType.EOF:
            self.current = self.ws.peek_token()
        else:
            self.current = self.ws.next_token()

    def read(self):
        """
        Reads a single character from the current token.
        """
        while not self.is_end_of_file() and self.tokind >= len(
                self.current.value):
            self.fill_token()
            self.tokind = 0

        if self.is_end_of_file():
            return None

        c = self.current.value[self.tokind]
        self.tokind += 1
        return c

    def is_end_of_file(self):
        return self.current.type == TokType.EOF

    def read_attributes(self):
        atts = Attributes()

        while not self.is_end_of_file():
            att = self.read_attribute()
            if not att:
                break
            atts.add(att)

        return atts

    def read_attribute(self):
        """
        Read a single attribute.

        Has to work with either kind of quoting and the special characters
        that can be in an attribute value.
        """
        key = []
        val = []

        while not self.is_end_of_file():
            c = self.read()
            if c is None:
                return None

            if c == '=':
                break
            key.append(c)

        c = self.read()
        if c is None:
            return None

        if c == '\'' or c == '"':
            quotec = c
        else:
            quotec = None
            val.append(c)

        while not self.is_end_of_file():
            c = self.read()
            if c is None or c == quotec or (
                    quotec is None and c in (' ', '\t')):
                break
            if c == '&':
                c = self.read_entity()
            val.append(c)

        return Attribute(''.join(key), ''.join(val))

    def read_entity(self):
        ws = self.ws
        text = ''
        while not ws.is_end_of_file():
            c = self.read()
            if c is None or c == ';':
                break
            text += c

        if text[0:2] == '#x' or text[0:2] == '#X':
            d = int(text[2:], 16)
            c = chr(d)
        elif text[0] == '#':
            c = chr(int(text[1:]))
        elif text == 'amp':
            c = '&'
        elif text == 'quot':
            c = '"'
        elif text == 'lt':
            c = '<'
        elif text == 'gt':
            c = '>'
        else:
            c = '?'

        return c
