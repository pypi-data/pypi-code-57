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
This module implements the concept of a frame for the transporting of
serializations across networks and for storing them in files. It manages
the breakdown of an endless, network byte-stream into discrete payloads
that are assumed to contain complete serializations. The opportunity is
taken to tack on optional attributes to each payload allowing an out-of-band
stream of information to pass between sender and receiver. That OOB stream
can be used to pass details such as the encoding of the payload and security
details.

The crucial contents are the :py:class:`~ansar.zed.ZedFrame` class and the
:py:func:`~ansar.zed.zed` generator function.

.. autoclass:: ZedFrame
.. autoclass:: ZedError
.. autoclass:: NotZed
.. autoclass:: NotGoodZed
.. autofunction:: zed
"""
__docformat__ = 'restructuredtext'

__all__ = [
	'ZedError',
	'NotZed',
	'NotGoodZed',
	'ZedFrame',
	'zed',
]

# Exceptions
#
class ZedError(Exception):
    """
    Base exception for all `ZedFrame` exceptions.
    """
    pass

class NotZed(ZedError):
    """
    The exception raised on failure of the :py:func:`~ansar.zed.zed` function
    to process the byte stream into a :py:class:`~ansar.zed.ZedFrame`. The stream
    does not conform to the specification.
    """
    def __init__(self, zf):
        self.zf = zf

    def __str__(self):
        zf = self.zf
        r = ''.join(zf.register.keys())
        return 'byte %d, state %d (registers "%s", payload %d)' % (
            zf.token, zf.state,
            r, len(zf.payload))

class NotGoodZed(ZedError):
    """
    The exception raised after successful detection of a
    :py:class:`~ansar.zed.ZedFrame` but the values within that
    frame do not conform to specification, e.g. a duplicate key.
    """
    def __init__(self, why, help=None):
        self.why = why
        self.help = help
    def __str__(self):
        if self.help is None:
            return self.why
        return '%s (%s)' % (self.why, self.help)

# Functions that construct transition
# fragments;
# shift_only ......... move to defined state
# shift_key .......... save token as latest "key"
# shift_value ........ append token to current "value"
# shift_h1 ........... save token as high byte of slash hex
# shift_h2 ........... construct hex byte and append to "value"
# shift_register ..... validity checks and add "key+value" to map
# shift_payload ...... append token to current "payload"

def shift_only(next):
    def shift(zf):
        return next
    return shift

def shift_key(next):
    def shift(zf):
        zf.key = zf.token
        return next
    return shift

def shift_value(next):
    def shift(zf):
        zf.value += chr(zf.token)
        return next
    return shift

def shift_h1(next):
    def shift(zf):
        zf.h1 = zf.token - ord('0')
        return next
    return shift

def shift_h2(next):
    def shift(zf):
        zf.h2 = zf.token - ord('0')
        zf.value += chr((zf.h1 << 4) | zf.h2)
        return next
    return shift

def shift_register(next):
    def shift(zf):
        if zf.key != ord('Z'):
            if zf.key in zf.register:
                why = 'duplicate "%s" register' % (chr(zf.key),)
                raise NotGoodZed(why)
            zf.register[zf.key] = zf.value
            zf.value = ''
            return next
        if zf.value.isdigit():
            zf.size = int(zf.value)
            if zf.size == 0:
                return 0
            zf.expected = zf.size
            return 14
        if zf.value == '*':
            return 0
        why = 'cannot use value "%s" for the Z-register' % (zf.value,)
        raise NotGoodZed(why, 'value must be a number or an asterisk')
    return shift

def shift_payload(next):
    def shift(zf):
        zf.payload.append(zf.token)
        zf.expected -= 1
        if zf.expected > 0:
            return 14
        return 0
    return shift

# Helper functions that capture description of edges
# from states and save into state machine;
# char_shift ....... save edge for char
# set_shift ........ save edges for chars in the string
# range_shift ...... save edges for chars from b through e
def char_shift(s, char, next, f=shift_only):
    f = f(next)         # Complete the transition function.
    s[ord(char)] = f

def set_shift(s, r, next, f=shift_only):
    f = f(next)
    for c in r:
        i = ord(c)
        s[i] = f

def range_shift(s, b, e, next, f=shift_only):
    f = f(next)
    b = ord(b)
    e = ord(e) + 1
    for i in range(b, e):
        s[i] = f

# Build the state machine. Each state (s1, s2, s3...) is
# an array of 256 entries that are either nulls or a funtion
# that knows the next state.
def empty():
    return [None] * 256

s1 = empty()

char_shift(s1, '\r', 2)
char_shift(s1, '\n', 1)
range_shift(s1, 'A', 'Z', 3, shift_key)
range_shift(s1, 'a', 'z', 3, shift_key)

#
#
s2 = empty()

char_shift(s2, '\n', 1)

#
#
s3 = empty()

char_shift(s3, '=', 4)

#
#
s4 = empty()

char_shift(s4, '\r', 7)
char_shift(s4, '\n', 8, shift_register)
range_shift(s4, ' ', '~', 4, shift_value)
char_shift(s4, '\\', 5)     # Overwrite edge created by range.

#
#
s5 = empty()

range_shift(s5, '0', '9', 6, shift_h1)
range_shift(s5, 'a', 'f', 6, shift_h1)
range_shift(s5, 'A', 'F', 6, shift_h1)

#
#
s6 = empty()

range_shift(s6, '0', '9', 4, shift_h2)
range_shift(s6, 'a', 'f', 4, shift_h2)
range_shift(s6, 'A', 'F', 4, shift_h2)

#
#
s7 = empty()

char_shift(s7, '\n', 8, shift_register)

#
#
s8 = empty()

range_shift(s8, 'A', 'Z', 9, shift_key)
range_shift(s8, 'a', 'z', 9, shift_key)

#
#
s9 = empty()

char_shift(s9, '=', 10)

#
#
s10 = empty()

char_shift(s10, '\r', 13)
char_shift(s10, '\n', 8, shift_register)
range_shift(s10, ' ', '~', 10, shift_value)
char_shift(s10, '\\', 11)

#
#
s11 = empty()

range_shift(s11, '0', '9', 12, shift_h1)
range_shift(s11, 'a', 'f', 12, shift_h1)
range_shift(s11, 'A', 'F', 12, shift_h1)

#
#
s12 = empty()

range_shift(s12, '0', '9', 10, shift_h2)
range_shift(s12, 'a', 'f', 10, shift_h2)
range_shift(s12, 'A', 'F', 10, shift_h2)

#
#
s13 = empty()

char_shift(s13, '\n', 8, shift_register)

#
#
s14 = [shift_payload(14)] * 256

#
#
class ZedFrame(object):
    """
    The object that holds the current state of stream processing and
    the results when a complete frame is detected.

    Members include;

    - a finite state machine,
    - state variables,
    - the register file,
    - and the payload, usually a block of bytes.
    """
    machine = [
        [], s1, s2, s3, s4, s5, s6, s7,
        s8, s9, s10, s11, s12, s13, s14
    ]

    def __init__(self):
        self.reset()

    def reset(self):
        self.state = 1      # Machine values and artefacts
        self.token = 0      # of register (key+value)
        self.key = 0        # construction.
        self.value = ''
        self.h1 = 0
        self.h2 = 0
        
        self.expected = 0   # Countdown of payload.

        self.register = dict()          # Results of an accepted
        self.payload = bytearray()      # frame
        self.size = 0

def zed(zf, block):
    """
    This function accepts an *active* ``ZedFrame`` and the latest block of bytes
    from the input stream. The bytes within the block are passed through an analyzer
    until a complete frame has been detected. The function then yields the value of
    the final, detected register, i.e. the 'Z' register. The function yields zero or
    more times each time it is called. The caller can respond in the manner appropriate
    to the contents of the string. All the elements of the ``ZedFrame`` are available
    in the updated *zf* parameter, e.g. the ``payload`` of the frame::

       for p in zed(zf, block):
           if p.isdigit():
               encoding = zf.payload

    This arrangement allows for the recovery of the payload as a contiguous block even
    though it may have been broken up or combined with neighbours, on its journey
    across a network.

    Parameters:

    - `zf`, an instance of a :py:class:`~ansar.zed.ZedFrame`
    - `block`, a block of bytes.

    Yields (generator):

    - a string, being the value of the zed ('Z') register.
    """
    for b in block:
        zf.token = b
        f = zf.machine[zf.state][zf.token]
        if f is None:
            raise NotZed(zf)
        next = f(zf)
        if next == 0:
            yield zf.value
            zf.reset()
            continue
        zf.state = next
