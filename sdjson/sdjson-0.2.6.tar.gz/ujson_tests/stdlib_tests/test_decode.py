# stdlib
import decimal
from collections import OrderedDict
from io import StringIO

# 3rd party
import pytest

# this package
import sd_ujson


@pytest.mark.xfail(reason="parse_float is unsupported by ujson")
def test_decimal():
	rval = sd_ujson.loads('1.1', parse_float=decimal.Decimal)
	assert isinstance(rval, decimal.Decimal)
	assert rval == decimal.Decimal('1.1')


@pytest.mark.xfail(parse_int="parse_float is unsupported by ujson")
def test_float():
	rval = sd_ujson.loads('1', parse_int=float)
	assert isinstance(rval, float)
	assert rval == 1.0


def test_empty_objects():
	assert sd_ujson.loads('{}') == {}
	assert sd_ujson.loads('[]') == []
	assert sd_ujson.loads('""') == ""


@pytest.mark.xfail(reason="object_pairs_hook is unsupported by ujson")
def test_object_pairs_hook():
	s = '{"xkd":1, "kcw":2, "art":3, "hxm":4, "qrt":5, "pad":6, "hoy":7}'
	p = [("xkd", 1), ("kcw", 2), ("art", 3), ("hxm", 4),
		 ("qrt", 5), ("pad", 6), ("hoy", 7)]
	assert sd_ujson.loads(s) == eval(s)
	assert sd_ujson.loads(s, object_pairs_hook=lambda x: x) == p
	assert sd_ujson.json.load(StringIO(s),
							object_pairs_hook=lambda x: x) == p
	od = sd_ujson.loads(s, object_pairs_hook=OrderedDict)
	assert od == OrderedDict(p)
	assert type(od) == OrderedDict
	# the object_pairs_hook takes priority over the object_hook
	assert sd_ujson.loads(s, object_pairs_hook=OrderedDict,
						object_hook=lambda x: None) == \
		   OrderedDict(p)
	# check that empty object literals work (see #17368)
	assert sd_ujson.loads('{}', object_pairs_hook=OrderedDict) == \
		   OrderedDict()
	assert sd_ujson.loads('{"empty": {}}',
						object_pairs_hook=OrderedDict) == \
		   OrderedDict([('empty', OrderedDict())])


def test_decoder_optimizations():
	# Several optimizations were made that skip over calls to
	# the whitespace regex, so this test is designed to try and
	# exercise the uncommon cases. The array cases are already covered.
	rval = sd_ujson.loads('{   "key"    :    "value"    ,  "k":"v"    }')
	assert rval == {"key": "value", "k": "v"}


def check_keys_reuse(source, loads):
	rval = loads(source)
	(a, b), (c, d) = sorted(rval[0]), sorted(rval[1])
	assert a == c
	assert b == d


def test_keys_reuse():
	s = '[{"a_key": 1, "b_\xe9": 2}, {"a_key": 3, "b_\xe9": 4}]'
	check_keys_reuse(s, sd_ujson.loads)
	decoder = sd_ujson.json.decoder.JSONDecoder()
	check_keys_reuse(s, decoder.decode)
	assert not decoder.memo


def test_extra_data():
	s = '[1, 2, 3]5'
	msg = 'Trailing data'
	with pytest.raises(ValueError, match=msg):
		sd_ujson.loads(s)


def test_invalid_escape():
	s = '["abc\\y"]'
	msg = "Unrecognized escape sequence when decoding 'string'"
	with pytest.raises(ValueError, match=msg):
		sd_ujson.loads(s)


def test_invalid_input_type():
	msg = 'Expected String or Unicode'
	for value in [1, 3.14, [], {}, None]:
		with pytest.raises(TypeError, match=msg):
			sd_ujson.loads(value)


def test_string_with_utf8_bom():
	# see #18958
	bom_json = "[1,2,3]".encode('utf-8-sig').decode('utf-8')
	with pytest.raises(ValueError, match="Expected object or value") as e:
		sd_ujson.loads(bom_json)
	
	with pytest.raises(ValueError, match="Expected object or value") as e:
		sd_ujson.load(StringIO(bom_json))

	# make sure that the BOM is not detected in the middle of a string
	bom_in_str = '"{}"'.format(''.encode('utf-8-sig').decode('utf-8'))
	assert sd_ujson.loads(bom_in_str) == '\ufeff'
	assert sd_ujson.json.load(StringIO(bom_in_str)) == '\ufeff'


def test_negative_index():
	d = sd_ujson.json.JSONDecoder()
	with pytest.raises(ValueError):
		d.raw_decode('a' * 42, -50000)
