# stdlib
import codecs
from collections import OrderedDict

# 3rd party
import pytest

# this package
import sd_ujson


# test_encoding1 and test_encoding2 from 2.x are irrelevant (only str
# is supported as input, not bytes).

def test_encoding3():
	u = '\N{GREEK SMALL LETTER ALPHA}\N{GREEK CAPITAL LETTER OMEGA}'
	j = sd_ujson.dumps(u)
	assert j == '"\\u03b1\\u03a9"'


def test_encoding4():
	u = '\N{GREEK SMALL LETTER ALPHA}\N{GREEK CAPITAL LETTER OMEGA}'
	j = sd_ujson.dumps([u])
	assert j == '["\\u03b1\\u03a9"]'


def test_encoding5():
	u = '\N{GREEK SMALL LETTER ALPHA}\N{GREEK CAPITAL LETTER OMEGA}'
	j = sd_ujson.dumps(u, ensure_ascii=False)
	assert j == '"{0}"'.format(u)


def test_encoding6():
	u = '\N{GREEK SMALL LETTER ALPHA}\N{GREEK CAPITAL LETTER OMEGA}'
	j = sd_ujson.dumps([u], ensure_ascii=False)
	assert j == '["{0}"]'.format(u)


def test_big_unicode_encode():
	u = '\U0001d120'
	assert sd_ujson.dumps(u) == '"\\ud834\\udd20"'
	assert sd_ujson.dumps(u, ensure_ascii=False) == '"\U0001d120"'


def test_big_unicode_decode():
	u = 'z\U0001d120x'
	assert sd_ujson.loads('"' + u + '"') == u
	assert sd_ujson.loads('"z\\ud834\\udd20x"') == u


def test_unicode_decode():
	for i in range(0, 0xd7ff):
		u = chr(i)
		s = '"\\u{0:04x}"'.format(i)
		assert sd_ujson.loads(s) == u


def test_unicode_preservation():
	assert type(sd_ujson.loads('""')) == str
	assert type(sd_ujson.loads('"a"')) == str
	assert type(sd_ujson.loads('["a"]')[0]) == str


@pytest.mark.xfail(reason="ujson encodes bytes to a string")
def test_bytes_encode():
	with pytest.raises(TypeError):
		sd_ujson.dumps(b"hi")
	with pytest.raises(TypeError):
		sd_ujson.dumps([b"hi"])


@pytest.mark.xfail
def test_bytes_decode():
	for encoding, bom in [
			('utf-8', codecs.BOM_UTF8),
			('utf-16be', codecs.BOM_UTF16_BE),
			('utf-16le', codecs.BOM_UTF16_LE),
			('utf-32be', codecs.BOM_UTF32_BE),
			('utf-32le', codecs.BOM_UTF32_LE),
			]:
		data = ["a\xb5\u20ac\U0001d120"]
		encoded = sd_ujson.dumps(data).encode(encoding)
		print(data, encoded)
		assert sd_ujson.loads(bom + encoded) == data
		assert sd_ujson.loads(encoded) == data
	with pytest.raises(UnicodeDecodeError):
		sd_ujson.loads(b'["\x80"]')
	# RFC-7159 and ECMA-404 extend JSON to allow documents that
	# consist of only a string, which can present a special case
	# not covered by the encoding detection patterns specified in
	# RFC-4627 for utf-16-le (XX 00 XX 00).
	assert sd_ujson.loads('"\u2600"'.encode('utf-16-le')) == '\u2600'
	# Encoding detection for small (<4) bytes objects
	# is implemented as a special case. RFC-7159 and ECMA-404
	# allow single codepoint JSON documents which are only two
	# bytes in utf-16 encodings w/o BOM.
	assert sd_ujson.loads(b'5\x00') == 5
	assert sd_ujson.loads(b'\x007') == 7
	assert sd_ujson.loads(b'57') == 57


@pytest.mark.xfail
def test_object_pairs_hook_with_unicode():
	s = '{"xkd":1, "kcw":2, "art":3, "hxm":4, "qrt":5, "pad":6, "hoy":7}'
	p = [
			("xkd", 1), ("kcw", 2), ("art", 3), ("hxm", 4),
			("qrt", 5), ("pad", 6), ("hoy", 7),
			]
	assert sd_ujson.loads(s) == eval(s)
	assert sd_ujson.loads(s, object_pairs_hook=lambda x: x) == p
	od = sd_ujson.loads(s, object_pairs_hook=OrderedDict)
	assert od == OrderedDict(p)
	assert type(od) == OrderedDict
	# the object_pairs_hook takes priority over the object_hook
	assert sd_ujson.loads(
			s, object_pairs_hook=OrderedDict,
			object_hook=lambda x: None
			) == OrderedDict(p)
