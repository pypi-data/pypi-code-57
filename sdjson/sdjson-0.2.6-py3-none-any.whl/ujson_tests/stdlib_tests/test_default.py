# this package
import sd_ujson


def test_default():
	assert sd_ujson.dumps(type, default=repr) == sd_ujson.dumps(repr(type))
