# 3rd party
import pytest  # type: ignore

# this package
import sdjson


class JSONTestObject:
	pass


def test_listrecursion():
	x = []
	x.append(x)
	try:
		sdjson.dumps(x)
	except ValueError:
		pass
	else:
		pytest.fail("didn't raise ValueError on list recursion")
	x = []
	y = [x]
	x.append(y)
	try:
		sdjson.dumps(x)
	except ValueError:
		pass
	else:
		pytest.fail("didn't raise ValueError on alternating list recursion")
	y = []
	x = [y, y]
	# ensure that the marker is cleared
	sdjson.dumps(x)


def test_dictrecursion():
	x = {}
	x["test"] = x
	try:
		sdjson.dumps(x)
	except ValueError:
		pass
	else:
		pytest.fail("didn't raise ValueError on dict recursion")
	x = {}
	y = {"a": x, "b": x}
	# ensure that the marker is cleared
	sdjson.dumps(x)


def test_defaultrecursion():

	class RecursiveJSONEncoder(sdjson.JSONEncoder):
		recurse = False

		def default(self, o):
			if o is JSONTestObject:
				if self.recurse:
					return [JSONTestObject]
				else:
					return 'JSONTestObject'
			return sdjson.JSONEncoder.default(o)

	enc = RecursiveJSONEncoder()
	assert enc.encode(JSONTestObject) == '"JSONTestObject"'
	enc.recurse = True
	try:
		enc.encode(JSONTestObject)
	except ValueError:
		pass
	else:
		pytest.fail("didn't raise ValueError on default recursion")


def test_highly_nested_objects_decoding():
	# test that loading highly-nested objects doesn't segfault when C
	# accelerations are used. See #12017
	with pytest.raises(RecursionError):
		sdjson.loads('{"a":' * 100000 + '1' + '}' * 100000)
	with pytest.raises(RecursionError):
		sdjson.loads('{"a":' * 100000 + '[1]' + '}' * 100000)
	with pytest.raises(RecursionError):
		sdjson.loads('[' * 100000 + '1' + ']' * 100000)


def test_highly_nested_objects_encoding():
	# See #12051
	l, d = [], {}
	for x in range(100000):
		l, d = [l], {'k': d}
	with pytest.raises(RecursionError):
		sdjson.dumps(l)
	with pytest.raises(RecursionError):
		sdjson.dumps(d)


def test_endless_recursion():
	# See #12051
	class EndlessJSONEncoder(sdjson.JSONEncoder):

		def default(self, o):
			"""If check_circular is False, this will keep adding another list."""
			return [o]

	with pytest.raises(RecursionError):
		EndlessJSONEncoder(check_circular=False).encode(5j)
