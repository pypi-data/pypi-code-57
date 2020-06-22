# coding=utf-8
#
# Copyright © 2011,2016 Itinken Limited
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

import string

from six import StringIO

from mwconv.writer.html_writer import HtmlWriter
from . import table, wikilist
from .attributes import AttributeReader
from .token_scanner import WikiScanner, TokType

DEFAULT_BLOCK_TAGS = (
    "div", "pre",
    "ul", "ol", "li", "p",
    "dl", "dd", "dt",
    "pre",
)

DEFAULT_INLINE_TAGS = (
    "span",
    "code", "tt",
    "strong", "em", "i", "b", "kbd", "var", "samp",
    "var", "sub", "sup", "small",
    "br", "hr",
    "nowiki",
    "img",
    "blockquote",
    "cite",
)

DEFAULT_URL_SCHEMES = (
    '/',
    'http',
    'https',
)


class WikiParse(object):
    """
    A parser for mediawiki-like wiki text.  It is designed to produce nice-looking output.

    This is an event based parser, the input is read token by token and events are
    generated through the DocumentWriter interface.  It keeps some state for
    constructs that span several lines.

    It implements most of the formatting operations that you might want to use to
    format a page that is not part of a wiki. There is no templating for example
    or referencing other wiki pages.
    """

    def __init__(self, first_level=None):
        self.lists = wikilist.WikiLists(self)
        self.tables = table.WikiTable(self, self.lists)

        # If set, act more like mediawiki
        self.strict_mw = False  # not working yet

        # Paragraphs can't nest, so track if we are in one
        self.in_para = False
        self.end_para_pending = False  # pending end paragraph

        self.next_link_number = 1

        self.allowed_block_tags = DEFAULT_BLOCK_TAGS
        self.allowed_inline_tags = DEFAULT_INLINE_TAGS
        self.allowed_url_schemes = DEFAULT_URL_SCHEMES

        # TODO way to add extension tags
        self.allowed_block_tags += ('syntaxhighlight', )

        self.first_level = int(first_level) if first_level else None
        self.header_offset = 0
        self.title = None

    def parse_to_html(self, r):
        sb = StringIO()
        doc = HtmlWriter(sb)
        self.parse(r, doc)
        return sb.getvalue()

    def parse(self, r, doc):
        """
        Top level public parse routine.
        @param r A reader implementation that gives the wiki text.  It should be buffered
        if coming from a file.
        @param doc A document output object
        """
        ws = WikiScanner(r)

        doc.block_tags = self.allowed_block_tags
        doc.inline_tags = self.allowed_inline_tags

        while ws.first_token_type() == TokType.EOL:
            ws.next_token()

        while not ws.is_end_of_file():
            self.parse_next(ws, doc)
        self.lists.end_lists(doc, 0)
        doc.end_document()

    def parse_next(self, ws, dw):
        """
        Parse a block level element.  We can always tell from the first character of
        a line what kind of block this is going to be.  Or at least by looking at the first
        part of the line.

        The blocks are then parsed by separate routines.  No tree is built up, events are
        emmited as soon as a construct is recognised.

        The lists stack is used to keep track of the list level.  The bold/italic styles
        can also nest, although I never do that, so that will be implemented later.
        """
        c = ws.peek_char()
        if c == 0:
            return

        if c == '\n':  # end of para
            ws.next_token()
            if self.end_para_pending:
                self.lists.end_lists(dw, 0)
            self.end_para_pending = True
        elif c == '=':  # header start
            self.parse_header(ws, dw)
        elif c == ' ':
            self.parse_block(ws, dw, False, True)
        elif c in ('*', '#', ';', ':'):  # lists
            self.lists.parse_list(ws, dw)
            self.end_para_pending = False
        elif c == '<':
            self.parse_tag(ws, dw, ws.next_value())
            self.parse_inline(ws, dw)
        elif c == '{':
            self.tables.parse_table(ws, dw)
        elif c in ('|', '!'):
            self.tables.end_table(ws, dw, c)
        else:
            # everything else is just inline text
            if not self.lists.in_list or self.end_para_pending:
                self.start_para(dw)
            self.parse_inline(ws, dw)

    def parse_block(self, ws, dw, fill=True, wiki=True, tag=None, atts=None):
        """
        A section that may preserve new-lines and prevent wiki formatting.

        An indented block is fill=False, wiki=True. A pre tag
        is fill=False, wiki=False and nowiki tag is just wiki=False.

        @param fill If true, the the output is filled, else new lines are preserved.
        @param wiki If true, wiki formatting characters are interpreted within the block,
        otherwise all text is literal.
        """

        if self.strict_mw:
            self.lists.end_lists(dw, 0)

        if not fill:
            self.end_para(dw)

        # If there is a start tag, then find the matching end tag
        end = None
        if tag:
            end = ws.find_end_tag(tag)
            end.type = TokType.EOF

        dw.start_block(fill, wiki, atts)
        while not ws.is_end_of_file():
            if wiki:
                # If we are wiki formatting, then parse one line and
                # see if the next starts with white space too.
                if ws.first_token_type() == TokType.SPACE:
                    dw.chars(ws.next_value()[1:])

                self.parse_inline(ws, dw)
                c = ws.peek_char()
                if ws.is_end_of_file():
                    break
                if c == '\n' or c not in string.whitespace:
                    break
            else:
                t = ws.next_token()
                if t.get_type() != TokType.IGNORE:
                    dw.chars(t.get_value())

        if tag:
            end.type = TokType.SYMBOL
            ws.next_token()
            ws.next_token()
            ws.next_token()

        dw.end_block(fill, wiki)

    def start_para(self, dw):
        """
        A paragraph.  Note that in HTML (and therefore in this wikitext) paras
        can only hold inline elements, so any open block element is closed by
        a start of paragraph.

        There is only a paragraph start if one is not already active.
        """
        if self.end_para_pending:
            self.end_para(dw)
        if not self.in_para and len(self.tables.tables) == 0:
            self.lists.end_lists(dw, 0)
            dw.start_para()
            self.in_para = True

    def end_para(self, dw):
        """
        End a paragraph if we are in one.  Else do nothing so it can be called
        whenever we want to be sure that paragraphs are finised.
        """

        if self.in_para:
            dw.end_para()
            self.in_para = False
        self.end_para_pending = False

    def parse_header(self, ws, dw):
        """
        A heading.  Starts with a number of '=' chars.  Never spans lines, but can
        contain inline formatting.
        """
        self.lists.end_lists(dw, 0)
        h = ws.next_value()

        # Its not really a header unless the string occurs later in the line.
        t = ws.find_token_in_line(TokType.SYMBOL, h, False)

        if t is not None:
            t.type = TokType.IGNORE

            n = len(h)
            if self.first_level:
                self.header_offset = self.first_level - n
                self.first_level = None

            ws.skip_space()
            dw.start_header(n + self.header_offset)
            if not self.title:
                # Collect the text for the first header which we will use as the title
                class DocTextCollector(object):
                    def __init__(self, dw):
                        self.dw = dw
                        self.textarr = []

                    def chars(self, s):
                        self.dw.chars(s)
                        self.textarr.append(s)

                    def __getattr__(self, item):
                        return getattr(self.dw, item)

                    def __unicode__(self):
                        return u' '.join(self.textarr)

                dw = self.title = DocTextCollector(dw)

            self.parse_inline(ws, dw)
            dw.end_header(n + self.header_offset)
        else:
            # just send the characters as they are
            dw.chars(h)

    def parse_inline(self, ws, dw):
        """
        Parse all the inline styles and constructs.
        """
        while not ws.is_end_of_file():
            t = ws.next_token()

            if t.get_type() == TokType.EOL:
                dw.set_pending_newline()
                break

            typ = t.get_type()
            if typ == TokType.SPACE:
                dw.one_char(' ')
            elif typ == TokType.SYMBOL:
                self.parse_inline_symbol(ws, dw, t)
            elif typ == TokType.TEXT:
                dw.chars(t.get_value())
            elif typ == TokType.END_BOLD:
                dw.end_style("b", False)
            elif typ == TokType.END_ITALIC:
                dw.end_style("i", False)
            elif typ == TokType.END_LINK:
                dw.end_link()
            elif typ == TokType.EOF:
                pass
            elif typ == TokType.EOL:
                pass
            elif typ == TokType.IGNORE:
                pass
            elif typ == TokType.IGNORABLE_END_TAG:
                ws.next_token()
                ws.next_token()

    def parse_inline_symbol(self, ws, dw, start):
        """
        Called to deal with a symbol found in the input stream.  Mostly symbols
        are just output as-is, but some are recognised by the parser and
        are converted to markup.

        @param start The token the caused this routine to be called.
        """

        val = start.get_value()
        c = val[0]
        if c == '\'':
            self.parse_quotes(ws, dw, val)
        elif c == '[':  # a link
            self.parse_link(ws, dw, val)
        elif c == '|':  # maybe a table separator
            self.tables.start_cell(dw, val)
        elif c == '!':  # maybe a table separator
            self.tables.start_cell(dw, val)
        elif c == '<':  # maybe html or just a plain less than sign
            self.parse_tag(ws, dw, val)
        else:
            dw.chars(val)

    def parse_tag(self, ws, dw, val):
        """
        Mediawiki can contain html tags.  There is some filtering of what is
        allowed as well.

        Tags have to be complete and within a range of known tags
        to be recognised.  If not then the literal text will be output.

        This allows you to write things like 1 < 2 without having to use
        entities.

        @param val The value of the tag that caused us to be called.  It will therefore
        start with an opening angle bracket, but might be longer.
        """

        if self.end_para_pending:
            self.end_para(dw)

        valid = False
        block = True
        opening = True

        # May be a closing or opening tag.  But if it does not have the right
        # syntax for a tag then it is just literal text.
        next_type = ws.first_token_type()
        tag = ws.peek_token().get_value()
        if val == "<":
            opening = True
        elif val == "</":
            opening = False

        if next_type == TokType.TEXT:
            ltag = tag.lower()
            if ltag in self.allowed_block_tags:
                valid, block = True, True
            elif ltag in self.allowed_inline_tags:
                valid, block = True, False

        # We also need to have the closing bracket or else it is still not
        # valid.  Not sure what the conditions are here.
        end = None
        if valid:
            end = ws.find_token(TokType.SYMBOL, ">")
            if end is None:
                valid = False

        if not valid:
            # just a literal opening angle bracket
            dw.chars(val)
            return

        # Ok now we are committed, get the tag word and attributes.
        tag = ws.next_value()

        # Mark the closing bracket and read attributes
        atts = None
        if opening:
            end.type = TokType.EOF
            ar = AttributeReader(ws)
            atts = ar.read_attributes()
            end.type = TokType.IGNORE

        ext = self.parse_extension_tag(tag, atts, ws, dw, opening)
        if ext:
            if ext.is_done:
                return

            self.parse_block(ws, dw, ext.fill, ext.wiki, ext.tag, atts)
            return

        # The closing bracket
        ws.next_value()

        # If not a block element then we need to ensure that we are in a paragraph.
        if opening and not block and not self.lists.in_list:
            self.start_para(dw)

        # Likewise if we have a block element, then a para must be closed (if open).
        if block:
            self.end_para(dw)

        # There are some special cases.
        if tag.lower() == "pre":
            assert opening
            self.parse_block(ws, dw, False, False, 'pre', atts)
        elif tag.lower() == "nowiki":
            assert opening
            self.parse_block(ws, dw, True, False, 'nowiki', atts)
        elif tag.lower() == 'p':
            if opening:
                dw.start_para()
            else:
                dw.end_para()
        else:
            if opening:
                dw.start_style(tag, block, atts)
            else:
                dw.end_style(tag, block)

    def parse_link(self, ws, dw, val):
        """
        Parse a link item, that is something that starts with a '['.  This could
        be just a plain character or the start of an internal or external link.
        """
        l = len(val)
        if l == 1:  # external link
            self.parse_ext_link(ws, dw, val)
        elif l == 2:  # internal link, or not a link
            pass  # TODO
        else:
            pass  # not a link

    def parse_ext_link(self, ws, dw, val):
        """
        Parse an external link.

        If it doesn't have the correct format, then it is not a link and the characters
        should be output literally.
        """

        nextval = ws.peek_token().get_value()
        if nextval not in self.allowed_url_schemes:
            dw.chars(val)
            return

        end = ws.find_token_in_line(TokType.SYMBOL, "]", False)
        if end is None:
            # not a link, because no closing bracket
            dw.chars(val)
        else:
            end.type = TokType.END_LINK
            href, auto_link = self.extract_ext_link(ws)
            dw.start_link(href, auto_link)

    def extract_ext_link(self, ws):
        """
        Extract the external link by re-joining all the tokens until we see a space
        or the end of the link.  If there is no space, then we auto generate some
        link text like '[1]'
        """
        href = []
        auto_link = None
        while not ws.is_end_of_file():
            t = ws.next_token()
            val = t.get_value()

            typ = t.get_type()
            if typ == TokType.TEXT:
                href.append(val)
            elif typ == TokType.SYMBOL:
                href.append(val)
            elif typ == TokType.END_LINK:
                has_text = False
                ws.insert_token_before(t, None)

                auto_link = "[" + str(self.next_link_number) + "]"
                self.next_link_number += 1
                break
            else:
                break

        return ''.join(href), auto_link

    def parse_quotes(self, ws, dw, val):
        """
        Parse quoted sections that will be bold or italic.  This is quite
        difficult as the open tag is the same as the close and both tags
        are made out of single quotes.

        You can do things like this:

        <pre>
        '''''hello'' world'''
        B I hello /I /B

        '''''hello''' world''
        I B hello /B /I

        '''hello'''''world''
        B hello /B I world /I
        </pre>
        In other words if there are 5 quotes together they could be ''' followed by ''
        or the other way round and each could be opening or closing versions.

        The best thing is to just use <b> and <i> in any situation where it
        could get tricky.
        """
        l = len(val)
        if l == 1:  # this is just a regular single quote
            dw.one_char('\'')
        elif l == 2:
            # TODO deal with '''''
            end = ws.find_token_in_line(TokType.SYMBOL, val, True)
            end.type = TokType.END_ITALIC
            dw.start_style("i", False, None)
        elif l == 3:
            end = ws.find_token_in_line(TokType.SYMBOL, val, True)
            end.type = TokType.END_BOLD
            dw.start_style("b", False, None)
        else:
            # this is more complex - leave till later as I don't use it.
            dw.chars(val)

    def parse_extension_tag(self, tag, atts, ws, dw, opening):
        class Ext:
            def __init__(self, tag=None):
                self.tag = tag
                self.is_done = False
                self.fill = True
                self.wiki = True

        ext = None
        if tag == 'syntaxhighlight' or tag == 'pre' and atts.has_invalid('code'):
            if not hasattr(dw.extensions, 'syntax'):
                ext = Ext()
                ext.tag = tag
                ext.fill = False
                ext.wiki = False
                atts.pop('code', None)
                atts.pop('lang', None)
            else:
                ext = Ext()
                ext.is_done = True
                if tag == 'syntaxhighlight':
                    lang = atts.get('lang')
                else:
                    lang = atts.get_invalid('code')

                end = ws.find_end_tag(tag)
                end.type = TokType.EOF

                dw.start_syntax(lang)
                while not ws.is_end_of_file():
                    t = ws.next_token()
                    if t.get_type() != TokType.IGNORE:
                        dw.chars(t.get_value())
                dw.end_syntax(lang)

                end.type = TokType.SYMBOL
                ws.next_token()
                ws.next_token()
                ws.next_token()

        return ext
