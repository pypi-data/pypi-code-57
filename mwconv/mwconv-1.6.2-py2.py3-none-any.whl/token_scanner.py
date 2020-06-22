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

import string


class Token(object):
    def __init__(self, typ, val=None):
        self.type = typ
        self.value = val

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

    def is_white_space(self):
        return self.type == TokType.SPACE or self.type == TokType.EOL


class TokType(object):
    SYMBOL = 1
    TEXT = 2
    SPACE = 3
    EOL = 4
    EOF = 5

    # the following are set during parsing to distinguish ambiguous situations.
    END_BOLD = 6
    END_ITALIC = 7
    END_LINK = 8
    IGNORE = 9
    IGNORABLE_END_TAG = 10


NO_PUSHBACK = None

# Symbols that can introduce a list item
LIST_SYMBOLS = ('*', '#', ';', ':')

# All multi character symbols
SYMBOLS = {'=', '==', '===', '====', '=====', '======', '{|', '|}', '|-', '|+', '||', '!!', '</', "''", "'''"}


class WikiScanner(object):
    """
     * A tokenizer for wiki text reading.
     *
     * @author Steve Ratcliffe
    """

    def __init__(self, reader):
        self.reader = reader
        self.pushback = NO_PUSHBACK
        self.is_eof = False
        self.tokens = list()

    def peek_char(self):
        t = self.peek_token()
        val = t.get_value()
        if val is None:
            return 0
        else:
            return val[0]

    def first_token_type(self):
        self.ensure_tok()
        return self.tokens[0].get_type()

    def peek_token(self):
        if not len(self.tokens):
            self.file_tok()
        return self.tokens[0]

    def next_token(self):
        if not len(self.tokens):
            return self.read_tok()
        else:
            return self.tokens.pop(0)

    def next_value(self):
        return self.next_token().get_value()

    def find_token_in_line(self, type, val=None, create=False):
        """
        Find a token of the given type before the end of the line.

        If the optional val argument is given, then the found token
        has to have the given value as well as the given type.

        If the end of the line is reached and the token has not
        been found and 'create' is set, then create the token, just
        before the end of line.

        The tokens are not consumed.

        The found (or created) token is returned.
        """
        found = None
        saved = []
        while 1:
            t = self.next_token()
            saved.append(t)
            if t.get_type() == type:
                if val is None:
                    found = t
                    break
                elif t.get_value() == val:
                    found = t
                    break

            if t.get_type() == TokType.EOL:
                break

        if create and found is None:
            found = Token(type)
            found.value = val
            saved.insert(-1, found)

        self.tokens[0:0] = saved
        return found

    def find_token(self, type, val=None):
        """
        Find a token with the given type and (optionally) value.

        This will search through the whole file if necessary.
        """
        found = None
        saved = []
        while not found:
            t = self.next_token()
            saved.append(t)
            if t.type == type:
                if val is None:
                    found = t
                elif t.value == val:
                    found = t
        self.tokens[0:0] = saved  # replace the ones we have searched through
        return found

    def find_end_tag(self, tag):
        """
        Find the end tag with the given name.

        Does not deal with the case where the same tag ocurrs nested.
        If not found then None is returned.
        Otherwise the token that starts the end tag is returned (but what use is that?).
        """
        found = None
        saved = []
        while not self.is_end_of_file():
            start = self.next_token()
            saved.append(start)
            if start.type == TokType.SYMBOL and start.value == "</":
                if not self.is_end_of_file():
                    t = self.next_token()
                    saved.append(t)
                    if t.type == TokType.TEXT and t.value == tag:
                        if not self.is_end_of_file():
                            t = self.next_token()
                            saved.append(t)
                            if t.get_type() == TokType.SYMBOL and t.get_value() == ">":
                                found = start
                                break

        # Replace the tokens we took
        self.tokens[0:0] = saved
        return found

    def insert_token_before(self, tok, before):
        if before is None:
            self.tokens.insert(0, tok)
            return

        ind = 0
        for t in self.tokens:
            if t == before:
                self.tokens.insert(ind, tok)
                break

            ind += 1

    def skip_space(self):
        while len(self.tokens) and self.tokens[0].is_white_space():
            self.tokens.pop(0)

        # If the list is empty, directly consume white space
        if not len(self.tokens):
            c = NO_PUSHBACK
            while not self.is_end_of_file():
                c = self.read_char()
                if not self.is_space(c):
                    break

            self.pushback = c

    def is_end_of_file(self):
        if not len(self.tokens):
            return self.is_eof
        else:
            return self.tokens[0].get_type() == TokType.EOF

    def ensure_tok(self):
        if not len(self.tokens):
            self.file_tok()

    def file_tok(self):
        t = self.read_tok()
        self.tokens.append(t)

    def read_tok(self):
        """
        Read a token from the input stream.  There are only a few
        kinds of token that are recognised on input.  Other token
        types are recognised or constructed later on.

        @return A token.  Never returns null or throws an exception.
        Once end of file or an error occurs the routine will always return EOF.
        """
        if self.is_eof:
            return Token(TokType.EOF)

        c = self.read_char()

        if c is None:
            self.is_eof = True
            return Token(TokType.EOF)

        val = []
        val.append(c)

        if c == '\n':
            tt = TokType.EOL
        elif c == '\r':
            # normalise \r\n and \r to \n
            tt = TokType.EOL
            c = self.read_char()
            val = ['\n']
            if c != '\n':
                self.pushback = c

        elif self.is_space(c):
            c = self.read_char()
            while self.is_space(c) and c != '\n':
                val.append(c)
                c = self.read_char()

            self.pushback = c
            tt = TokType.SPACE
        elif self.is_word_char(c):
            c = self.read_char()
            while self.is_word_char(c):
                val.append(c)
                c = self.read_char()
            self.pushback = c
            tt = TokType.TEXT
        else:
            # A symbol.  Some symbols consist of more than one character or are treated as so
            # by the code. It does not matter that symbols are recognised as a combined symbol outside
            # of the context where they would be recognised, but it is important not to combine symbols
            # that should not be combined.
            if self.is_combining_symbol(c):
                oc = c
                c = self.read_char()
                while self.is_symbol(c):
                    if oc in LIST_SYMBOLS:
                        if c not in LIST_SYMBOLS:
                            break
                    elif ''.join(val) + c not in SYMBOLS:
                        break

                    val.append(c)
                    c = self.read_char()

                self.pushback = c

            tt = TokType.SYMBOL

        t = Token(tt, ''.join(val))
        return t

    def is_combining_symbol(self, c):
        if c in ['\'', '{', '|', '!', '=', '<', ' ', '\t', '*', '#', ':',
                 ';', ]:
            return True
        else:
            return False

    def read_char(self):
        if self.pushback is not None:
            c = self.pushback
            self.pushback = None
            return c

        try:
            c = self.reader.read(1)
            if not c:
                raise Exception()
        except Exception:
            self.is_eof = True
            c = None

        return c

    def is_symbol(self, ch):
        if not ch: return False
        return not self.is_space(ch) and not self.is_word_char(ch)

    def is_space(self, ch):
        if not ch: return False
        return ch in string.whitespace

    def is_word_char(self, ch):
        if not ch: return False;
        return ch in string.ascii_letters or ch in string.digits
