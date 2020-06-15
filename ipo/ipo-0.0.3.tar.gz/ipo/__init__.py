#!/usr/bin/env python3

# © 2020, Midgard
# License: LGPL-3.0-or-later

# pylint: disable=invalid-name

import sys
import io
import csv
import itertools
import re
from functools import wraps
import typing


class ipo:
	def __init__(self, data):
		self.data = data

	# Make it possible to pipe, e.g.
	#   ipo([1, 5, 3]) | sorted
	def __or__(self, function):
		return ipo(function(self.data))

	def __eq__(self, other):
		return other.__class__ == ipo and self.data == other.data

	def __repr__(self):
		return "ipo({0!r})".format(self.data)


def ipo_source(function):
	"""
	Decorator for functions that should return ipo data.
	"""
	@wraps(function)
	def f(*args, **kwargs):
		return ipo(function(*args, **kwargs))
	return f


# =================================================================================
# STANDARD LIBRARY

# ----------------------------------------------------
# I/O

# This must not be decorated with @ipo because it has to generate data.
@ipo_source
def read(file):
	return (line.rstrip("\n") for line in file)

stdin = read(sys.stdin)


def write(str_or_iter, **kwargs):
	"""
	Write to file. If the data is iterable, each item is printed on its own line.

	Exception: strings and bytes are not iterated but printed as-is.
	"""
	if isinstance(str_or_iter, (str, bytes)):
		print(str_or_iter, **kwargs)
		return

	try:
		it = iter(str_or_iter)
	except TypeError:
		print(str_or_iter, **kwargs)
		return

	for x in it:
		print(x, **kwargs)


# ----------------------------------------------------
# CSV

from_csv = csv.reader


def to_csv(data, separator=",", quotechar='"', escapechar=None, quoteall=False):
	# We have our own CSV writer because csv.writer insists upon writing to a file

	if escapechar is None:
		escapechar = quotechar

	def serialize(item):
		if item is None:
			return ""

		item_s = str(item)

		# If item should not be quoted
		if not quoteall and quotechar not in item_s and "\n" not in item_s:
			return item_s

		if quotechar != escapechar:
			item_s = item_s.replace(escapechar, escapechar + escapechar)
		item_s = item_s.replace(quotechar, escapechar + quotechar)
		return quotechar + item_s + quotechar

	return (
		separator.join(serialize(item) for item in line)
		for line in data
	)


T = typing.TypeVar("T")
U = typing.TypeVar("U")
@typing.overload
def recompose(
	selection: typing.Iterable[typing.Callable[[T], U]],
	data: typing.Iterable[T]
) -> typing.Tuple[U]:
	...
@typing.overload
def recompose(
	selection: typing.Iterable[typing.Union[typing.Callable[[T], T], int]],
	data: typing.Sequence[T]
) -> typing.Tuple[T]:
	...

def recompose(selection, data):
	"""
	Recomposition that follows `selection`:
	- each callable is called, the result is taken,
	- each int is used as an index in `data`.

	This is especially useful in conjunction with `map`, e.g. to transform tabular data.

	If ints are used, `data` should support indexing (so a list or tuple is fine,
	but a generator is not).

	>>> from functools import partial as p
	>>> (
	...   ipo([(3, 4, 5), ("a", "b")]) |
	...   p(map, p(recompose,
	...     [0, lambda x: x[0] + x[1]]
	...   )) | list
	... )
	ipo([(3, 7), ("a", "ab")])
	"""
	return tuple(
		(sel(data) if callable(sel) else data[sel])
		for sel in selection
	)


# ----------------------------------------------------
# Iterable stuff


def starstarmap(function, data, *args):
	return map(lambda x: function(*args, **x), data)


flatten = itertools.chain.from_iterable

# Some aliases for common usages of slicing makes things more understandable
def head(n, data):
	return itertools.islice(data, n)
def skip(n, data):
	return itertools.islice(data, n, None)


def before(data_to_prepend, data):
	return itertools.chain(data_to_prepend, data)


def after(data_to_append, data):
	return itertools.chain(data, data_to_append)


def flat_enum(data, start=0):
	return (
		(i, *els)
		for i, els in enumerate(data, start=start)
	)


def intersperse(separator, data):
	it = iter(data)

	# Yield first element
	try:
		yield next(it)
	except StopIteration:
		return

	# Yield remaining elements per pair of (separator, element)
	yield from itertools.chain.from_iterable(
		zip(itertools.repeat(separator), it)
	)


# ----------------------------------------------------
# Dict stuff

def dictmap(function, data):
	return dict(
		function(k, v)
		for k, v in data.items()
	)


# ----------------------------------------------------
# Shell-like utils

def grep(pattern, data, flags=0):
	"""
	Like grep -E or egrep
	"""
	return (
		item
		for item in data
		if re.search(pattern, item, flags)
	)


def grepo(pattern, data, match_objects=False, flags=0):
	"""
	Like grep -E -o (keep only the matched parts, with each such part in a separate output item)

	:param match_objects: False to return strings, True to return tuples of match objects
	"""
	if match_objects:
		for item in data:
			yield from re.finditer(pattern, item, flags)
	else:
		for item in data:
			yield from (
				match.group(0)
				for match in re.finditer(pattern, item, flags)
			)
