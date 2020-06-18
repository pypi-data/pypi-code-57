"""
Test dumping and loading some objects
"""

# stdlib
import pathlib
from tempfile import TemporaryDirectory

# 3rd party
import pytest

# this package
import sd_ujson


def write_then_read(obj):
	with TemporaryDirectory() as tmpdir:
		tmpfile = pathlib.Path(tmpdir) / "output.json"
	
		with open(tmpfile, "w") as fp:
			sd_ujson.dump(obj, fp)
		
		with open(tmpfile, "r") as fp:
			return sd_ujson.load(fp)
	

def test_bools():
	assert write_then_read(True) is True
	assert str(write_then_read(True)) == "True"  # Double check with string
	
	assert write_then_read(False) is False
	assert str(write_then_read(False)) == "False"  # Double check with string
	

def test_none():
	assert write_then_read(None) is None
	assert str(write_then_read(None)) == "None"  # Double check with string
	
	
def test_int():
	assert write_then_read(1) == 1
	assert write_then_read(1234) == 1234
	assert write_then_read(12340000000) == 12340000000
	assert write_then_read(-1) == -1
	assert write_then_read(-1234) == -1234
	assert write_then_read(-12340000000) == -12340000000
	
	
def test_float():
	assert write_then_read(1.0) == 1.0
	assert write_then_read(1234.0) == 1234.0
	assert write_then_read(12340000000.0) == 12340000000.0
	assert write_then_read(-1.0) == -1.0
	assert write_then_read(-1234.0) == -1234.0
	assert write_then_read(-12340000000.0) == -12340000000.0
	
	assert write_then_read(1.005) == 1.005
	assert write_then_read(1234.005) == 1234.005
	assert write_then_read(12340000000.005) == 12340000000.005
	assert write_then_read(-1.005) == -1.005
	assert write_then_read(-1234.005) == -1234.005
	assert write_then_read(-12340000000.005) == -12340000000.005
	
	
def test_string():
	for string in ["egg and bacon", "egg sausage and bacon", "egg and spam", "egg bacon and spam"]:
		print(string)
		assert write_then_read(string) == string
		

@pytest.mark.xfail
def test_dict_failure():
	"""
	This test will fail because the boolean dictionary keys get read back in a lowercase strings
	"""
	
	assert write_then_read({True: False, False: True}) == {True: False, False: True}
	assert write_then_read({2: 3.0, 4.0: 5, False: 1, 6: True}) == {2: 3.0, 4.0: 5, False: 1, 6: True}


def test_dict():
	assert write_then_read({"True": True, "False": False, "String": "spam", "Integer": 1, "Float": 2.5}) == \
		   {"True": True, "False": False, "String": "spam", "Integer": 1, "Float": 2.5}


def test_list():
	assert write_then_read([True, False, 1, 2.5, "spam"]) == [True, False, 1, 2.5, "spam"]


@pytest.mark.xfail
def test_tuple_failure():
	"""
	This test will fail because the tuple gets loaded back in as a list
	"""
	
	assert write_then_read((True, False, 1, 2.5, "spam")) == (True, False, 1, 2.5, "spam")
	
	
def test_tuple_success():
	assert write_then_read((True, False, 1, 2.5, "spam")) == [True, False, 1, 2.5, "spam"]
