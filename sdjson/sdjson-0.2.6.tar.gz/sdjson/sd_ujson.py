#  !/usr/bin/env python
#
#  sd_ujson.py
#  Scroll down for license info
"""
JSON encoder utilising functools.singledispatch to support custom encoders
for both Python's built-in classes and user-created classes, without as much legwork.


Creating and registering a custom encoder is as easy as:

>>> import sdjson
>>>
>>> @sdjson.encoders.register(MyClass)
>>> def encode_myclass(obj):
...     return dict(obj)
>>>

In this case, ``MyClass`` can be made JSON-serializable simply by calling
:class:`dict <python:dict>` on it. If your class requires more complicated logic
to make it JSON-serializable, do that here.

Then, to dump the object to a string:

>>> class_instance = MyClass()
>>> print(sdjson.dumps(class_instance))
'{"menu": ["egg and bacon", "egg sausage and bacon", "egg and spam", "egg bacon and spam"],
"today\'s special": "Lobster Thermidor au Crevette with a Mornay sauce served in a Provencale
manner with shallots and aubergines garnished with truffle pate, brandy and with a fried egg
on top and spam."}'
>>>

Or to dump to a file:

>>> with open("spam.json", "w") as fp:
...     sdjson.dumps(class_instance, fp)
...
>>>

``sdjson`` also provides access to :func:`load <python:json.load>`,
:func:`loads <python:json.loads>`, :class:`~python:json.JSONDecoder`,
:class:`~python:json.JSONDecodeError`, and :class:`~python:json.JSONEncoder`
from the :mod:`~python:json` module, allowing you to use ``sdjson`` as a drop-in replacement
for :mod:`~python:json`.

If you wish to dump an object without using the custom encoders, you can pass
a different :class:`~python:json.JSONEncoder` subclass, or indeed
:class:`~python:json.JSONEncoder` itself to get the stock functionality.

>>> sdjson.dumps(class_instance, cls=sdjson.JSONEncoder)
>>>

|

When you've finished, if you want to unregister the encoder you can call:

>>> sdjson.encoders.unregister(MyClass)
>>>

to remove the encoder for ``MyClass``. If you want to replace the encoder with a
different one it is not necessary to call this function: the
``@sdjson.encoders.register`` decorator will replace any existing decorator for
the given class.


TODO: This module does not currently support custom decoders, but might in the future.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Based on https://treyhunner.com/2013/09/singledispatch-json-serializer/
#  Copyright © 2013 Trey Hunner
#  He said "Feel free to use it however you like." So I have.
#
#  Also based on the `json` module (version 2.0.9) by Bob Ippolito from Python 3.7
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com . All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives . All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum . All rights reserved.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# TODO: perhaps add a limit on number of decimal places for floats etc, like with pandas' jsons

__all__ = [
		"load",
		"loads",
		"dump",
		"dumps",
		"encoders",
		"register_encoder",
		"unregister_encoder",
		]

__author__ = "Dominic Davis-Foster"
__copyright__ = "2020 Dominic Davis-Foster"

__license__ = "LGPLv3+"
__version__ = "0.2.3"
__email__ = "dominic@davis-foster.co.uk"

# stdlib
import json

# 3rd party
import ujson  # must be the internet archive fork https://pypi.org/project/ujson-ia/
from domdf_python_tools.doctools import append_docstring_from

# this package
from sdjson import encoders, register_encoder, unregister_encoder
from sdjson.core import sphinxify_json_docstring


@sphinxify_json_docstring()
@append_docstring_from(json.dump)
def dump(obj, fp, **kwargs):
	"""
	Serialize custom Python classes to JSON.
	Custom classes can be registered using the ``@encoders.register(<type>)`` decorator.
	"""

	iterable = dumps(obj, **kwargs)

	for chunk in iterable:
		fp.write(chunk)


def _ujson_hook(obj):
	# Hook to allow custom encoders for ujson
	for type_, handler in encoders.registry.items():
		if isinstance(obj, type_) and type_ is not object:
			return handler(obj)
	return obj


@sphinxify_json_docstring()
@append_docstring_from(json.dumps)
def dumps(
		obj,
		*,
		# skipkeys=False,
		ensure_ascii=True,
		# check_circular=True,
		# allow_nan=True,
		# cls=None,
		indent=None,
		# separators=None,
		default=None,  # Same as pre_encode_hook
		# sort_keys=False,
		encode_html_chars=False,
		escape_forward_slashes=False,
		pre_encode_hook=_ujson_hook,
		**kw,
		):
	"""
	Serialize custom Python classes to JSON.
	Custom classes can be registered using the ``@encoders.register(<type>)`` decorator.
	"""

	if default:
		pre_encode_hook = default

	if indent is None:
		_indent = 0
	elif indent == '\t':
		# TODO: Support for actual tabs
		_indent = 4
	else:
		_indent = indent

	output = ujson.dumps(
			obj,
			ensure_ascii=ensure_ascii,
			indent=_indent,
			encode_html_chars=encode_html_chars,
			escape_forward_slashes=escape_forward_slashes,
			pre_encode_hook=pre_encode_hook,
			**kw,
			)

	return output


# Provide access to remaining objects from ujson module.
load = ujson.load
loads = ujson.loads
encode = dumps
decode = loads
