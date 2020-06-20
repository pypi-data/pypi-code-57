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

from . import chars, server, static
from .utils import register_signal_handler, try_remove
from nr import ansiterm as ansi
from nr.interface import Interface
from nr.sumtype import Constructor, Sumtype
from nr.utils.process import process_exists, process_terminate, replace_stdio, spawn_daemon
from typing import Iterable, Optional, Sequence, TextIO, Union

import argparse
import io
import json
import logging
import os
import nr.databind.core, nr.databind.json
import signal
import sys

__author__ = 'Niklas Rosenstein <rosensteinniklas@gmail.com>'
__version__ = '0.1.1'

logger = logging.getLogger(__name__)


class Pen(Sumtype):
  Text = Constructor('text,style')
  Flipchar = Constructor('char')


def render(
    pen_sequence: Sequence[Pen],
    fp: TextIO = None,
    escape_unprintable: bool = False
    ) -> Optional[str]:
  r"""
  Render a sequence of #Pen instructions to *fp*, or returns it as a string.
  If *escape_unprintable* is enabled, unprintable characters will be wrapped
  in `\[` and `\]` to allow the shell to properly count the width of the
  resulting string.
  """

  if fp is None:
    fp = io.StringIO()
    return_result = True
  else:
    return_result = False

  def _find_next_bg(offset: int) -> Optional[ansi.Color]:
    for pen in pen_sequence[offset:]:  # TODO (@NiklasRosenstein): islice()?
      if isinstance(pen, Pen.Text):
        return pen.style.bg
    return None

  style = ansi.Style()
  for index, pen in enumerate(pen_sequence):
    if isinstance(pen, Pen.Flipchar):
      new_bg = _find_next_bg(index+1) or ansi.SgrColor('DEFAULT')
      if new_bg == style.bg:
        # Note: This is more of a hack in cases where two plugins
        #   have the same background color, rendering the common
        #   RIGHT_TRIANGLE flipchar invisible.
        text = chars.RIGHT_TRIANGLE_THIN
        style = ansi.Style(None, new_bg)
      else:
        style = ansi.Style(style.bg, new_bg)
        text = pen.char
    elif isinstance(pen, Pen.Text):
      style = pen.style or style
      text = pen.text
    else:
      raise TypeError('expected Pen object, got {!r}'.format(
        type(pen).__name__))
    if escape_unprintable:
      fp.write('\\[')
    fp.write(str(style))
    if escape_unprintable:
      fp.write('\\]')
    fp.write(text)
    if escape_unprintable:
      fp.write('\\[')
    fp.write(str(ansi.Attribute.RESET))
    if escape_unprintable:
      fp.write('\\]')

  if return_result:
    return fp.getvalue()

  return None


class PowerlineContext:

  def __init__(self,
      path: str,
      exit_code: int = 0,
      default_style: ansi.Style = None,
      env: dict = None,
      is_server: bool = False):
    self.path = path
    self.exit_code = exit_code
    self.default_style = default_style or ansi.parse_style('white blue')
    self.env = os.environ if env is None else env
    self.is_server = is_server

  def getenv(self, name: str, default: str = None) -> Optional[str]:
    return self.env.get(name, default)


class AnsiModule(nr.databind.core.Module):

  def __init__(self):
    super().__init__()
    self.register(ansi.Color, nr.databind.core.IDeserializer(
      deserialize=lambda m, n: ansi.parse_color(n.value)))
    self.register(ansi.Style, nr.databind.core.IDeserializer(
      deserialize=lambda m, n: ansi.parse_style(n.value)))


@nr.databind.core.SerializeAs(nr.databind.core.UnionType
  .with_entrypoint_resolver('nr.powerline.plugins'))
class PowerlinePlugin(Interface):

  def render(self, context: PowerlineContext) -> Iterable[Pen]:
    ...


class Powerline(nr.databind.core.Struct):
  plugins = nr.databind.core.Field([PowerlinePlugin])
  default_style = nr.databind.core.Field(ansi.Style,
    nr.databind.core.FieldName('default-style'), default=None)

  def render(self,
      context: PowerlineContext,
      fp: TextIO = None,
      escape_unprintable: bool = False
      ) -> Optional[str]:
    pens = []
    for plugin in self.plugins:
      pens += plugin.render(context)
    return render(pens, fp, escape_unprintable)


def load_powerline(*try_files: str, default: Union[dict, Powerline] = None) -> Optional[Powerline]:
  mapper = nr.databind.core.ObjectMapper(
    AnsiModule(),
    nr.databind.json.JsonModule(),
  )
  for filename in try_files:
    if os.path.isfile(filename):
      with open(filename) as fp:
        data = json.load(fp)
      return mapper.deserialize(data, Powerline, filename=filename)
  if isinstance(default, dict):
    default = mapper.deserialize(default, Powerline, filename='<default>')
  return default


def main(argv=None):
  """
  Entrypoint for nr-powerline.
  """

  parser = argparse.ArgumentParser()
  parser.add_argument('exit_code', type=int, nargs='?')
  parser.add_argument('-f', '--file')
  parser.add_argument('-e', '--escape', action='store_true')
  parser.add_argument('--run-dir', default=None)
  parser.add_argument('--start', action='store_true')
  parser.add_argument('--stop', action='store_true')
  parser.add_argument('--status', action='store_true')
  parser.add_argument('--fake-server', action='store_true')
  parser.add_argument('--exit-code', action='store_true')
  parser.add_argument('--src', choices=('bash',))
  args = parser.parse_args(argv)

  logging.basicConfig(format='[%(asctime)s - %(levelname)s]: %(message)s', level=logging.INFO)

  powerline = load_powerline(
    args.file or os.path.expanduser('~/.local/powerline/config.json'),
    default=static.default_powerline)
  context = PowerlineContext(
    os.getcwd(),
    args.exit_code or 0,
    default_style=powerline.default_style,
    is_server=args.fake_server)

  if args.src == 'bash':
    print(static.bash_src)
    sys.exit(0)
  elif args.src:
    parser.error('unexpected argument for --src: {!r}'.format(args.src))

  if not args.start and not args.stop and not args.status:
    print(powerline.render(context, escape_unprintable=args.escape), end='')
    return

  run_dir = args.run_dir or os.path.expanduser('~/.local/powerline')
  log_file = os.path.join(run_dir, 'daemon.log')
  pid_file = os.path.join(run_dir, 'daemon.pid')
  socket_file = os.path.join(run_dir, 'daemon.sock')

  if os.path.isfile(pid_file):
    with open(pid_file) as fp:
      daemon_pid = int(fp.read().strip())
  else:
    daemon_pid = None

  if args.stop and daemon_pid:
    logger.info('Stopping %d', daemon_pid)
    process_terminate(daemon_pid)
  if args.start:
    if os.path.exists(socket_file):
      os.remove(socket_file)

    def run(powerline, stdout):
      with open(pid_file, 'w') as fp:
        fp.write(str(os.getpid()))
      logger.info('Started %d', os.getpid())
      register_signal_handler('SIGINT', lambda *a: try_remove(pid_file))
      replace_stdio(None, stdout, stdout)
      conf = server.Address.UnixFile(socket_file)
      server.PowerlineServer(conf, powerline).run_forever()
      logger.info('Bye bye')

    os.makedirs(run_dir, exist_ok=True)
    stdout = open(log_file, 'a')
    spawn_daemon(lambda: run(powerline, stdout))
  if args.status:
    if not daemon_pid or not process_exists(daemon_pid):
      if args.exit_code:
        sys.exit(7)
      print('stopped')
    else:
      if args.exit_code:
        sys.exit(0)
      print('running')
