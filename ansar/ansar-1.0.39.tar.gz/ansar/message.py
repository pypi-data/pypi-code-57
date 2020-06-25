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
A message is an object with named members of arbitrary type (i.e. something
that can be described using :py:mod:`~ansar.memory`). A message may be
sent across a network or stored in a file.
This module provides for the registration of messages with Ansar. Registration
can include type information, flags and state values that affect the
handling and behaviour of messages according to their respective types.
This module supports the encode and decode operations;

Encode
------

* lookup type information
* apply to serialization of application data

Decode
------

* lookup type information
* create a default instance
* deserialize into the default instance


.. autoclass:: Message
.. autoclass:: Unknown
.. autoclass:: Incognito

.. autofunction:: infer_memory
.. autofunction:: from_memory
.. autofunction:: or_from_memory

.. autofunction:: decode_type
.. autofunction:: encode_type

.. autofunction:: bind_message
"""
__docformat__ = 'restructuredtext'

import sys
import uuid

from .memory import *
from .runtime import *


__all__ = [
    'MessageError',
    'MessageRegistrationError',

    'Message',
    'Unknown',
    'Incognito',

    'TypeTrack',
    'correct_track',

    'infer_memory',
    'from_memory',
    'or_from_memory',

    'default_time',
    'default_uuid',
    'default_vector',
    'default_set',
    'default_map',
    'default_deque',

    'default_value',

    'fix_type',
    'fix_schema',
    'compile_schema',

    'encode_type',
    'decode_type',

    'major_minor',
    'current_version',
    'bind_message',
    'equal_to',
]

# Exceptions
#
class MessageError(Exception):
    '''Base exception for all message exceptions.
    '''
    pass

class MessageRegistrationError(MessageError):
    '''The request to register a class cannot be fulfilled.

    :param name: the name of the class
    :type name: str
    :param reason: a short description
    :type reason: str
    '''
    def __init__(self, name, reason):
        self.name = name
        self.reason = reason

    def __str__(self):
        if self.name:
            return 'cannot register "%s" (%s)' % (
                self.name, self.reason)
        return 'registration failure "%s"' % (self.reason,)

#
#
class Message(object):
    '''The base class for all registered application objects.
    '''
    def __init__(self):
        pass

class Unknown(Message):
    '''An abstract class used to indicate an unexpected message.
    '''
    def __init__(self):
        Message.__init__(self)

#
#

class Incognito(Message):
    '''A class that holds the recovered materials of an unregistered message.
    '''
    def __init__(self, type_name=None, decoded_word=None):
        Message.__init__(self)
        self.type_name = type_name
        self.decoded_word = decoded_word

# A group of functions that exist to allow type descriptions for
# messages to make use of *classes* rather than *instances* of those
# classes;
#     VectorOf(Float8)
# instead of;
#     VectorOf(Float8())
# Unclear on best design/engineering response to the issue but
# certainly this results in fewer parentheses and quicker development.
# Fully correct declaration of user-defined messages quite verbose
# and consequently less clear;
#     VectorOf(SomeMessage)
# vs;
#     VectorOf(UserDefined(SomeMessage))

def is_message_class(a):
    try:
        b = issubclass(a, Message)
    except TypeError:
        return False
    return b

# Holds nested names that would be helpful in the event
# of an error.
class TypeTrack(Exception):
    def __init__(self, name, reason):
        Exception.__init__(self)
        if name:
            self.path = [name]
        else:
            self.path = []
        self.reason = reason

def correct_track(e):
    t = '.'.join(reversed(e.path))
    return t

# Default initializers for tricky types.
# Want an instance of the type but preferrably
# without side-effects. Most containers need
# a fresh instance of themselves (i.e. list,
# deque...) but UUID construction considered
# too expensive. Everyone gets the same UUID.
# default_array does not exist cos should be
# using from_memory.

DEFAULT_UUID = uuid.uuid4()

def default_time():
    '''A function for initializing a time variable, i.e. ``WorldTime``, ``ClockTime`` or ``TimeSpan``.

    :return: a meaningless time value
    :rtype: float
    '''
    return float()

def default_uuid():
    '''A function for initializing a UUID variable.

    :return: a global, constant UUID value
    :rtype: uuid.UUID
    '''
    return DEFAULT_UUID

def default_vector():
    '''A function for initializing a vector variable.

    :return: a fresh, empty vector
    :rtype: list
    '''
    return list()

def default_set():
    '''A function for initializing a set variable.

    :return: a fresh, empty set
    :rtype: set
    '''
    return set()

def default_map():
    '''A function for initializing a map variable.

    :return: a fresh, empty map
    :rtype: dict
    '''
    return dict()

def default_deque():
    '''A function for initializing a deque variable.

    :return: a fresh, empty double-ended queue
    :rtype: collections.deque
    '''
    return deque()

def default_value(te):
    '''A function for initializing any variable with an associated type expression.

    :param te: see :ref:`type expression<type-expressions>`
    :return: an item of application data
    '''
    f = fix_type(t)
    v = from_memory(f)
    return v

# Allow the use of basic python types
# in type expressions.
equivalent = {
    bool:       Boolean,
    int:        Integer8,
    float:      Float8,
    bytearray:  Block,
    bytes:      String,
    str:        Unicode,
    uuid.UUID:  UUID,
}

# Promote parameter a from class to instance, as required.'
def fix_type(a):
    if is_type(a):
        if not is_container(a):
            return a    # No change.
        # Fall thru for structured processing.
    elif is_type_class(a):
        if not is_container_class(a):
            return a()  # Promotion of simple type.
        raise TypeTrack(a.__name__, 'container class used in type information, instance required')
    elif is_message_class(a):
        return UserDefined(a)
    else:
        try:
            e = equivalent[a]
            return e()
        except KeyError:
            pass
        raise TypeTrack(None, 'not one of the portable types')

    # We have an instance of a structuring.
    try:
        name = a.__class__.__name__
        if isinstance(a, ArrayOf):
            a.element = fix_type(a.element)
        elif isinstance(a, VectorOf):
            a.element = fix_type(a.element)
        elif isinstance(a, SetOf):
            a.element = fix_type(a.element)
        elif isinstance(a, MapOf):
            a.key = fix_type(a.key)
            a.value = fix_type(a.value)
        elif isinstance(a, DequeOf):
            a.element = fix_type(a.element)
        elif isinstance(a, UserDefined):
            if not is_message_class(a.element):
                raise TypeTrack(None, 'not a user-defined Message')
        elif isinstance(a, PointerTo):
            a.element = fix_type(a.element)
        else:
            raise TypeTrack(None, 'unexpected container type')
    except TypeTrack as e:
        e.path.append(name)
        raise e
    return a

# Promote schema items from class to instance, as required.'
def fix_schema(name, schema):
    if schema is None:
        return
    d = {}
    for k, t in schema.items():
        try:
            d[k] = fix_type(t)
        except TypeTrack as e:
            track = correct_track(e)
            raise MessageRegistrationError('%s.%s' % (track, name), e.reason)
    schema.update(d)

# Is name present in the explicit map of types.'
def override(name, explicit):
    if not explicit:
        return None

    try:
        t = explicit[name]
        return t
    except KeyError:
        return None

def compile_schema(message, explicit_declarations):
    '''
    Produce the best-possible type information for the specified
    message, using the class and the app-supplied declarations. The
    declarations override any default info that might otherwise be
    acquired from the message.
    '''
    name = message.__name__

    fix_schema(name, explicit_declarations)
    try:
        m = message()
    except TypeError:
        raise MessageRegistrationError('%s' % (name,), 'not default constructable')
    d = getattr(m, '__dict__', None)
    r = {}
    if d:
        for k, a in d.items():
            explicit = override(k, explicit_declarations)
            if explicit:
                t = explicit
            else:
                t = infer_memory(a)

            if not t:
                name_k = "%s.%s" % (name, k)
                reason = 'not enough type information provided/discoverable'
                raise MessageRegistrationError(name_k, reason)
            r[k] = t
    return r

# Each language type is assigned an equivalent memory
# type. This is the map that holds those assignments.
# No entry indicates no assigned equivalent.
inference = {
    bool:       Boolean(),
    int:        Integer8(),
    float:      Float8(),
    bytearray:  Block(),
    bytes:      String(),
    str:        Unicode(),
    uuid.UUID:  UUID(),
}

def infer_memory(a):
    'Maps an instance of a Python type to the proper memory description, or None.'
    try:
        t = inference[a.__class__]
        return t
    except AttributeError:
        return None     # No class.
    except KeyError:
        pass
    if isinstance(a, Message):
        return UserDefined(a.__class__)
    try:
        if issubclass(a, Message):
            return Type()
    except TypeError:
        pass
    return None

# Machinery for manufacture of Python objects equivalent to
# a memory description.
from_class = {
    Boolean: bool,
    Byte: int,
    # Default ctor produces
    # a zero-length string.
    Character: lambda: b' ',
    Rune: lambda: ' ',
    Integer2: int,
    Integer4: int,
    Integer8: int,
    Unsigned2: int,
    Unsigned4: int,
    Unsigned8: int,
    Float4: float,
    Float8: float,
    Block: bytearray,
    String: bytes,
    Unicode: str,
    Enumeration: int,
    WorldTime: float,
    ClockTime: float,
    TimeSpan: float,
    UUID: uuid.uuid4,
    Type: lambda: None,
    TargetAddress: lambda: NO_SUCH_ADDRESS,
    Address: lambda: NO_SUCH_ADDRESS,
    PointerTo: lambda: None,
    Any: lambda: None,

    VectorOf: list,
    SetOf: set,
    MapOf: dict,
    DequeOf: deque,
}

#
#
def from_memory(t):
    'Manufactures the Python equivalent of the memory description, or None.'
    if not is_type(t):
        raise MessageRegistrationError(None, 'non-memory type presented for construction')

    try:
        c = from_class[t.__class__]
        return c()
    except KeyError:
        pass
    except TypeError:
        raise MessageRegistrationError(None, 'internal failure to create from class')

    # Following types are more involved - cant be
    # ctor'd solely from the class.
    if isinstance(t, ArrayOf):
        d = [None] * t.size
        for i in range(t.size):
            d[i] = from_memory(t.element)
        return d

    if isinstance(t, UserDefined):
        return t.element()

    raise MessageRegistrationError(None, 'internal failure to create from memory')

def or_from_memory(a, t):
    if a:
        return a
    return from_memory(t)

#
#
def decode_type(s):
    '''Converts the dotted string *s* to a class, or None.'''
    try:
        i = s.rindex('.')
    except ValueError:
        return None
    module = s[:i]
    name = s[i + 1:]
    try:
        m = sys.modules[module]
    except KeyError:
        return None

    try:
        c = m.__dict__[name]
    except KeyError:
        return None
    return c

def encode_type(c):
    '''Converts the class *c* to a dotted string representation.'''
    b = c.__art__     # Ansar runtime.
    e = '%s.%s' % (b.module, b.name)
    return e

def major_minor(tag):
    s = tag.split('.')
    try:
        m = int(s[0])
        n = int(s[1])
    except IndexError:
        raise MessageError('cannot access major/minor numbers in %r' % (tag,))
    except ValueError:
        raise MessageError('cannot use major/minor in %r' % (tag,))
    except TypeError:
        raise MessageError('non-integer version tag %r' % (tag,))

    return [m, n]

def current_version(c):
    if not is_message_class(c):
        return '0.0'
    r = c.__art__
    v = r.version_history
    if v is None:
        return '0.0'
    return v[-1][0]

#
#
def bind_message(message, type_details=None, version_history=None, message_trail=True, execution_trace=True, copy_before_sending=True, not_portable=False):
    """
    Sets the runtime controls for the given message type. Returns nothing.

    This function adds control values to the class scope of the given
    message type. These then affect the behaviour for all instances of
    that type.

    Parameters:

    - `message`, a class derived from ``Message``.
    - `message_trail`, enable a log when an instance of this message is sent.
    - `version_history`, audit trail of tag+description pairs.
    - `execution_trace`, enable a log when an instance of this message is received.
    - `copy_before_sending`, enable the copying of messages for thread-safety reasons.

    Returns:

    None.
    """
    if not_portable:
        schema = None
    else:
        schema = compile_schema(message, type_details)

    rt = Runtime(message.__name__, message.__module__, schema, version_history,
                      message_trail=message_trail,
                      execution_trace=execution_trace,
                      copy_before_sending=copy_before_sending,
                      not_portable=not_portable)

    # TODO
    # Crude check for whether the new type is
    # properly registered - can an instance
    # be created from its portable type id.
    if not decode_type(rt.path):
        raise MessageRegistrationError(message.__name__, 'not a global level class?')

    setattr(message, '__art__', rt)


bind_message(Unknown)
bind_message(Incognito, type_details={
    'type_name': String,
    'decoded_word': Word,
})

#
#
def equal_to(a, b, t=None):
    if t is None:
        if not isinstance(b, Message):
            return a == b
        if not isinstance(a, b.__class__):
            return False
        t = UserDefined(b.__class__)
        
    if isinstance(t, ArrayOf):
        if len(a) != len(b):
            return False
        return all(equal_to(i, j, t.element) for i, j in zip(a, b)) 
    elif isinstance(t, VectorOf):
        if len(a) != len(b):
            return False
        return all(equal_to(i, j, t.element) for i, j in zip(a, b)) 
    elif isinstance(t, DequeOf):
        if len(a) != len(b):
            return False
        return all(equal_to(i, j, t.element) for i, j in zip(a, b)) 
    elif isinstance(t, SetOf):
        #if len(a) != len(b):
        #    return False
        #return all(i in a for i in b)
        return a == b
    elif isinstance(t, MapOf):
        if len(a) != len(b):
            return False
        return all(k in b and equal_to(a[k], v, t.value) for k, v in b.items())
    elif isinstance(t, UserDefined):
        x = t.element.__art__
        for k, v in x.value.items():
            try:
                l = getattr(a, k)
                r = getattr(b, k)
            except AttributeError:
                return False
            if not equal_to(l, r, v):
                return False
        return True
    elif isinstance(t, PointerTo):
        # TODO
        # Perhaps more correct to compare the
        # identities, but tricky one in the
        # python, handle-based model.
        if equal_to(a, b, t.element):
            return True
        return False
    else:
        return a == b 
