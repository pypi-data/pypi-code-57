# stdlib
import math

# 3rd party
import pytest

# this package
import sd_ujson


def test_floats():
	for num in [1617161771.7650001, math.pi, math.pi ** 100, math.pi ** -100, 3.1]:
		assert float(sd_ujson.dumps(num)) == num
		assert sd_ujson.loads(sd_ujson.dumps(num)) == num


def test_ints():
	for num in [1, 1 << 32]:
		assert sd_ujson.dumps(num) == str(num)
		assert int(sd_ujson.dumps(num)) == num
	
	with pytest.raises(OverflowError):
		num = 1 << 64
		assert sd_ujson.dumps(num) == str(num)
		assert int(sd_ujson.dumps(num)) == num


def test_out_of_range():
	assert sd_ujson.loads('[23456789012E666]') == [float('inf')]
	assert sd_ujson.loads('[-23456789012E666]') == [float('-inf')]



@pytest.mark.xfail(reason="Not working as expected")
def test_allow_nan():
	for val in (float('inf'), float('-inf'), float('nan')):
		out = sd_ujson.dumps([val])
		if val == val:  # inf
			assert sd_ujson.loads(out) == [val]
		else:  # nan
			res = sd_ujson.loads(out)
			assert len(res) == 1
			assert res[0] != res[0]
		with pytest.raises(ValueError):
			sd_ujson.dumps([val], allow_nan=False)
