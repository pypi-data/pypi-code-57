#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Misc helper
"""
from __future__ import division, print_function, absolute_import, unicode_literals

# Standard libraries.
import time
from datetime import timedelta
from contextlib import contextmanager

try:
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0.invalid0"

__date__ = "2020/06/13 17:28:32 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 1999, 2000 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "bhoel@starship.python.net"


def swirl():
    """Generator to show a swirling life indicator.

Returns:
    `generator`: printing running indicator.

>>> sw = swirl()
>>> a = [_ for _ in zip(range(5), sw)]
\\\r|\r/\r-\r\\\r
>>>
"""
    sw_string = r"\|/-"
    while True:
        for c in sw_string:
            print(c, end="\r")
            yield


def count_with_msg(msg="loop", start=0):
    """Counting variable with start value and message.

Args:
    msg (str): base message
    start (int): counter start_time

Returns:
    `generator`: counter with message.

>>> c = count_with_msg("msg", 5)
>>> print([i for _, i in zip(range(5),c)] == [5, 6, 7, 8, 9])
msg 1 \rmsg 2 \rmsg 3 \rmsg 4 \rmsg 5 \rTrue
>>>
"""
    i = 1
    _count = start
    while True:
        print("{} {} ".format(msg, i), end="\r")
        yield _count
        _count += 1
        i += 1


@contextmanager
def process_msg_context(msg):
    """Provides a context for calling routines and reporting entering and exit.

Args:
    msg (str): message for bracing process.

Returns:
    `contextmanager`: bracing message.

>>> with process_msg_context("do something"):
...     pass
do something...\rdo something...done
>>>
"""
    print("{}...".format(msg), end="\r")
    yield
    print("{}...done".format(msg))


@contextmanager
def timed_process_msg_context(msg, time_form=None):
    """Provides a context for calling routines and reporting entering and exit.
Report spent time.

Args:
    msg (str): message for bracing process.
    time_form (func): function formatting druntime.

Returns:
    `contextmanager`: bracing message.

>>> with timed_process_msg_context("do something"):
...     time.sleep(1)
do something...\rdo something...done (0:00:01)
>>> with timed_process_msg_context("do something", lambda t:"{:d}s".format(int(t))):
...     time.sleep(1)
do something...\rdo something...done (1s)
>>>
"""
    if time_form is None:
        time_form = lambda t: timedelta(seconds=int(t))
    start_time = time.time()
    print("{}...".format(msg), end="\r")
    yield
    print(("{}...done ({})").format(msg, time_form(time.time() - start_time)))


# Local Variables:
# mode: python
# compile-command: "python ../../setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
