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

import getpass
import re
from . import chars, Pen, PowerlineContext, PowerlinePlugin
from nr import ansiterm as ansi
from nr.databind.core import Field, FieldName, Struct
from nr.interface import implements, override
from typing import Callable, Dict, Iterable, List


@implements(PowerlinePlugin)
class TextPlugin(Struct):
  """
  Displays some text in the specified *style*. Some additional flags can change the
  style based on some condition. Available conditions are

  * is-server-indicator: Swaps to *indicator_style* if the powerline is rendered
    from a server. Swaps to *indicator_style_2* if no environment data is passed
    to the server.
  * is-status-indicator: Swaps to *indicator_style* if the status code is non-zero.
  """

  style = Field(ansi.Style, default=None)
  is_server_indicator = Field(bool, FieldName('is-server-indicator'), default=False)
  is_status_indicator = Field(bool, FieldName('is-status-indicator'), default=False)
  indicator_style = Field(ansi.Style, FieldName('indicator-style'), default=ansi.parse_style('bg:red bold'))
  indicator_style_2 = Field(ansi.Style, FieldName('indicator-style-2'), default=ansi.parse_style('fg:yellow'))
  text = Field(str)

  def get_vars(self) -> Dict[str, Callable]:
    return {
      'username': getpass.getuser,
    }

  def get_text(self) -> str:
    variables = self.get_vars()
    def _sub(m):
      if m.group(1) not in variables:
        return m.group(0)
      return variables[m.group(1)]()
    return re.sub(r'\$\{([\w\d\_]+)\}', _sub, self.text)

  @override
  def render(self, context: PowerlineContext) -> Iterable[Pen]:
    if self.is_server_indicator and context.is_server:
      if not context.env:
        style = self.indicator_style_2
      else:
        style = self.indicator_style
    elif self.is_status_indicator and context.exit_code != 0:
      style = self.indicator_style
    else:
      style = self.style or context.default_style
    style = style.merge(self.style or context.default_style)
    yield Pen.Text(self.get_text(), style)
    yield Pen.Flipchar(chars.RIGHT_TRIANGLE)
