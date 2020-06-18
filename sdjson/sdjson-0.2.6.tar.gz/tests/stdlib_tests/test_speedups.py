# stdlib
# These tests test the internals of json, so we really do
#  mean to be importing json here
# stdlib
import json
import platform

# 3rd party
import pytest  # type: ignore


class BadBool:

	def __bool__(self):
		1 / 0


@pytest.mark.skipif(platform.python_implementation() == "PyPy", reason="Unsupported on PyPy")
def test_scanstring():
	assert json.decoder.scanstring.__module__ == "_json"
	assert json.decoder.scanstring is json.decoder.c_scanstring


@pytest.mark.skipif(platform.python_implementation() == "PyPy", reason="Unsupported on PyPy")
def test_encode_basestring_ascii():
	assert json.encoder.encode_basestring_ascii.__module__ == "_json"
	assert json.encoder.encode_basestring_ascii is json.encoder.c_encode_basestring_ascii


@pytest.mark.skipif(platform.python_implementation() == "PyPy", reason="Unsupported on PyPy")
def test_make_scanner():
	with pytest.raises(AttributeError):
		json.scanner.c_make_scanner(1)


@pytest.mark.skipif(platform.python_implementation() == "PyPy", reason="Unsupported on PyPy")
def test_bad_bool_args_1():

	def test(value):
		json.decoder.JSONDecoder(strict=BadBool()).decode(value)

	with pytest.raises(ZeroDivisionError):
		test('""')
	with pytest.raises(ZeroDivisionError):
		test('{}')


@pytest.mark.skipif(platform.python_implementation() == "PyPy", reason="Unsupported on PyPy")
def test_make_encoder():
	# bpo-6986: The interpreter shouldn't crash in case c_make_encoder()
	# receives invalid arguments.
	with pytest.raises(TypeError):
		json.encoder.c_make_encoder(
				(True, False),
				b"\xCD\x7D\x3D\x4E\x12\x4C\xF9\x79\xD7\x52\xBA\x82\xF2\x27\x4A\x7D\xA0\xCA\x75",
				None,
				)


@pytest.mark.skipif(platform.python_implementation() == "PyPy", reason="Unsupported on PyPy")
def test_bad_str_encoder():
	# Issue #31505: There shouldn't be an assertion failure in case
	# c_make_encoder() receives a bad encoder() argument.
	def bad_encoder1(*args):
		return None

	enc = json.encoder.c_make_encoder(
			None, lambda obj: str(obj), bad_encoder1, None, ': ', ', ', False, False, False
			)

	with pytest.raises(TypeError):
		enc('spam', 4)
	with pytest.raises(TypeError):
		enc({'spam': 42}, 4)

	def bad_encoder2(*args):
		1 / 0

	enc = json.encoder.c_make_encoder(
			None, lambda obj: str(obj), bad_encoder2, None, ': ', ', ', False, False, False
			)

	with pytest.raises(ZeroDivisionError):
		enc('spam', 4)


@pytest.mark.skipif(platform.python_implementation() == "PyPy", reason="Unsupported on PyPy")
def test_bad_bool_args_2():

	def test(name):
		json.encoder.JSONEncoder(**{name: BadBool()}).encode({'a': 1})

	with pytest.raises(ZeroDivisionError):
		test('skipkeys')
	with pytest.raises(ZeroDivisionError):
		test('ensure_ascii')
	with pytest.raises(ZeroDivisionError):
		test('check_circular')
	with pytest.raises(ZeroDivisionError):
		test('allow_nan')
	with pytest.raises(ZeroDivisionError):
		test('sort_keys')


def test_unsortable_keys():
	with pytest.raises(TypeError):
		json.encoder.JSONEncoder(sort_keys=True).encode({'a': 1, 1: 'a'})
