# this package
import sdjson


def test_default():
	assert sdjson.dumps(type, default=repr) == sdjson.dumps(repr(type))
