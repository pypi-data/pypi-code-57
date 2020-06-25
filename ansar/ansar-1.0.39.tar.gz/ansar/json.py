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
Implementation of the JSON codec. Refer to;

* https://tools.ietf.org/html/rfc7159
* https://www.json.org/json-en.html


.. autoclass:: CodecJson

.. autofunction:: word_to_json

.. autofunction:: json_to_word
"""
__docformat__ = 'restructuredtext'

import json

from .memory import *
from .convert import *
from .runtime import *
from .message import *
from .codec import *


__all__ = [
    'word_to_json',
    'json_to_word',
    'CodecJson'
]

# Standard JSON library version of generation and
# parsing of standard-conforming text.
def word_to_json(c, w):
    '''
    Generate the JSON representation of a generic word.

    If the codec `pretty_format` property is true, this
    function will produce a more human-readable rendering
    of JSON.

    Parameters:

    - `c`, the active codec.
    - `w`, the generic word to be represented.

    Returns:

    A string containing valid JSON.
    '''
    if c.pretty_format:
        j = json.dumps(w, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        j = json.dumps(w, separators=(',', ':'))
    return j

# Decoding - from parsing of JSON to transformation
# into app data items.

def json_to_word(c, j):
    '''
    Produce a generic word from the parsing of a
    text JSON representation.
     
    :param c: an active codec
    :param j: the JSON text
    :type c: a codec-based instance
    :type j: string
    :rtype: a generic word.
    '''
    j = json.loads(j)
    return j

#
#
class CodecJson(Codec):
    '''Encoding and decoding of JSON representations.

    This class is the default value for the ``encoding`` parameter, related
    to the various store and recover operations of the library. Refer to the
    :ref:`base codec class<codec-base>` for the significant methods.
    '''
    EXTENSION='json'

    def __init__(self, return_proxy=None, local_termination=None, pretty_format=False, decorate_names=True):
        Codec.__init__(self,
            CodecJson.EXTENSION,
            word_to_json,
            json_to_word,
            return_proxy, local_termination, pretty_format, decorate_names)
