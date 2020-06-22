# coding=utf-8
#
# Copyright © 2013, 2016 Steve Ratcliffe, Itinken Limited
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

from six import StringIO


class Writer(object):
    def __init__(self, out):
        super(Writer, self).__init__()

        class E:
            pass

        self.extensions = E()


class WriteInterface(Writer):
    """
    The interface required by all writers.

    You need to support all of these methods to create a writer.
    """

    def __init__(self, out):
        super(WriteInterface, self).__init__(out)
        self.pending_new_line = False
        self.out = out

    def set_pending_newline(self):
        self.pending_new_line = True

    def start_header(self, n):
        raise Exception('not implemented')

    def end_header(self, n):
        raise Exception('not implemented')

    def start_para(self):
        raise Exception('not implemented')

    def end_para(self):
        raise Exception('not implemented')

    def start_unordered(self):
        raise Exception('not implemented')

    def end_unordered(self):
        raise Exception('not implemented')

    def start_ordered(self):
        raise Exception('not implemented')

    def end_ordered(self):
        raise Exception('not implemented')

    def start_def_list(self):
        raise Exception('not implemented')

    def end_def_list(self):
        raise Exception('not implemented')

    def start_list_item(self, li):
        raise Exception('not implemented')

    def end_list_item(self, kind):
        raise Exception('not implemented')

    def start_block(self, fill, wiki, atts=None):
        raise Exception('not implemented')

    def end_block(self, fill, wiki):
        raise Exception('not implemented')

    def start_style(self, tag, is_block, atts):
        raise Exception('not implemented')

    def end_style(self, tag, is_block):
        raise Exception('not implemented')

    def start_link(self, href, auto_link):
        raise Exception('not implemented')

    def end_link(self):
        raise Exception('not implemented')

    def start_table(self, atts):
        raise Exception('not implemented')

    def end_table(self):
        raise Exception('not implemented')

    def start_table_row(self, atts):
        raise Exception('not implemented')

    def end_table_row(self):
        raise Exception('not implemented')

    def start_table_cell(self, atts):
        raise Exception('not implemented')

    def end_table_cell(self):
        raise Exception('not implemented')

    def start_table_header(self, atts):
        raise Exception('not implemented')

    def end_table_header(self):
        raise Exception('not implemented')

    def end_document(self):
        raise Exception('not implemented')

    def one_char(self, c):
        assert len(c) == 1
        raise Exception('not implemented')

    def chars(self, s):
        raise Exception('not implemented')


class TextBase(WriteInterface):
    """
    Base writer for text-like output formats.
    """

    def __init__(self, out):
        super(TextBase, self).__init__(OutWrapper(out))

        self.block_tags = []
        self.inline_tags = []

        self.lists = []
        self.tables = []

        self.pending_new_line = False
        self.bol = True
        self.skip_space = False
        self.has_gap = True     # Beginning of file does not require blank line

        self.block_fill = True

        self.in_para = False
        self.in_list_item = False
        self.in_block = False

    def set_pending_newline(self):
        self.pending_new_line = True

    def write_atts(self, atts):
        if atts is None:
            return

        for att in atts:
            self.write(' ')
            self.write(att.key)
            self.write('="')
            self.write(att.value.strip())
            self.write('"')

    def pop_list(self):
        self.lists.pop()
        self.in_list_item = False

    def get_lists(self):
        """If we are in a table, get the table list spec, else the
        top level list spec"""
        if len(self.tables):
            return self.tables[-1].lists
        else:
            return self.lists

    def get_current_list(self):
        """
        Get the current list object.
        """
        l = self.get_lists()
        if len(l) > 0:
            return l[-1]
        else:
            raise Exception("badly nested list")

    def write(self, text):
        for c in text:
            if c == '\n':
                self.pending_new_line = False

            if c in (' ', '\t', '\n', '\r'):
                if self.skip_space:
                    continue
            else:
                self.skip_space = False

            if c == '\n':
                if self.bol:
                    self.has_gap = True
                self.bol = True
            else:
                self.bol = False
                self.has_gap = False
            self.out.write(c)

    def writenl(self):
        self.write('\n')

    def ensure_bol(self, force=False):
        if not self.bol:
            if force:
                self.out.write('\n')
                self.bol = True
            else:
                self.write('\n')

    def ensure_gap(self, force=False):
        self.ensure_bol(force)
        if not self.has_gap:
            if force:
                self.out.write('\n')
            else:
                self.write('\n')


class OutWrapper(object):
    """
    A wrapper for the output stream that allows parts of it to be captured.

    Acts like a writable object, but the output can be directed to a buffer rather
    than the final output.
    """

    def __init__(self, out):
        super(OutWrapper, self).__init__()
        self.out_stack = [out]

    def write(self, text):
        """
        Write the string to the current output stream.
        """
        s = self.out_stack[-1]
        return s.write(text)

    def start_capture(self):
        b = TextBuffer()
        self.out_stack.append(b)
        return b

    def end_capture(self):
        assert len(self.out_stack) > 1
        return self.out_stack.pop()


class TextBuffer(object):
    """
    A buffer to receive text.

    The text is added raw on input. It can then be formatted in various ways when
    the capture is complete.
    """

    def __init__(self):
        super(TextBuffer, self).__init__()
        self.buf = StringIO()

    def write(self, text):
        self.buf.write(text)

    def format(self, prefix=None):
        """
        Reformat the buffer by prefixing each line with the given prefix.

        If the first or last lines are blank, then no prefix is applied to them.

        :param prefix: This will be pre-pended to each line. If None, then the buffer value is returned
        directly.
        :return: A string.
        """
        s = self.buf.getvalue()
        if prefix is None:
            return s

        lines = s.split('\n')
        out = []
        for line in lines:
            mod = line
            mod = prefix + line
            out.append(mod)

        for i in (0, len(out) - 1):
            if out[i] == prefix:
                out[i] = ''

        return '\n'.join(out)
