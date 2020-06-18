# stdlib
from collections import OrderedDict

# this package
import sd_ujson
from ..utils import nospace


CASES = [
		('/\\"\ucafe\ubabe\uab98\ufcde\ubcda\uef4a\x08\x0c\n\r\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?',
		 '"/\\\\\\"\\ucafe\\ubabe\\uab98\\ufcde\\ubcda\\uef4a\\b\\f\\n\\r\\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?"'),
		('\u0123\u4567\u89ab\ucdef\uabcd\uef4a', '"\\u0123\\u4567\\u89ab\\ucdef\\uabcd\\uef4a"'),
		('controls', '"controls"'),
		('\x08\x0c\n\r\t', '"\\b\\f\\n\\r\\t"'),
		('{"object with 1 member":["array with 1 element"]}',
		 '"{\\"object with 1 member\\":[\\"array with 1 element\\"]}"'),
		(' s p a c e d ', '" s p a c e d "'),
		('\U0001d120', '"\\ud834\\udd20"'),
		('\u03b1\u03a9', '"\\u03b1\\u03a9"'),
		("`1~!@#$%^&*()_+-={':[,]}|;.</>?", '"`1~!@#$%^&*()_+-={\':[,]}|;.</>?"'),
		('\x08\x0c\n\r\t', '"\\b\\f\\n\\r\\t"'),
		('\u0123\u4567\u89ab\ucdef\uabcd\uef4a', '"\\u0123\\u4567\\u89ab\\ucdef\\uabcd\\uef4a"'),
		]


def test_encode_basestring_ascii():
	fname = sd_ujson.json.encoder.encode_basestring_ascii.__name__
	for input_string, expect in CASES:
		result = sd_ujson.json.encoder.encode_basestring_ascii(input_string)
		assert result == expect, \
			'{0!r} != {1!r} for {2}({3!r})'.format(
					result, expect, fname, input_string)


def test_ordered_dict():
	# See issue 6105
	items = [('one', 1), ('two', 2), ('three', 3), ('four', 4), ('five', 5)]
	s = sd_ujson.dumps(OrderedDict(items))
	assert s == nospace('{"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}')


def test_sorted_dict():
	items = [('one', 1), ('two', 2), ('three', 3), ('four', 4), ('five', 5)]
	s = sd_ujson.dumps(dict(items), sort_keys=True)
	assert s == nospace('{"five": 5, "four": 4, "one": 1, "three": 3, "two": 2}')
