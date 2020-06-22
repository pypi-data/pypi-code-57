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

from .token_scanner import TokType


class WikiLists(object):
    def __init__(self, main):
        self.main = main
        # Stack of lists at the top level. Lists can also be embedded in tables.
        self.list_stack = ListStack()

    @property
    def in_list(self):
        return len(self.list_stack.lists) > 0

    def parse_list(self, ws, dw):
        """
        Parse a list item.  The problem here is that you have no markers
        for when a list starts or ends or when a list is indented inside
        another list apart from the list item start strings themselves.
        """

        list_spec = ws.next_value()

        # If there is nothing following, then this is just characters
        if ws.peek_token().type == TokType.EOL:
            dw.chars('*')
            return

        self.main.end_para(dw)

        # The next symbol will be something like '*' or '**#' etc. and this
        # shows which levels are active.
        self.start_lists(dw, list_spec)
        self.list_stack.start_item()
        ws.skip_space()
        self.main.parse_inline(ws, dw)

    def start_lists(self, dw, spec):
        """
        Gets the lists into the state they should be in.  We look at the list level in
        the spec that is passed in.  If this is at the same level as the last list
        item then there is nothing to do.

        Go through the list spec and see if there and check it matches the currently
        open lists.  If there are more levels in the new spec, then we open a list for
        each (if more than one is possible at a time?).

        If there is less then we close list(s) until the current list stack matches the
        spec.

        If there is a mismatch at a position, then we have to close all open lists from
        that point and then open a new one with the new type.  (Possible/allowed?)

        @param spec A list 'spec', the leading characters that give the type and
        nesting of the list.  Eg "*" or "*#".  The second one is a numbered list
        nested in an unordered list.
        """
        oldlev = len(self.list_stack)
        newlev = len(spec)

        match_level = 0

        # find out where the current lists and the wanted lists differ
        for wl in self.list_stack:
            c = spec[match_level]
            lt = wl.list_type
            if (c != ':' or lt != ';') and (c != ';' or lt != ':'):
                if c != wl.list_type:
                    break
            match_level += 1
            if match_level >= len(spec):
                break

        # If the match point is at the end, then we just close
        # down the item and start the next
        if match_level == newlev and match_level == oldlev:
            if self.list_stack.end_item():
                dw.end_list_item(self.list_stack.get_top_list().get_item_kind())

            # Special treatment for dl, may need to switch from : to ;
            
            newsym = spec[-1]
            if self.list_stack.get_top_list().get_item_kind() in (1, 2):
                self.list_stack.switch_def_list(newsym)

            if self.list_stack.start_item():
                dw.start_list_item(self.list_stack.get_top_list())
            return

        # If the matching point is not at the end, then we close down lists.
        if match_level < oldlev:
            if oldlev == newlev:
                self.list_stack.end_item()
            self.end_lists(dw, match_level)
            if newlev < oldlev:
                self.list_stack.end_item()

            # Special treatment for dl, may need to switch from : to ;
            newsym = spec[-1]
            if self.list_stack.get_top_list().get_item_kind() in (1, 2):
                self.list_stack.switch_def_list(newsym)

        if self.list_stack.start_item():
            dw.start_list_item(self.list_stack.get_top_list())

        # If the spec is longer than the matchLevel then we open some lists.
        while match_level < len(spec):
            c = spec[match_level]
            match_level += 1
            self.list_stack.add_list(c)
            if c == '*':
                dw.start_unordered()
            elif c == '#':
                dw.start_ordered()
            elif c == ';' or c == ':':
                dw.start_def_list()

            if self.list_stack.start_item():
                dw.start_list_item(self.list_stack.get_top_list())

    def end_lists(self, dw, level):
        """
        Close lists until we are back down the the given level.  If we
        need to end lists, we also need to end paragraphs.  So this is the
        stronger end point.  Ending table would be stronger too.
        """
        self.main.end_para(dw)
        assert level >= 0
        while len(self.list_stack) > level:

            wl = self.list_stack.pop()
            if wl.item_in_progress:
                dw.end_list_item(wl.get_item_kind())

            lt = wl.list_type
            if lt == '*':
                dw.end_unordered()
            elif lt == '#':
                dw.end_ordered()
            else:
                dw.end_def_list()


class ListStack(object):
    """
    Keeps track of the open lists.

    Lists can be nested and can also be inside tables.
    """

    def __init__(self):
        # Used as a stack
        self.lists = []

    def start_item(self):
        if not len(self.lists):
            return False

        li = self.lists[-1]
        ret = li.item_in_progress
        li.item_in_progress = True
        if not ret:
            li.number += 1
        return not ret

    def __len__(self):
        return len(self.lists)

    def __iter__(self):
        return iter(self.lists)

    def add_list(self, c):
        wl = WikiList(c)
        self.lists.append(wl)

    def get_top_list(self):
        return self.lists[-1]

    def end_item(self):
        if not len(self.lists):
            return False
        end = self.lists[-1].item_in_progress
        self.lists[-1].item_in_progress = False
        return end

    def pop(self):
        return self.lists.pop()

    def switch_def_list(self, newsym):
        if not len(self.lists):
            return
        if self.lists[-1].get_item_kind() > 0:
            self.lists.pop()
            self.lists.append(WikiList(newsym))


class WikiList(object):
    """
    To keep track of the lists.  Lists can nest and they
    can also appear inside tables.  There is no marker for a list
    that has ended so you need to keep track of what is going on.
    """
    UNORDERED = 0
    TERM = 1
    DEF = 2
    ORDERED = 3

    def __init__(self, list_type):
        self.list_type = list_type
        self.item_in_progress = False
        self.number = 0

    def get_item_kind(self):
        if self.list_type == ';':
            return self.TERM
        elif self.list_type == ':':
            return self.DEF
        elif self.list_type == '#':
            return self.ORDERED
        else:
            return self.UNORDERED
