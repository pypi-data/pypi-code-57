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
from typing import Iterable, Optional

import collections
import os
import re
import subprocess


def get_output(
    command: str,
    default: str = None,
    cwd: str = None
    ) -> Optional[str]:

  try:
    data = subprocess.check_output(
      command,
      shell=True,
      stderr=open(os.devnull, 'w'),
      cwd=cwd)
    return data.decode().strip()
  except subprocess.CalledProcessError:
    return default


@implements(PowerlinePlugin)
class GitPlugin(Struct):
  style = Field(ansi.Style, default=None)
  colors = Field({
    'conflicted': Field(ansi.Color, default=ansi.SgrColor('red')),
    'modified': Field(ansi.Color, default=ansi.SgrColor('yellow')),
    'staged': Field(ansi.Color, default=ansi.SgrColor('green')),
    'else_': Field(ansi.Color, FieldName('else'), default=ansi.SgrColor('black', True)),
  }, nullable=True, default=Field.DEFAULT_CONSTRUCT)
  padding = Field(str, default=' ')

  _Status = collections.namedtuple('Status', 'new,conflicted,modified,staged')

  def _get_git_root(self, path: str) -> Optional[str]:
    return get_output('git rev-parse --show-toplevel', cwd=path)

  def _get_git_branch(self, path: str) -> Optional[str]:
    branches = get_output('git branch', cwd=path)
    if not branches:
      return None

    branches = [x.strip() for x in re.split('\s+', branches)]
    try:
      index = branches.index('*')
    except ValueError:
      return 'master'
    else:
      return branches[index+1]

  def _get_git_user(self, path: str) -> Optional[str]:
    return get_output('git config user.email', cwd=path)

  def _get_repo_status(self, path: str) -> Optional[_Status]:
    status = get_output('git status --porcelain -b', cwd=path)
    if not status:
      return None
    new, conflicted, modified, staged = 0, 0, 0, 0
    for line in status.splitlines()[1:]:
      code = line[:2]
      if code == '??':
        new += 1
      elif code in ('DD', 'AU', 'UD', 'UA', 'DU', 'AA', 'UU'):
        conflicted += 1
      else:
        if code[0] != ' ':
          staged += 1
        if code[1] != ' ':
          modified += 1
    return self._Status(new, conflicted, modified, staged)

  @override
  def render(self, context: PowerlineContext) -> Iterable[Pen]:
    branch = self._get_git_branch(context.path)
    if not branch:
      return

    status = self._get_repo_status(context.path)
    if status.conflicted:
      bg = self.colors.conflicted if self.colors else self.style.bg
    elif status.modified:
      bg = self.colors.modified if self.colors else self.style.bg
    elif status.staged:
      bg = self.colors.staged if self.colors else self.style.bg
    else:
      bg = self.colors.else_ if self.colors else self.style.bg

    if self.style:
      style = self.style.merge(context.default_style)
    else:
      style = context.default_style
    style = style.replace(bg=bg)

    yield Pen.Text('{0}{2}{0}{1}{0}'.format(self.padding, branch, chars.BRANCH), style)
    yield Pen.Flipchar(chars.RIGHT_TRIANGLE)
