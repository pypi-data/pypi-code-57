# coding=utf-8
#
# Copyright © 2011, 2016 Itinken Limited
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

from .attributes import Attributes, AttributeReader
from .token_scanner import TokType


class WikiTable(object):
    def __init__(self, main, lists):
        self.main = main
        self.lists = lists

        # The table stack. Tables can be nested and provide a completely separate context
        # for lists.
        #
        # So for example you can have a nested table containing a set of nested lists in
        # one cell.
        self.tables = []
        pass

    def in_table(self):
        return len(self.tables) > 0

    def parse_table(self, ws, dw):
        """
        Start of a table, set up to parse it.
        """

        # Is this really the start of a table?
        tok = ws.peek_token()
        if tok.get_value() != '{|':
            # No, so ensure we are in a paragraph and output the characters
            self.main.start_para(dw)
            dw.chars(ws.next_value())
            return

        self.lists.end_lists(dw, 0)

        # consume the '{|' symbol
        ws.next_token()

        # read attributes until the end of the line.

        tab = Table()

        self.tables.append(tab)
        atts = self.read_attributes(ws, TokType.EOL, None)

        dw.start_table(atts)
        self.parse_table_rows(tab, ws, dw)
        dw.end_table()

        self.tables.pop()

    def parse_table_rows(self, tab, ws, dw):
        while not tab.finished and not ws.is_end_of_file():
            t = ws.peek_token()
            atts = None
            if "|-" == t.get_value():
                atts = self.read_attributes(ws, TokType.EOL, None)

            dw.start_table_row(atts)
            self.parse_table_cells(tab, ws, dw)
            dw.end_table_row()

    def parse_table_cells(self, tab, ws, dw):
        while not ws.is_end_of_file():
            t = ws.peek_token()
            if t.get_type() == TokType.EOL:
                ws.next_token()
                continue

            if t.get_type() == TokType.SYMBOL:
                val = t.get_value()

                if val == "|}":
                    # When the table is finished we have to let the higher
                    # routines know.
                    ws.next_token()
                    tab.finished = True
                    return

                if val == "|+":
                    # table caption, just ignore for now
                    while ws.next_token().get_type() != TokType.EOL:
                        pass
                    return

                if val == "|-":
                    ws.next_token()
                    ws.skip_space()
                    return

                if val == "|":
                    ws.next_token()  # consume
                elif val == "!":
                    tab.cellType = '!'
                    ws.next_token()  # consume
                else:
                    # an error, eg || at beginning of the line, must always consume the token
                    ws.next_token()

            atts = self.read_attributes(ws, TokType.SYMBOL, "|")
            headerType = (tab.cellType == '!')
            if headerType:
                dw.start_table_header(atts)
            else:
                dw.start_table_cell(atts)

            ws.skip_space()
            tab.parseFinished = False
            while not tab.parseFinished and not ws.is_end_of_file():
                self.main.parse_next(ws, dw)
            self.lists.end_lists(dw, 0)
            if headerType:
                dw.end_table_header()
            else:
                dw.end_table_cell()

    def start_cell(self, dw, val):
        """
        This could be the start of a table cell (normal or header cell).

        If not then just output the characters as they are.
        """
        if len(self.tables) and val == "||":
            dw.end_table_cell()
            dw.start_table_cell(None)
        elif len(self.tables) > 0 and val == "!!":
            dw.end_table_header()
            dw.start_table_header(None)
        else:
            dw.chars(val)

    def end_table(self, ws, dw, c):
        tab = self.tables[-1]
        if tab is None:
            # no active table so this is just an ordinary character
            self.main.start_para(dw)
            self.main.parse_inline(ws, dw)
        else:
            tab.parseFinished = True
            tab.cellType = c

    def read_attributes(self, ws, endType, end):
        """
        Read attributes up until the character given by 'end'.  The
        end character/token is consumed from the input.

        @param endType The token type of the end marker.
        @param end The end character.  It must be on its own such as a
        new line or symbol.
        @return An attributes instance that contains all the attributes found
        that should be used.
        """
        atts = Attributes()

        endTok = ws.find_token_in_line(endType, end, False)
        if endTok is None:
            return atts

        save = endTok.get_type()
        endTok.type = TokType.EOF

        ar = AttributeReader(ws)
        atts = ar.read_attributes()

        endTok.type = save
        ws.next_token()  # consume the end character
        return atts


class Table(object):
    """
    Used to keep track of tables.  Tables have an explicit end marker and
    so are not too difficutlt to keep track of.
    """

    def __init__(self):
        self.parseFinished = False
        self.finished = False
        self.cellType = None
