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
Through a set of classes this module implements an abstract memory model.
The classes can be combined to describe arbitrarily complex types, within
that model. These descriptions are then used during the encode and decode
processes, to curate and transform the serializations produced and the results
of subsequent deserializations::

    ar.MapOf(ar.String(), ar.ArrayOf(ar.Float8(), 8))

.. autofunction:: is_type
.. autofunction:: is_container
.. autofunction:: is_type_class
.. autofunction:: is_container_class
"""
__docformat__ = 'restructuredtext'


from collections import deque
import sys
import time
import calendar
import re
import uuid

__all__ = [
    'Boolean',          # The basic types. Integrals.
    'Byte',
    'Character',
    'Rune',
    'Integer2',
    'Integer4',
    'Integer8',
    'Unsigned2',
    'Unsigned4',
    'Unsigned8',

    'Float4',           # Floating point.
    'Float8',

    'Block',            # Sequence of basic units
    'String',
    'Unicode',

    'Enumeration',

    'WorldTime',        # Time.
    'ClockTime',
    'TimeSpan',

    'UUID',             # UUID - RFC 4122

    'ArrayOf',          # Containers.
    'VectorOf',
    'SetOf',
    'MapOf',
    'DequeOf',

    'UserDefined',      # User-defined type.
    'Type',             # Type of a message.
    'PointerTo',        # Reference to one of the above.

    'TargetAddress',    # Destination.
    'Address',          # An address, such as the sender.

    'Word',             # Instance of generic form, e.g. results of python_to_word
    'Any',              # Any message - on-the-wire, a tuple of Type and Word.

    'complete_list',
    'complete_set',

    'is_type',
    'is_container',
    'is_type_class',
    'is_container_class',

    'NO_SUCH_ADDRESS',  # A properly formed "null" address.

    'is_address',       # Can be used to direct movement.
    'address_on_proxy',

    'deque',            # Auto-inject into namespace.
]

# Each class is used to describe a unit
# of memory.
class Portable(object): pass
class Container(Portable): pass

class Boolean(Portable): pass
class Byte(Portable): pass
class Character(Portable): pass
class Rune(Portable): pass

class Integer2(Portable): pass
class Integer4(Portable): pass
class Integer8(Portable): pass

class Unsigned2(Portable): pass
class Unsigned4(Portable): pass
class Unsigned8(Portable): pass

class Float4(Portable): pass
class Float8(Portable): pass

class String(Portable): pass
class Unicode(Portable): pass
class Block(Portable): pass

class Enumeration(Portable):
    def __init__(self, **kv):
        self.kv = kv
        for k, v in kv.items():
            setattr(self, k, v)
        self.vk = {v: k for k, v in kv.items()}

    def to_name(self, v):
        return self.vk[v]

    def to_number(self, k):
        return self.kv[k]

class WorldTime(Portable): pass
class ClockTime(Portable): pass
class TimeSpan(Portable): pass

class UUID(Portable): pass

# Types that require additional
# info, i.e. the contents of an array.
class ArrayOf(Container):
    def __init__(self, element, size):
        self.element = element
        self.size = size

class VectorOf(Container):
    def __init__(self, element):
        Container.__init__(self)
        self.element = element

class SetOf(Container):
    def __init__(self, element):
        self.element = element

class MapOf(Container):
    def __init__(self, key, value):
        self.key = key
        self.value = value

class DequeOf(Container):
    def __init__(self, element):
        self.element = element

class UserDefined(Container):
    def __init__(self, element):
        self.element = element

class PointerTo(Container):
    def __init__(self, element):
        self.element = element

class Type(Portable): pass
class TargetAddress(Portable): pass
class Address(Portable): pass
class Word(Portable): pass
class Any(Portable): pass

# Every defined type.
#
complete_list = [
    Boolean,
    Byte,
    Character,
    Rune,
    Integer2,
    Integer4,
    Integer8,
    Unsigned2,
    Unsigned4,
    Unsigned8,
    Float4,
    Float8,
    String,
    Unicode,
    Block,
    Enumeration,
    WorldTime,
    ClockTime,
    TimeSpan,
    UUID,
    UserDefined,
    ArrayOf,
    VectorOf,
    SetOf,
    MapOf,
    DequeOf,
    PointerTo,
    Type,
    TargetAddress,
    Address,
    Word,
    Any,
]

complete_set = set(complete_list)

# Few handy type predicates.
#

def is_type(a):
    '''Is object *a* an instance of one of the portable types.'''
    return isinstance(a, Portable)

def is_container(a):
    '''Is object *a* an instance of one of the portable container types.'''
    return isinstance(a, Container)

def is_type_class(c):
    '''Is parameter *c* one of the portable types.'''
    try:
        return issubclass(c, Portable)
    except TypeError:
        return False

def is_container_class(c):
    '''Is parameter *c* one of the portable container types.'''
    try:
        return issubclass(c, Container)
    except TypeError:
        return False

# This is the official null address and where required the
# default value for an address.
NO_SUCH_ADDRESS = None

def is_address(a):
    '''Is parameter *a* is a valid point address.'''
    try:
        return isinstance(a, tuple) and len(a) > 0
    except:
        return False

def address_on_proxy(a, p):
    '''Predicate function. Returns true if a is a remote address behind the proxy address, p.'''
    if a[-1] == p[-1]:
        if len(p) == 1 and len(a) > 1:
            return True
    return False
