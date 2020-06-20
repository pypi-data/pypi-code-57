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
from nr.databind.core import Field, Struct
from nr.interface import implements, override
from typing import Iterable
import os


@implements(PowerlinePlugin)
class VenvPlugin(Struct):
  style = Field(ansi.Style, default=None)
  parenthesized = Field(bool, default=True)

  def render(self, context: PowerlineContext) -> Iterable[Pen]:
    env = (context.getenv('VIRTUAL_ENV') or context.getenv('CONDA_ENV_PATH') or
           context.getenv('CONDA_DEFAULT_ENV'))
    if context.getenv('VIRTUAL_ENV') and os.path.basename(env) == '.venv':
      env = os.path.dirname(env)
    if not env:
      return
    env_name = os.path.basename(env)
    if self.parenthesized:
      env_name = '(' + env_name  + ')'
    yield Pen.Text(' ' + env_name + ' ', self.style or context.default_style)
    yield Pen.Flipchar(chars.RIGHT_TRIANGLE)
