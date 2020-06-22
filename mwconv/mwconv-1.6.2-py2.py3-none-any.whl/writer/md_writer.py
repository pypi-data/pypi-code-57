# coding=utf-8
#
# Copyright © 2013, Steve Ratcliffe, Itinken Limited
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
#
from __future__ import print_function
from __future__ import unicode_literals

from .extensions import SyntaxExtension
from ..base import TextBase
from ..wikilist import WikiList


class MdWriterLocal(TextBase):
    """
    A helper class for the markdown writer.

    Contains methods that are not callback methods from the parser, but that
    are not general enough to go into TextBase.
    """
    def push_list(self, kind):
        level = len(self.lists)
        li = MdList(level, kind)
        self.lists.append(li)


class MdSyntax(SyntaxExtension, TextBase):
    def start_syntax(self, lang=None):
        self.ensure_gap()
        self.chars('```%s' % lang)

    def end_syntax(self, lang=None):
        self.chars('```\n')


class MdWriter(MdWriterLocal, MdSyntax):
    """
    Writer for standard markdown.

    This class contains only the callback routines.
    """

    def __init__(self, out):
        super(MdWriter, self).__init__(out)
        self.in_para = True

    def start_header(self, n):
        self.ensure_gap()
        self.write(n * '#')
        self.write(' ')

    def end_header(self, n):
        self.writenl()

    def start_para(self):
        if self.in_list_item and self.in_para:
            self.write('</p>')
        self.in_para = True
        if self.in_list_item:
            self.write('<p>')
        else:
            self.ensure_gap()

    def end_para(self):
        self.in_para = False
        if self.in_list_item:
            self.write('</p>')
        else:
            self.ensure_bol()

    def start_unordered(self):
        self.ensure_bol(True)
        if not self.in_list_item:
            self.writenl()
        self.push_list('*')

    def end_unordered(self):
        self.pop_list()
        self.ensure_bol()

    def start_ordered(self):
        # list need a blank line to separate them from a paragraph
        self.ensure_bol()
        if not self.in_list_item:
            self.writenl()
        self.push_list('1')

    def end_ordered(self):
        self.pop_list()
        self.ensure_bol()

    def start_def_list(self):
        self.write('<dl>')
        self.push_list(';')

    def end_def_list(self):
        self.pop_list()
        self.ensure_bol()
        self.write('</dl>')

    def start_list_item(self, li):
        self.ensure_bol(True)
        self.in_list_item = True
        kind = li.get_item_kind()
        top = self.get_current_list()
        if kind in (WikiList.UNORDERED, WikiList.TERM, WikiList.ORDERED):
            # Indent by 4 spaces for each indent level
            self.write(top.level * '    ')
            self.write(top.tag())
            self.write(' ')
        elif kind == WikiList.DEF:
            self.write('<dd>')
        else:
            assert False
        self.skip_space = True

    def end_list_item(self, kind):
        self.in_list_item = False
        self.ensure_bol()

    def start_block(self, fill, wiki, atts=None):
        if not fill:
            self.block_fill = fill
            self.start_para()
            self.out.start_capture()

    def end_block(self, fill, wiki):
        if not fill:
            b = self.out.end_capture()
            self.write(b.format(prefix='    '))

    def start_link(self, href, auto_link):
        self.write('[')
        if auto_link:
            self.write(auto_link)
        self.link_save = href

    def end_link(self):
        self.write(']')
        self.write('(%s)' % self.link_save)

    def start_style(self, tag, is_block, atts):
        # Note will have to deal with extra spaces which are not allowed in markdown
        if tag == 'b':
            self.write('**')
        elif tag == 'i':
            self.write('_')

    def end_style(self, tag, is_block):
        if tag == 'b':
            self.write('**')
        elif tag == 'i':
            self.write('_')

    def end_document(self):
        self.out.pend_gap = False
        self.ensure_bol()

    def one_char(self, c):
        assert len(c) == 1
        self.write(c)

    def chars(self, s):
        if self.pending_new_line:
            self.writenl()

        # Since this is text and not markup, we can escape characters that might be
        # taken for markup by md. XXX check in code blocks later.
        # Since all the major users of markdown disable this anyway,
        # don't do this for now.
        #if s == '_':
        #    s = r'\_'

        self.write(s)


class MdList(object):
    def __init__(self, level, kind):
        self.level = level
        self.kind = kind
        self.count = 0

    def tag(self):
        if self.kind == '*':
            return '*'
        elif self.kind == '1':
            self.count += 1
            return '%d.' % self.count
        elif self.kind == ';':
            return '<dt>'
