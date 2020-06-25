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
This module provides the basis for implementation of all codecs, i.e. the
Ansar objects that can encode and decode items of application data.

Encoding and decoding is split into a 2-layer process. The upper layer
deals with the conversion of application data to and from an internal
generic form. The lower layer is dedicated to the rendering of generic
forms into specific representations and the subsequent parsing of those
representations back into generic forms.

The :py:class:`~ansar.code.Codec` class provides the upper layer. Lower
layers are provided by classes such as :py:class:`~ansar.json.CodecJson`.
The latter derives from the former, inheriting 2 important methods -
:py:meth:`~ansar.codec.Codec.encode` and :py:meth:`~ansar.codec.Codec.decode`.

    .. code-block:: python

        # Define the wrapper around the JSON encoding
        # primitives.
        class CodecJson(Codec):

These 2 methods manage the combination of the two layers, presenting an
encoding-independent interface for all serialization activities within
the library.

.. autoclass:: CodecError

.. autoclass:: CodecUsage

.. autoclass:: CodecFailed

.. autoclass:: Codec
   :members:
   :no-undoc-members:

.. autofunction:: python_to_word

.. autofunction:: word_to_python
"""
__docformat__ = 'restructuredtext'

import base64
import uuid
import types

from .memory import *
from .convert import *
from .runtime import *
from .message import *


__all__ = [
    'TypeType',
    'NoneType',
    'CodecError',
    'CodecUsage',
    'CodecFailed',
    'python_to_word',
    'word_to_python',
    'INITIAL_VERSION',
    'INITIAL_SUPPORT',
    'SCENARIO_INAPPROPRIATE',
    'SCENARIO_UNSUPPORTED',
    'SCENARIO_BEHIND',
    'SCENARIO_AHEAD',
    'SCENARIO_SAME',
    'version_scenario',
    'Codec',
]

#
#
TypeType = type
NoneType = type(None)

#
#
class CodecError(Exception):
    '''Base exception for all codec exceptions.
    
    :param note: a short, helpful description
    :type note: str
    '''
    def __init__(self, note):
        Exception.__init__(self)
        self.note = note
    
    def __str__(self):
        return self.note

class CodecUsage(CodecError):
    '''The codec cannot proceed due to its supplied environment such as unusable parameters.
    
    :param note: a short, helpful description
    :type note: str
    :param a: values to be substituted into ``note``
    :type a: list
    '''
    def __init__(self, note, *a):
        CodecError.__init__(self, note % a)

class CodecFailed(CodecError):
    '''The codec failed during encoding or decoding activity, such as parsing.
    
    :param note: a short, helpful description
    :type note: str
    :param a: values to be substituted into ``note``
    :type a: list
    '''
    def __init__(self, note, *a):
        CodecError.__init__(self, note % a)

class EnumerationFailed(Exception):
    def __init__(self, note):
        Exception.__init__(self, note)

class CircularReference(Exception):
    pass

# Transform python data to generic words. Immediately below
# are the code fragments that perform conversions from a
# specific type of python data to a declared Ansar type.
# These fragments are loaded into a jump table and the
# python_to_word function packages proper access to the
# table.
#
# All application data is reduced to an instance of the
# following types. All language and Ansar type information
# is cleared away. The generic types are;
#
# * bool .....
# * int ......
# * float ....
# * str ...... unicode
# * list ..... [v, v, v, ...]
# * dict ..... {k: v, k: v, ...}
# * none ..... null
#
# e.g.;
# * an array of 8 integers will be rendered as a list.
# * a map<string,list<int>> will be rendered as a list of pairs.
# * the dict type is reserved for rendering of structs/objects.

def pass_thru(c, p, t):
    return p

def p2w_block(c, p, t):
    w = base64.b64encode(p)
    w = w.decode(encoding='utf-8', errors='strict')
    return w

def p2w_string(c, p, t):
    w = p.decode(encoding='utf-8', errors='strict')
    return w

def p2w_world(c, p, t):
    w = world_iso(p)
    return w

def p2w_clock(c, p, t):
    w = clock_iso(p)
    return w

def p2w_span(c, p, t):
    w = span_to_text(p)
    return w

def p2w_uuid(c, p, t):
    w = uuid_to_text(p)
    return w

def p2w_enumeration(c, p, t):
    try:
        w = t.to_name(p)
    except KeyError:
        m = '/'.join(t.kv.keys())
        raise EnumerationFailed('no name for %d in "%s"' % (p, m))
    return w

def p2w_message(c, p, t):
    schema = t.element.__art__.value
    w = {}
    for k, v in schema.items():
        c.stack.append(k)
        m = getattr(p, k)
        w[k] = python_to_word(c, m, v)
        c.stack.pop()
    return w

def p2w_array(c, p, t):
    e = t.element
    n = len(p)
    s = t.size
    if n != s:
        raise ValueError('array size vs specification - %d/%d' % (n, s))
    w = []
    for i, y in enumerate(p):
        c.stack.append(i)
        a = python_to_word(c, y, e)
        w.append(a)
        c.stack.pop()
    return w

def p2w_vector(c, p, t):
    e = t.element
    w = []
    for i, y in enumerate(p):
        c.stack.append(i)
        a = python_to_word(c, y, e)
        w.append(a)
        c.stack.pop()
    return w

def p2w_set(c, p, t):
    e = t.element
    w = []
    for y in p:
        a = python_to_word(c, y, e)
        w.append(a)
    return w

def p2w_map(c, p, t):
    k_t = t.key
    v_t = t.value
    w = []
    for k, v in p.items():
        a = python_to_word(c, k, k_t)
        b = python_to_word(c, v, v_t)
        w.append([a, b])
    return w

def p2w_deque(c, p, t):
    e = t.element
    w = []
    for y in p:
        a = python_to_word(c, y, e)
        w.append(a)
    return w

def p2w_pointer(c, p, t):
    k = id(p)
    try:
        a = c.aliased[k]
        return a[0]
    except KeyError:
        pass
    a = c.reserve(k)
    w = python_to_word(c, p, t.element)
    a[1] = w
    return a[0]

def p2w_type(c, p, t):
    b = p.__art__
    w = b.path
    return w

def p2w_target(c, p, t):
    # TODO
    # Perhaps the JSON encoder passes this
    # through as a list anyway. No need for
    # transform?
    w = list(p)
    return w

def p2w_address(c, p, t):
    # Check to see if an address is being
    # passed back over the connection it
    # arrived on. Prevents trombone behaviour.
    # Detection happens *here* at the remote
    # end of the trombone because this codec
    # knows it is sending an address back to
    # where it came from. Add the invalid point
    # id. See w2p_address.
    if c.return_proxy is not None:
        a = c.return_proxy
        if p[-1] == a:
            # Need to advise remote that address
            # is returning to where it came from.
            w = list(p[:-1])    # DROP THIS PROXY
            w.append(0)         # SPECIAL MARK
            return w
    w = list(p)
    return w

def p2w_any(c, p, t):
    a = p.__class__
    if a == Incognito:
        t = p.type_name
        w = p.decoded_word
    else:
        t = python_to_word(c, a, Type())
        w = python_to_word(c, p, UserDefined(a))
    return [t, w]

# Map the python+memory pair to a dedicated
# transform function.
p2w = {
    # Direct mappings.
    (bool, Boolean): pass_thru,
    (int, Byte): pass_thru,
    (bytes, Character): p2w_string,
    (str, Rune): pass_thru,
    (int, Integer2): pass_thru,
    (int, Integer4): pass_thru,
    (int, Integer8): pass_thru,
    (int, Unsigned2): pass_thru,
    (int, Unsigned4): pass_thru,
    (int, Unsigned8): pass_thru,
    (float, Float4): pass_thru,
    (float, Float8): pass_thru,
    (int, Enumeration): p2w_enumeration,
    (bytearray, Block): p2w_block,
    (bytes, String): p2w_string,
    (str, Unicode): pass_thru,
    (float, WorldTime): p2w_world,
    (float, ClockTime): p2w_clock,
    (float, TimeSpan): p2w_span,
    (uuid.UUID, UUID): p2w_uuid,
    (list, ArrayOf): p2w_array,
    (list, VectorOf): p2w_vector,
    (set, SetOf): p2w_set,
    (dict, MapOf): p2w_map,
    (deque, DequeOf): p2w_deque,
    (TypeType, Type): p2w_type,
    (tuple, TargetAddress): p2w_target,
    (tuple, Address): p2w_address,

    # PointerTo - can be any of the above.
    (bool, PointerTo): p2w_pointer,
    (int, PointerTo): p2w_pointer,
    (float, PointerTo): p2w_pointer,
    (bytearray, PointerTo): p2w_pointer,
    (bytes, PointerTo): p2w_pointer,
    (str, PointerTo): p2w_pointer,
    (uuid.UUID, PointerTo): p2w_pointer,
    (list, PointerTo): p2w_pointer,
    (set, PointerTo): p2w_pointer,
    (dict, PointerTo): p2w_pointer,
    (deque, PointerTo): p2w_pointer,
    (TypeType, PointerTo): p2w_pointer,
    (tuple, PointerTo): p2w_pointer,
    (Message, PointerTo): p2w_pointer,

    # Two mechanisms for including messages
    (Message, UserDefined): p2w_message,
    (Message, Any): p2w_any,

    # Support for Word, i.e. passthru anything
    # that could have been produced by the functions
    # above. No iterating nested layers.

    (bool, Word): pass_thru,
    (int, Word): pass_thru,
    (float, Word): pass_thru,
    #(bytearray, Word): pass_thru,
    #(bytes, Word): pass_thru,
    (str, Word): pass_thru,
    (list, Word): pass_thru,
    (dict, Word): pass_thru,
    # set, tuple - do not appear in generic

    # Provide for null values being
    # presented for different universal
    # types.

    (NoneType, Boolean): pass_thru,
    (NoneType, Byte): pass_thru,
    (NoneType, Character): pass_thru,
    (NoneType, Rune): pass_thru,
    (NoneType, Integer2): pass_thru,
    (NoneType, Integer4): pass_thru,
    (NoneType, Integer8): pass_thru,
    (NoneType, Unsigned2): pass_thru,
    (NoneType, Unsigned4): pass_thru,
    (NoneType, Unsigned8): pass_thru,
    (NoneType, Float4): pass_thru,
    (NoneType, Float8): pass_thru,
    (NoneType, Block): pass_thru,
    (NoneType, String): pass_thru,
    (NoneType, Unicode): pass_thru,
    (NoneType, WorldTime): pass_thru,
    (NoneType, ClockTime): pass_thru,
    (NoneType, TimeSpan): pass_thru,
    (NoneType, UUID): pass_thru,
    (NoneType, Enumeration): pass_thru,
    (NoneType, UserDefined): pass_thru,
    (NoneType, ArrayOf): pass_thru,
    (NoneType, VectorOf): pass_thru,
    (NoneType, SetOf): pass_thru,
    (NoneType, MapOf): pass_thru,
    (NoneType, DequeOf): pass_thru,
    (NoneType, PointerTo): pass_thru,
    (NoneType, Type): pass_thru,
    (NoneType, TargetAddress): pass_thru,
    (NoneType, Address): pass_thru,
    (NoneType, Word): pass_thru,
    (NoneType, Any): pass_thru,
}

def python_to_word(c, p, t):
    '''
    Generate the generic word equivalent for the supplied
    application data.

    Parameters:

    - `c`, the active codec.
    - `p`, the item of application data.
    - `t`, the memory description of `p`.

    Returns:

    A generic word, ready for serialization.
    '''
    try:
        if isinstance(p, Message):
            a = Message
        else:
            a = getattr(p, '__class__')
    except AttributeError:
        a = None

    try:
        b = t.__class__         # One of the universal types.
    except AttributeError:
        b = None
    
    if a is None:
        if b is None:
            raise TypeError('data and specification are unusable')
        raise TypeError('data with specification "%s" is unusable' % (b.__name__,))
    elif b is None:
        raise TypeError('specification with data "%s" is unusable' % (a.__name__,))

    try:
        f = p2w[a, b]
    except KeyError:
        raise TypeError('no transformation for data/specification %s/%s' % (a.__name__, b.__name__))

    # Apply the transform function
    return f(c, p, t)

# From generic data (after parsing) to final python
# representation in the application.

def w2p_character(c, w, t):
    p = w.encode('ascii', 'strict')
    return p

def w2p_string(c, w, t):
    p = w.encode('ascii', 'strict')
    return p

def w2p_block(c, w, t):
    p = base64.b64decode(w)
    return bytearray(p)

def w2p_world(c, w, t):
    p = world_epoch(w)
    if p is None:
        raise ValueError('"%s" is not a conforming world time' % (w,))
    return p

def w2p_clock(c, w, t):
    p = clock_epoch(w)
    if p is None:
        raise ValueError('"%s" is not a conforming clock time' % (w,))
    return p

def w2p_span(c, w, t):
    p = text_to_span(w)
    if p is None:
        raise ValueError('"%s" is not a conforming span' % (w,))
    return p

def w2p_uuid(c, w, t):
    p = text_to_uuid(w)     # Throws a ValueError.
    return p

def w2p_enumeration(c, w, t):
    try:
        p = t.to_number(w)
    except KeyError:
        m = '/'.join(t.kv.keys())
        raise EnumerationFailed('no number for %s in "%s"' % (w, m))
    return p

def w2p_message(c, w, t):
    p = t.element()
    schema = t.element.__art__.value
    for k, v in schema.items():
        c.stack.append(k)
        d = w.get(k, None)
        if d is None:       # Allow generic to not have member.
            c.stack.pop()
            continue
        def patch(a):
            setattr(p, k, a)
        try:
            a = word_to_python(c, d, v)
            setattr(p, k, a)
        except CircularReference:
            c.patching.append([d, patch])
        c.stack.pop()
    return p

def w2p_pointer(c, a, t):
    # None is handled in the table
    # (NoneType, PointerTo): pass_thru

    # 1. Is this a recursive visit to a - throw.
    # 2. Has the aliased word aleady been decoded.
    # 3. Find the shipped generic word.
    # 4. Guarded decode of generic word.
    # 5. Remember the decode.

    if a in c.called:
        raise CircularReference()

    try:
        p = c.decoded[a]
        return p
    except KeyError:
        pass

    try:
        w = c.pointed[a]
    except KeyError:
        raise CodecUsage('pointer alias not in materials')

    c.called.add(a)
    p = word_to_python(c, w, t.element)
    c.called.remove(a)

    c.decoded[a] = p
    return p

def w2p_type(c, w, t):
    p = decode_type(w)
    return p

def w2p_array(c, w, t):
    e = t.element
    n = len(w)
    s = t.size
    if n != s:
        raise ValueError('array size vs specification - %d/%d' % (n, s))
    p = []
    for i, d in enumerate(w):
        c.stack.append(i)
        def patch(a):
            p[i] = a
        try:
            a = word_to_python(c, d, e)
            p.append(a)
        except CircularReference:
            p.append(None)
            c.patching.append([d, patch])
        c.stack.pop()
    return p

def w2p_vector(c, w, t):
    e = t.element
    p = []
    for i, d in enumerate(w):
        c.stack.append(i)
        def patch(a):
            p[i] = a
        try:
            a = word_to_python(c, d, e)
            p.append(a)
        except CircularReference:
            p.append(None)
            c.patching.append([d, patch])
        c.stack.pop()
    return p

def w2p_set(c, w, t):
    e = t.element
    p = set()
    for d in w:
        a = word_to_python(c, d, e)
        p.add(a)
    return p

def w2p_map(c, w, t):
    k_t = t.key
    v_t = t.value
    p = {}
    for d in w:
        k = word_to_python(c, d[0], k_t)
        def patch(a):
            p[k] = a
        try:
            v = word_to_python(c, d[1], v_t)
            p[k] = v
        except CircularReference:
            c.patching.append([d[1], patch])
    return p

def w2p_deque(c, w, t):
    e = t.element
    p = deque()
    for i, d in enumerate(w):
        def patch(a):
            p[i] = a
        try:
            a = word_to_python(c, d, e)
            p.append(a)
        except CircularReference:
            p.append(None)
            c.patching.append([d, patch])
    return p

def w2p_target(c, w, t):
    if c.local_termination is None:
        p = tuple(w)
    elif len(w) < 2:
        p = c.local_termination,
    else:
        p = tuple(w[:-1])
    return p

def w2p_address(c, w, t):
    if c.return_proxy is not None:
        # Clean out any trombone detected
        # in the remote. See p2w_address.
        a = w[-1]
        if a == 0:      # SPECIAL MARK
            # Address has returned home
            # No need to append a trip back
            # over this connection.
            w.pop()
        else:
            w.append(c.return_proxy)
    p = tuple(w)                 # Now convert.
    return p

def w2p_null_pointer(c, w, t):
    return [0, None]

def w2p_any(c, w, t):
    e = word_to_python(c, w[0], Type())
    if e is None:
        p = Incognito(w[0], w[1])
    else:
        p = word_to_python(c, w[1], UserDefined(e))
    return p

#
#
w2p = {
    # Direct mappings. Left part of key is
    # the type used in a generic representation to
    # pass the intended ansar type, i.e. if we are
    # expecting b then it should arrive as an a.
    (bool, Boolean): pass_thru,
    (int, Byte): pass_thru,
    (str, Character): w2p_character,
    (str, Rune): pass_thru,
    (int, Integer2): pass_thru,
    (int, Integer4): pass_thru,
    (int, Integer8): pass_thru,
    (int, Unsigned2): pass_thru,
    (int, Unsigned4): pass_thru,
    (int, Unsigned8): pass_thru,
    (float, Float4): pass_thru,
    (float, Float8): pass_thru,
    (str, Block): w2p_block,
    (str, String): w2p_string,
    (str, Unicode): pass_thru,
    (str, WorldTime): w2p_world,
    (str, ClockTime): w2p_clock,
    (str, TimeSpan): w2p_span,
    (str, UUID): w2p_uuid,
    (str, Enumeration): w2p_enumeration,
    (list, ArrayOf): w2p_array,
    (list, VectorOf): w2p_vector,
    (list, SetOf): w2p_set,
    (list, MapOf): w2p_map,
    (list, DequeOf): w2p_deque,
    (list, TargetAddress): w2p_target,
    (list, Address): w2p_address,
    (int, PointerTo): w2p_pointer,

    # Two mechanisms for including messages
    # and the representation of message type.
    (dict, UserDefined): w2p_message,
    (list, Any): w2p_any,
    (str, Type): w2p_type,

    # Support for Word, i.e. passthru anything
    # that could have been produced by generic
    # layer. No iterating nested layers.

    (bool, Word): pass_thru,
    (int, Word): pass_thru,
    (float, Word): pass_thru,
    (str, Word): pass_thru,
    (list, Word): pass_thru,
    (dict, Word): pass_thru,

    # Provide for null values being
    # presented for different universal
    # types.

    (NoneType, Boolean): pass_thru,
    (NoneType, Byte): pass_thru,
    (NoneType, Character): pass_thru,
    (NoneType, Rune): pass_thru,
    (NoneType, Integer2): pass_thru,
    (NoneType, Integer4): pass_thru,
    (NoneType, Integer8): pass_thru,
    (NoneType, Unsigned2): pass_thru,
    (NoneType, Unsigned4): pass_thru,
    (NoneType, Unsigned8): pass_thru,
    (NoneType, Float4): pass_thru,
    (NoneType, Float8): pass_thru,
    (NoneType, Block): pass_thru,
    (NoneType, String): pass_thru,
    (NoneType, Unicode): pass_thru,
    (NoneType, WorldTime): pass_thru,
    (NoneType, ClockTime): pass_thru,
    (NoneType, TimeSpan): pass_thru,
    (NoneType, UUID): pass_thru,
    (NoneType, Enumeration): pass_thru,
    (NoneType, UserDefined): pass_thru,
    (NoneType, ArrayOf): pass_thru,
    (NoneType, VectorOf): pass_thru,
    (NoneType, SetOf): pass_thru,
    (NoneType, MapOf): pass_thru,
    (NoneType, DequeOf): pass_thru,
    (NoneType, PointerTo): pass_thru,
    (NoneType, Type): pass_thru,
    (NoneType, TargetAddress): pass_thru,
    (NoneType, Address): pass_thru,
    (NoneType, Word): pass_thru,
    (NoneType, Any): pass_thru,
}

#
#
def word_to_python(c, w, t):
    '''
    Transform the supplied generic word to a valid
    instance of the described application data.

    Parameters:

    - `c`, the active codec.
    - `w`, the generic word.
    - `t`, the memory description of the intended data.

    Returns:

    An instance of application data.
    '''
    try:
        a = w.__class__     # The generic type.
    except AttributeError:
        a = None

    try:
        b = t.__class__     # One of the universal types.
    except AttributeError:
        b = None
    
    if a is None:
        if b is None:
            raise TypeError('data and specification are unusable')
        raise TypeError('data with specification "%s" is unusable' % (b.__name__,))
    elif b is None:
        raise TypeError('specification with data "%s" is unusable' % (a.__name__,))

    try:
        f = w2p[a, b]
    except KeyError:
        raise TypeError('no transformation for data/specification %s/%s' % (a.__name__, b.__name__))

    return f(c, w, t)


INITIAL_VERSION = "0.0"
INITIAL_SUPPORT = [INITIAL_VERSION, INITIAL_VERSION]

SCENARIO_INAPPROPRIATE = 0
SCENARIO_UNSUPPORTED = 1
SCENARIO_BEHIND = 2
SCENARIO_AHEAD = 3
SCENARIO_SAME = 4

def version_scenario(remote, local):
    # Access the major+minor arrays.
    remote_support = major_minor(remote[0])
    remote_current = major_minor(remote[1])
    local_support = major_minor(local[0])
    local_current = major_minor(local[1])

    if remote_current[0] != local_current[0]:
        return None, SCENARIO_INAPPROPRIATE

    # Drop down to just the minor number.
    remote_support = remote_support[1]
    remote_current = remote_current[1]
    local_support = local_support[1]
    local_current = local_current[1]

    if remote_current < local_current:
        if remote_current < local_support:
            return None, SCENARIO_UNSUPPORTED   # Too far behind.
        return remote[1], SCENARIO_BEHIND
    elif remote_current > local_current:
        if remote_support > local_current:
            return None, SCENARIO_UNSUPPORTED   # Too far ahead.
        return None, SCENARIO_AHEAD
    return None, SCENARIO_SAME

# The base class for all codecs and essentially a
# wrapping around 2 functions;
# 1. word to text representation (w2t)
# 2. text representation to word (t2w - parsing)

STARTING_ALIAS = 1100

class Codec(object):
    '''Base class for all codecs, e.g. CodecJson

    :param extension: the additional text added to file names, e.g. ``json``
    :type extension: str
    :param w2t: the low-level conversion of application data to its text representation
    :type w2t: function
    :param t2w: the low-level parsing of text back to application data.
    :type t2w: function
    :param return_proxy: an address that the codec will use to transform deserialized addresses.
    :type return_proxy: internal
    :param local_termination: an address the codec will use to transform deserialized, “to” addresses.
    :type local_termination: internal
    :param pretty_format: generate a human-readable layout, defaults to ``True``
    :type pretty_format: bool
    :param decorate_names: auto-append a dot-extension suffix, defaults to ``True``
    :type decorate_names: bool
    '''
    def __init__(self,
        extension,
        w2t,
        t2w,
        return_proxy, local_termination, pretty_format, decorate_names):
        self.extension = extension
        self.w2t = w2t
        self.t2w = t2w

        if return_proxy is None:
            self.return_proxy = 0,  # Tuple
        elif not isinstance(return_proxy, tuple) or len(return_proxy) != 1:
            raise CodecUsage('unusable address passed as return proxy')
        else:
            self.return_proxy = return_proxy[0]

        if local_termination is None:
            self.local_termination = 0,     # Tuple
        elif not isinstance(local_termination, tuple) or len(local_termination) != 1:
            raise CodecUsage('unusable address passed as local termination')
        else:
            self.local_termination = local_termination[0]

        self.pretty_format = pretty_format
        self.decorate_names = decorate_names

        # Encode/decode collections
        self.stack = []                 # Both ways.
        self.aliased = {}               # Encoding.
        self.called = set()
        self.pointed = {}               # Both.
        self.decoded = {}               # Decoding.
        self.patching = []
        self.serial = STARTING_ALIAS
    
    def reserve(self, k):
        a = [self.serial, None]
        self.serial += 1
        self.aliased[k] = a
        return a

    def encode(self, value, te):
        '''Encode an application value to its stored representation.

        :param value: any application value matching the `te` type expression
        :param te: a formal description of the `value`
        :type te: :ref:`type expression<type-expressions>`
        :return: a portable representation
        :rtype: str
        '''
        # Walk the python object and produce a
        # generic word and the map of pointer-to
        # objects in 'aliased'.
        try:
            self.stack = []
            self.aliased = {}
            self.serial = STARTING_ALIAS
            w = python_to_word(self, value, te)
        except (AttributeError, TypeError, ValueError, IndexError, KeyError, EnumerationFailed) as e:
            text = self.nesting()
            if len(text) == 0:
                raise CodecFailed('transformation (%s)', str(e))
            raise CodecFailed('transformation, near "%s" (%s)', text, str(e))

        # Compile the map of materials that is going to
        # be serialized.
        shipment = {'value': w}
        if len(self.aliased) > 0:
            # Convert id() lookup table to alias lookup
            # table - generic form.
            shipment['aliased'] = [[v[0], v[1]] for _, v in self.aliased.items()]

        # Inject a version tag if thats possible. Only relevant
        # for messages and message can be explicit, any or
        # pointer-to. Not doing versioning for containers of
        # messages. Have to consider incognitos as well.
        def insert_version(v, a):
            vh = v.__art__.version_history
            if vh is not None:
                b = vh[0][0]
                e = vh[-1][0]
                z = b == INITIAL_VERSION and e == INITIAL_VERSION
                if not z:
                    a['_'] = [b, e]

        if isinstance(te, UserDefined):
            insert_version(te.element, w)
        elif isinstance(te, Any) and isinstance(value, Message):
            insert_version(value.__class__, w[1])
        elif isinstance(te, PointerTo) and isinstance(te.element, UserDefined):
            insert_version(te.element.element, w)

        # Serialization of generic form.
        try:
            s = self.w2t(self, shipment)
        except (TypeError, ValueError) as e:
            raise CodecFailed('serialization (%s)', str(e))
        return s

    def decode(self, representation, te):
        '''Decode a representation to its final application form.

        :param representation: the result of a previous encode operation
        :type representation: str
        :param te: a formal description of memory
        :type te: a :ref:`type expression<type-expressions>`
        :return: an application value
        '''
        self.pointed = {}       # Pointed to words
        self.decoded = {}
        self.patching = []

        # Need to de-serialize, unpack the shipment into
        # generic word and pointer-to.
        try:
            shipment = self.t2w(self, representation)
        except (TypeError, ValueError) as e:
            raise CodecFailed('parsing (%s)', str(e))

        def decode(w, te):
            self.stack = []         # Error tracking.
            self.called = set()
            try:
                p = word_to_python(self, w, te)
            except (AttributeError, TypeError, ValueError, IndexError, KeyError, EnumerationFailed) as e:
                text = self.nesting()
                if len(text) == 0:
                    raise CodecFailed('transformation (%s)', str(e))
                raise CodecFailed('transformation, near "%s" (%s)', text, str(e))
            return p

        # Pull the aliased pointer-to materials out
        # of the materials and save into convenient
        # map.
        try:
            self.pointed = decode(shipment['aliased'], MapOf(Integer8(),Word()))
        except KeyError:
            self.pointed = {}

        def compare_versions(v, a):
            vh = v.__art__.version_history
            if vh is not None:
                local = [vh[0][0], vh[-1][0]]
            else:
                local = INITIAL_SUPPORT
            try:
                remote = a.pop('_')
            except KeyError:
                remote = INITIAL_SUPPORT

            v, s = version_scenario(remote, local)
            if s in (SCENARIO_INAPPROPRIATE, SCENARIO_UNSUPPORTED):
                raise CodecFailed('inappropriate or unsupported version')
            return v

        # Pull the generic word out and then pull
        # the version details out of that.
        try:
            w = shipment['value']
        except KeyError:
            raise CodecFailed('no "value" available')

        if isinstance(te, UserDefined):
            v = compare_versions(te.element, w)
        elif isinstance(te, Any):
            # Extra layer of difficulty due to
            # potential for incognitos.
            e = decode_type(w[0])
            if e:
                v = compare_versions(e, w[1])
            else:
                v = None    # Incognito has no history.
        elif isinstance(te, PointerTo) and isinstance(te.element, UserDefined):
            # Pointers have not been resolved so use the actual pointer
            # value (1100+) to lookup generic word. Pull the version info
            # from there.
            v = compare_versions(te.element.element, self.pointed[w])
        else:
            v = None  # Assumption of Same.

        # Can finally decode the word to its final python resting-place.
        # and backpatch any circular references.
        p = decode(w, te)
        for b in self.patching:
            decoded = self.decoded[b[0]]
            f = b[1]
            f(decoded)

        return p, v

    def nesting(self):
        p = ''
        for s in self.stack:
            if isinstance(s, int):
                p += '[%d]' % (s,)
            elif isinstance(s, str):
                if len(p) > 0:
                    p += '.'
                p += '%s' % (s,)
            else:
                p += '<?>'
        return p

    def full_name(self, name):
        if not self.decorate_names:
            return name
        if name[-1] == '.':
            return name[:-1]
        s = '%s.%s' % (name, self.extension)
        return s
