"""
Test registering custom encoders in multiple files
"""

# stdlib
from decimal import Decimal
from fractions import Fraction

# this package
import sd_ujson


def test_multiple_files():
	from .glossia import thorn
	from .glossia import talon
	
	# Test that we get the expected output when encoding a Decimal
	assert sd_ujson.dumps(Decimal(1)) == '"1"'
	
	# Test that we get the expected output when encoding a Fraction
	assert sd_ujson.dumps(Fraction(2, 3)) == '"2/3"'
	
	# Cleanup
	sd_ujson.encoders.unregister(Decimal)
	sd_ujson.encoders.unregister(Fraction)
