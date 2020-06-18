# stdlib
import platform
from io import StringIO

# 3rd party
import pytest

# this package
import sd_ujson


def test_dump():
	sio = StringIO()
	sd_ujson.json.dump({}, sio)
	assert sio.getvalue() == '{}'


def test_dumps():
	assert sd_ujson.dumps({}) == '{}'


def test_dump_skipkeys():
	v = {b'invalid_key': False, 'valid_key': True}
	with pytest.raises(TypeError):
		sd_ujson.json.dumps(v)
	
	s = sd_ujson.json.dumps(v, skipkeys=True)
	o = sd_ujson.json.loads(s)
	assert 'valid_key' in o
	assert b'invalid_key' not in o


@pytest.mark.xfail
def test_encode_truefalse():
	assert sd_ujson.dumps(
			{True: False, False: True}, sort_keys=True) == (
				'{"false": true, "true": false}')
	assert sd_ujson.dumps(
			{2: 3.0, 4.0: 5, False: 1, 6: True}, sort_keys=True) == (
				'{"false": 1, "2": 3.0, "4.0": 5, "6": true}')


@pytest.mark.xfail
# Issue 16228: Crash on encoding resized list
def test_encode_mutated():
	a = [object()] * 10
	
	def crasher(obj):
		del a[-1]
	
	assert sd_ujson.dumps(a, default=crasher) == '[null, null, null, null, null]'
