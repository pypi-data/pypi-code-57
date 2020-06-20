# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2020, Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# this software and associated documentation files (the "Software"), to deal in
# Software without restriction, including without limitation the rights to use,
# modify, merge, publish, distribute, sublicense, and/or sell copies of the
# and to permit persons to whom the Software is furnished to do so, subject to
# following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
# USE OR OTHER DEALINGS IN THE SOFTWARE.

from . import chars, Pen, PowerlineContext, PowerlinePlugin
from nr import ansiterm as ansi
from nr.databind.core import Field, FieldName, Struct
from nr.interface import implements, override
from typing import Iterable, List

import os


@implements(PowerlinePlugin)
class CwdPlugin(Struct):
  style = Field(ansi.Style, default=None)
  padding = Field(str, default=' ')
  breadcrumbs = Field({
    'max_crumbs': Field(int, FieldName('max-crumbs'), default=5)
  }, default=None)

  def _get_display_path(self, path: str) -> str:
    user_home = os.path.expanduser('~')
    try:
      relpath = os.path.relpath(path, user_home)
      if relpath.startswith(os.pardir):
        raise ValueError
      if relpath == os.curdir:
        return '~'
      return os.path.join('~', relpath)
    except ValueError:
      return path

  def _crumble_path(self, path: str) -> List[str]:
    parts = os.path.normpath(path).split(os.sep)
    if len(parts) > self.breadcrumbs.max_crumbs:
      neg_offset = len(parts) - self.breadcrumbs.max_crumbs + 1
      parts = [parts[0]] + [chars.ELLIPSIS] + parts[-neg_offset:]
    if not parts[0]:
      parts.pop(0)
    if not parts or parts == ['']:
      parts = ['/']
    return parts

  @override
  def render(self, context: PowerlineContext) -> Iterable[Pen]:
    display_path = self._get_display_path(context.path)
    style = self.style or context.default_style
    if self.breadcrumbs is None:
      yield Pen.Text('{0}{1}{0}'.format(self.padding, display_path), self.style)
    else:
      #bold_style = style.merge(ansi.parse_style('bold'))
      parts = self._crumble_path(display_path)
      sep = self.padding + chars.RIGHT_TRIANGLE_THIN + self.padding
      if len(parts) > 1:
        text = ' ' + sep.join(parts[:-1]) + sep
        yield Pen.Text(text, style)
        prefix = ''
      else:
        prefix = self.padding
      yield Pen.Text(prefix + parts[-1] + self.padding, style)

    yield Pen.Flipchar(chars.RIGHT_TRIANGLE)
