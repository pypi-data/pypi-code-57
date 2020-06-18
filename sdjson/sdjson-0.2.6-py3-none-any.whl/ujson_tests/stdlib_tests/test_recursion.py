# 3rd party
import pytest

# this package
import sd_ujson


class JSONTestObject:
	pass


def test_listrecursion():
	x = []
	x.append(x)
	try:
		sd_ujson.dumps(x)
	except (ValueError, OverflowError):
		pass
	else:
		pytest.fail("didn't raise ValueError or OverflowError on list recursion")
	x = []
	y = [x]
	x.append(y)
	try:
		sd_ujson.dumps(x)
	except (ValueError, OverflowError):
		pass
	else:
		pytest.fail("didn't raise ValueError or OverflowError on list recursion")
	y = []
	x = [y, y]
	# ensure that the marker is cleared
	sd_ujson.dumps(x)


def test_dictrecursion():
	x = {}
	x["test"] = x
	try:
		sd_ujson.dumps(x)
	except (ValueError, OverflowError):
		pass
	else:
		pytest.fail("didn't raise ValueError or OverflowError on dict recursion")
	x = {}
	y = {"a": x, "b": x}
	# ensure that the marker is cleared
	sd_ujson.dumps(x)


def test_highly_nested_objects_decoding():
	# test that loading highly-nested objects doesn't segfault when C
	# accelerations are used. See #12017
	with pytest.raises((RecursionError, ValueError)):
		sd_ujson.loads('{"a":' * 100000 + '1' + '}' * 100000)
	with pytest.raises((RecursionError, ValueError)):
		sd_ujson.loads('{"a":' * 100000 + '[1]' + '}' * 100000)
	with pytest.raises((RecursionError, ValueError)):
		sd_ujson.loads('[' * 100000 + '1' + ']' * 100000)


def test_highly_nested_objects_encoding():
	# See #12051
	l, d = [], {}
	for x in range(100000):
		l, d = [l], {'k': d}
	with pytest.raises((RecursionError, OverflowError)):
		sd_ujson.dumps(l)
	with pytest.raises((RecursionError, OverflowError)):
		sd_ujson.dumps(d)


def test_endless_recursion():
	# See #12051
	def hook(o):
		"""With ujson this will keep adding another list."""
		return [o]
	
	with pytest.raises((RecursionError, OverflowError)):
		sd_ujson.dumps(5j, pre_encode_hook=hook)
