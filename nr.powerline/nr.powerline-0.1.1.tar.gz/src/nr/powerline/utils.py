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

import logging
import os
import signal

from types import FrameType
from typing import Callable, Union

logger = logging.getLogger(__name__)


def try_remove(filename: str):
  try:
    os.remove(filename)
    logger.info('Removed %r', filename)
  except FileNotFoundError:
    pass
  except:
    logger.exception('Unable to remove file %s', filename)


def register_signal_handler(
    sig: Union[str, int],
    handler: Callable[[int, FrameType], None]
    ) -> None:
  """
  Registers a signal handler, chaining it with the current handler. If
  *handler* raises an exception, subsequent handlers will not be called.
  """

  if isinstance(sig, str):
    sig = getattr(signal, sig)

  old_handler = None
  def wrapper(sig, frame):
    handler(sig, frame)
    if old_handler:
      old_handler(sig, frame)
  old_handler = signal.signal(sig, wrapper)
