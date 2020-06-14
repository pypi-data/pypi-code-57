# Author: Scott Woods <scott.suzuki@gmail.com>
# MIT License
#
# Copyright (c) 2017, 2018, 2019, 2020 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Transformation of application data to a formal text representation according
to an associated :py:mod:`~ansar.memory` type, and back again. These text
fragments become the *on-the-wire* representation for data such as times, that
might otherwise end up as unreadable integer or floating point numbers. These
transformations guarantee correctness of the encode-decode process, i.e. the
original application value will be recovered in the decoding process. System
limitations, such as floating point representation, mean that the guarantee
cannot be extended to related encode-decode processes.

.. autofunction:: world_iso
.. autofunction:: clock_iso
.. autofunction:: world_epoch
.. autofunction:: clock_epoch
.. autofunction:: time_span
.. autofunction:: break_span
.. autofunction:: span_to_text
.. autofunction:: text_to_span
.. autofunction:: uuid_to_text
.. autofunction:: text_to_uuid
"""
__docformat__ = 'restructuredtext'

import sys
import time
import calendar
import re
import uuid

__all__ = [
    'ConversionError',
    'ConversionEncodeFailed',
    'ConversionDecodeFailed',

    'world_iso',
    'clock_iso',
    'world_epoch',
    'clock_epoch',
    'time_span',
    'break_span',
    'span_to_text',
    'text_to_span',
    'uuid_to_text',
    'text_to_uuid',
]

# Exceptions
#
class ConversionError(Exception):
    """
    Base exception for all conversion exceptions.
    """
    pass

class ConversionDecodeFailed(ConversionError):
    """
    The exception raised on failure of one of the :py:func:`~ansar.convert` decoding
    functions.
    """
    def __init__(self, need, text):
        self.need = need
        self.text = text

    def __str__(self):
        return 'cannot recover %s from "%s"' % (
            self.need, self.text)

class ConversionEncodeFailed(ConversionError):
    """
    The exception raised on failure of one of the :py:func:`~ansar.convert` encoding
    functions.
    """
    def __init__(self, need, text):
        self.need = need
        self.text = text

    def __str__(self):
        return 'cannot represent %s as a %s' % (
            self.text, self.need)


# Standard conversions between string and
# machine versions of time values.
ISO_8601_NO_SECONDS = '%Y-%m-%dT%H:%M'

# Very sensitive functions in the area of fractional
# part and time conversion functions, e.g. gmtime and
# timegm.
def world_iso(t=time.time()):
    '''Convert host time value to standard UTC time representation. Return string.'''
    a = '%f' % (t,)
    d = a.find('.')
    if d == -1:
        raise ConversionEncodeFailed('WorldTime', a)
    h = a[:d]
    t = a[d + 1:]
    if not h.isdigit() or not t.isdigit():
        # NOTE: catches times before epoch (negatives)
        raise ConversionEncodeFailed('WorldTime', a)
    i = int(h)
    f = int(t)
    t9 = time.gmtime(i)
    iso = time.strftime(ISO_8601_NO_SECONDS, t9)
    s = int(t9[5])
    if f == 0:
        return '%s:%02dZ' % (iso, s)
    z = t.rstrip('0')
    return '%s:%02d.%sZ' % (iso, s, z)

def clock_iso(t=time.time()):
    '''Convert host time value to standard clock-on-the-wall time representation. Return string.'''
    a = '%f' % (t,)
    d = a.find('.')
    if d == -1:
        raise ConversionEncodeFailed('ClockTime', a)
    h = a[:d]
    t = a[d + 1:]
    if not h.isdigit() or not t.isdigit():
        # NOTE: catches times before epoch (negatives)
        raise ConversionEncodeFailed('ClockTime', a)
    i = int(h)
    f = int(t)
    t9 = time.localtime(i)
    iso = time.strftime(ISO_8601_NO_SECONDS, t9)
    s = int(t9[5])
    if f == 0:
        return '%s:%02d' % (iso, s)
    z = t.rstrip('0')
    return '%s:%02d.%s' % (iso, s, z)

def group_or_zero(s):
    if s is None:
        return 0
    return int(s)

# BE AWARE THAT HAND-CODED TIME STRINGS WITH FRACTIONAL
# PARTS MAY NOT TRANSLATE WELL TO FLOAT VALUE AND BACK.
# VALUES PASSED TO _epoch FUNCTIONS SHOULD COME FROM
# _iso FUNCTIONS OR MANUAL STRINGS WITH NO FRACTIONAL
# PART.

ISO_REGULAR = r'^([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})T([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2})(\.[0-9]+)?Z?$'
iso = re.compile(ISO_REGULAR)

def world_epoch(s):
    '''Convert a standard UTC time string to a host time value. Fraction is optional. Return float.'''
    m = iso.match(s)
    if not m or s[-1] != 'Z':
        raise ConversionDecodeFailed('WorldTime', s)

    t9 = (group_or_zero(m.group(1)),
      group_or_zero(m.group(2)),
      group_or_zero(m.group(3)),
      group_or_zero(m.group(4)),
      group_or_zero(m.group(5)),
      group_or_zero(m.group(6)),
      0,
      0,
      -1)
    c = calendar.timegm(t9)
    c = float(c)
    f = m.group(7)
    if not f is None:
        f = float(f)
        # if c < 0:
        #    return c - f
        # return c + f
        if c < 0:
            raise ConversionEncodeFailed('WorldTime', 'negative value')
        return c + f
    return c

def clock_epoch(s):
    '''Convert a standard clock-on-the-wall time string to a host time value. Return float.'''
    m = iso.match(s)
    if not m or s[-1] == 'Z':
        raise ConversionDecodeFailed('ClockTime', s)
    t9 = (group_or_zero(m.group(1)),
      group_or_zero(m.group(2)),
      group_or_zero(m.group(3)),
      group_or_zero(m.group(4)),
      group_or_zero(m.group(5)),
      group_or_zero(m.group(6)),
      0,
      0,
      -1)
    c = time.mktime(t9)
    c = float(c)
    f = m.group(7)
    if not f is None:
        f = float(f)
        # if c < 0:
        #    return c - f
        # return c + f
        if c < 0:
            raise ConversionDecodeFailed('ClockTime', 'negative value')
        return c + f
    return c

# Helpers for time span values.
#
DHMS = r'^[-]?(([0-9]+)d)?(([0-9]+)h)?(([0-9]{1,2})m)?(([0-9]{1,2}(\.[0-9]+)?)s)?$'
span = re.compile(DHMS)

SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 60 * SECONDS_PER_MINUTE
SECONDS_PER_DAY = 24 * SECONDS_PER_HOUR

def time_span(hours=0, minutes=0, seconds=0.0, days=0):
    '''Convert standard time quanta to a host time value. Return float.'''
    s = hours * SECONDS_PER_HOUR + minutes * SECONDS_PER_MINUTE + seconds + days * SECONDS_PER_DAY
    return float(s)

def break_span(s):
    '''Break down a timespan value into standard quanta. Return tuple.'''
    n = s < 0
    if n:
        s = -s
    i = int(s)      # Whole part.
    f = s % 1       # Fractional part.

    D = int(i / SECONDS_PER_DAY)     # Grab largest sub-value
    i %= SECONDS_PER_DAY        # Then discard same.

    H = int(i / SECONDS_PER_HOUR)
    i %= SECONDS_PER_HOUR

    M = int(i / SECONDS_PER_MINUTE)
    S = i % SECONDS_PER_MINUTE

    return n, D, H, M, S, f

def text_to_span(t):
    '''Convert a standard text representation of a timespan to a host value. Return float.'''
    if len(t) == 0:
        return None
    # Regular expression and subsequent processing allows for clean redundancy
    # in text representation of timespan, e.g. "1h" is the same as "1h0m0s".
    m = span.match(t)
    if not m:
        return None
    n = t[0] == '-'
    D = group_or_zero(m.group(2))
    H = group_or_zero(m.group(4))
    M = group_or_zero(m.group(6))
    s = D * SECONDS_PER_DAY + H * SECONDS_PER_HOUR + M * SECONDS_PER_MINUTE

    if m.group(7):
        if m.group(9):
            s += float(m.group(8))
        else:
            s += float(int(m.group(8)))
    else:
        s = float(s)
    if n:
        return -s
    return s

def span_to_text(s):
    '''Convert a host timespan value to a standard text representation. Return string.'''
    n, D, H, M, S, f = break_span(s)

    r = ''
    if n: r += '-'
    if D: r += '%dd' % (D,)
    if H: r += '%dh' % (H,)
    if M: r += '%dm' % (M,)
    if S:
        if f == 0.0:
            r += '%ds' % (S,)
        else:
            t = '%f' % (S + f,)
            r += t.rstrip('0')
            r += 's'
    else:
        if f != 0.0:
            t = '%f' % (S + f,)
            r += t.rstrip('0')
            r += 's'

    if len(r):
        return r
    return '0s'

def uuid_to_text(u):
    t = str(u)
    return t

def text_to_uuid(t):
    u = uuid.UUID(t)
    return u
