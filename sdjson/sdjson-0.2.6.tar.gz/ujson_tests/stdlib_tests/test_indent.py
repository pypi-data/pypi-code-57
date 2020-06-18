# stdlib
import textwrap
from io import StringIO

# this package
import sd_ujson
import pytest
from ..utils import nospace


def test_indent():
	h = [
			['blorpie'], ['whoops'], [],
			'd-shtaeou', 'd-nthiouh', 'i-vhbjkhnth',
			{'nifty': 87}, {'field': 'yes', 'morefield': False}
			]
	
	expect = textwrap.dedent("""\
	[
	\t[
	\t\t"blorpie"
	\t],
	\t[
	\t\t"whoops"
	\t],
	\t[],
	\t"d-shtaeou",
	\t"d-nthiouh",
	\t"i-vhbjkhnth",
	\t{
	\t\t"nifty": 87
	\t},
	\t{
	\t\t"field": "yes",
	\t\t"morefield": false
	\t}
	]""")
	
	d1 = sd_ujson.dumps(h)
	h1 = sd_ujson.loads(d1)
	assert h1 == h

	with pytest.raises(TypeError):  # separators is not supported by ujson
		d2 = sd_ujson.dumps(h, indent=2, sort_keys=True, separators=(',', ': '))
		h2 = sd_ujson.loads(d2)
		assert h2 == h
		assert d2 == expect.expandtabs(2)

	with pytest.raises(TypeError):  # separators is not supported by ujson
		d3 = sd_ujson.dumps(h, indent='\t', sort_keys=True, separators=(',', ': '))
		h3 = sd_ujson.loads(d3)
		assert h3 == h
		assert d3 == expect
	
	d4 = sd_ujson.dumps(h, indent=2, sort_keys=True)
	# TODO: assert d4 == d2

	d5 = sd_ujson.dumps(h, indent='\t', sort_keys=True)
	# TODO: assert d5 == d3


def test_indent0():
	h = {3: 1}
	
	def check(indent, expected):
		d1 = sd_ujson.dumps(h, indent=indent)
		assert d1 == nospace(expected)
		
		sio = StringIO()
		sd_ujson.dump(h, sio, indent=indent)
		assert sio.getvalue() == nospace(expected)
	
	# indent=0 should emit newlines
	# FIXME: ujson indent=0 doesn't emit newlines
	# check(0, '{\n"3": 1\n}')
	check(0, '{"3": 1}')
	# indent=None is more compact
	check(None, '{"3": 1}')
