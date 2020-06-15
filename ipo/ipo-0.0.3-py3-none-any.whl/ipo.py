#!/usr/bin/env python3

# © 2020, Midgard
# License: LGPL-3.0-or-later

import sys
import io
import csv
from builtins import print as _print, str as _str, list as _list, map as _map


class ipo:
	def __init__(self, function):
		self.function = function


	# Make it possible to pipe, e.g.
	#   [1, 5, 3] | sort
	def __ror__(self, data):
		return self.function(data)


	# Make it possible to provide arguments, e.g. the call to `take` in
	#   [1, 5, 3, 4] | take(3)
	def __call__(self, *args, **kwargs):
		return ipo(lambda data: self.function(data, *args, **kwargs))


	# Enable chaining pipes that have not received data, e.g.
	#   get_top3 = sort | take(3)
	#   top3 = [1, 5, 3, 4] | get_top3
	def __or__(self, other):
		if not isinstance(other, ipo):
			raise TypeError("ipo can only be piped to other ipo")
		return ipo(lambda data: data | self | other)


	def __ior__(self, other):
		self.function = lambda data: data | self | other


	def __str__(self):
		return "| {0!s}".format(self.function)


	def __repr__(self):
		return "ipo({0!r})".format(self.function)


# =================================================================================
# STANDARD LIBRARY

# ----------------------------------------------------
# I/O

stdin = (line.rstrip("\n") for line in sys.stdin)


@ipo
def print(str_or_iter, **kwargs):
	"""
	Print to file.
	"""
	if isinstance(str_or_iter, (_str, bytes)):
		_print(str_or_iter, **kwargs)
		return

	try:
		it = iter(str_or_iter)
	except TypeError:
		_print(str_or_iter, **kwargs)
		return

	for x in it:
		_print(x, **kwargs)


# ----------------------------------------------------
# CSV

readcsv = ipo(csv.reader)


@ipo
def writecsv(data, **kwargs):
	buffer = io.StringIO()
	writer = csv.writer(buffer, **kwargs)
	# FIXME make asynchronous
	writer.writerows(data)
	return (line.split("\n") for line in buffer)


# ----------------------------------------------------
# Iterable stuff

@ipo
def map(data, function, **kwargs):
	(f"data {data}, function {function}") | print
	return _map(function, data, **kwargs)

sort = ipo(sorted)

str = ipo(str)

list = ipo(list)

# dict.items() returns dict_items which overrides __or__, so we need to convert to another iterable
items = ipo(lambda d: tuple(d.items()))


@ipo
def take(data, n):
	for x, _ in zip(data, range(n)):
		yield x


# ----------------------------------------------------
# Examples

x = [5, 2, 3, 1] | sort
x | str | print

y = [5, 2, 3, 1] | take(3) | list
y | str | print

z = [5, 2, 3, 1] | sort | take(3) | list
z | str | print

sort | print
take | print
take(3) | print

f"{sort!r}" | print
f"{take!r}" | print
f"{take(3)!r}" | print

sort_and_take = sort | take(3)
_print(sort_and_take)

_print({"hello": "world", "im": "still alive", "oh": "no"} | items) # | list | print

[r'hello,this,is,it', r'the,end,of,the,world'] | readcsv | map(sort) | writecsv | print
"Eyo" | print
