# stdlib
from decimal import Decimal

# 3rd party
import pytest

# this package
import sd_ujson


def test_unregister():
	# By default ujson returns a str(float(obj)) representation it seems
	assert sd_ujson.dumps(Decimal(1)) == "1.0"
	assert isinstance(sd_ujson.dumps(Decimal(1)), str)
	
	# Create and register a custom encoder for Decimal that turns it into a string
	@sd_ujson.encoders.register(Decimal)
	def encode_str(obj):
		return str(obj)
	
	# Test that we get the expected output from the first encoder
	assert sd_ujson.dumps(Decimal(1)) == '"1"'
	assert isinstance(sd_ujson.dumps(Decimal(1)), str)
	
	# Unregister that encoder
	sd_ujson.unregister_encoder(Decimal)
	
	# We should now get a float again
	assert sd_ujson.dumps(Decimal(2)) == "2.0"
	assert isinstance(sd_ujson.dumps(Decimal(2)), str)
