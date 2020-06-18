# stdlib
import decimal
import platform
from collections import OrderedDict
from io import StringIO

# 3rd party
import pytest  # type: ignore

# this package
import sdjson


def test_decimal():
	rval = sdjson.loads('1.1', parse_float=decimal.Decimal)
	assert isinstance(rval, decimal.Decimal)
	assert rval == decimal.Decimal('1.1')


def test_float():
	rval = sdjson.loads('1', parse_int=float)
	assert isinstance(rval, float)
	assert rval == 1.0


def test_empty_objects():
	assert sdjson.loads('{}') == {}
	assert sdjson.loads('[]') == []
	assert sdjson.loads('""') == ""


def test_object_pairs_hook():
	s = '{"xkd":1, "kcw":2, "art":3, "hxm":4, "qrt":5, "pad":6, "hoy":7}'
	p = [("xkd", 1), ("kcw", 2), ("art", 3), ("hxm", 4), ("qrt", 5), ("pad", 6), ("hoy", 7)]
	assert sdjson.loads(s) == eval(s)
	assert sdjson.loads(s, object_pairs_hook=lambda x: x) == p
	assert sdjson.load(StringIO(s), object_pairs_hook=lambda x: x) == p
	od = sdjson.loads(s, object_pairs_hook=OrderedDict)
	assert od == OrderedDict(p)
	assert type(od) == OrderedDict
	# the object_pairs_hook takes priority over the object_hook
	assert sdjson.loads(s, object_pairs_hook=OrderedDict, object_hook=lambda x: None) == OrderedDict(p)
	# check that empty object literals work (see #17368)
	assert sdjson.loads('{}', object_pairs_hook=OrderedDict) == OrderedDict()
	assert sdjson.loads('{"empty": {}}', object_pairs_hook=OrderedDict) == OrderedDict([('empty', OrderedDict())])


def test_decoder_optimizations():
	# Several optimizations were made that skip over calls to
	# the whitespace regex, so this test is designed to try and
	# exercise the uncommon cases. The array cases are already covered.
	rval = sdjson.loads('{   "key"    :    "value"    ,  "k":"v"    }')
	assert rval == {"key": "value", "k": "v"}


def check_keys_reuse(source, loads):
	rval = loads(source)
	(a, b), (c, d) = sorted(rval[0]), sorted(rval[1])
	assert a == c
	assert b == d


@pytest.mark.skipif(platform.python_implementation() == "PyPy", reason="Strange behaviour with PyPy")
def test_keys_reuse():
	s = '[{"a_key": 1, "b_\xe9": 2}, {"a_key": 3, "b_\xe9": 4}]'
	check_keys_reuse(s, sdjson.loads)
	decoder = sdjson.json.decoder.JSONDecoder()
	check_keys_reuse(s, decoder.decode)
	assert not decoder.memo


def test_extra_data():
	s = '[1, 2, 3]5'
	msg = 'Extra data'
	with pytest.raises(sdjson.JSONDecodeError, match=msg):
		sdjson.loads(s)


def test_invalid_escape():
	s = '["abc\\y"]'
	msg = 'escape'
	with pytest.raises(sdjson.JSONDecodeError, match=msg):
		sdjson.loads(s)


def test_invalid_input_type():
	msg = 'the JSON object must be str'
	for value in [1, 3.14, [], {}, None]:
		with pytest.raises(TypeError, match=msg):
			sdjson.loads(value)


def test_string_with_utf8_bom():

	# stdlib
	import sys

	# see #18958
	bom_json = "[1,2,3]".encode('utf-8-sig').decode('utf-8')
	with pytest.raises(sdjson.JSONDecodeError) as e:
		sdjson.loads(bom_json)
	# TODO:
	if sys.version_info.major >= 3 and sys.version_info.minor == 7:
		assert 'BOM' in str(e)

	with pytest.raises(sdjson.JSONDecodeError) as e:
		sdjson.load(StringIO(bom_json))
	# TODO:
	if sys.version_info.major >= 3 and sys.version_info.minor == 7:
		assert 'BOM' in str(e)

	# make sure that the BOM is not detected in the middle of a string
	bom_in_str = '"{}"'.format(''.encode('utf-8-sig').decode('utf-8'))
	assert sdjson.loads(bom_in_str) == '\ufeff'
	assert sdjson.load(StringIO(bom_in_str)) == '\ufeff'


def test_negative_index():
	d = sdjson.JSONDecoder()
	with pytest.raises(ValueError):
		d.raw_decode('a' * 42, -50000)
