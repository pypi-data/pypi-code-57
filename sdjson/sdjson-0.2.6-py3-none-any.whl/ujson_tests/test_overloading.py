# stdlib
from decimal import Decimal

# this package
import sd_ujson


def test_overloading():
	
	# Create and register a custom encoder
	@sd_ujson.encoders.register(Decimal)
	def encoder_1(obj):
		return "Result from first registration"
	
	# Test that we get the expected output from the first encoder
	assert sd_ujson.dumps(Decimal(1)) == '"Result from first registration"'
	
	# Create and register a new custom encoder that overloads the previous one
	@sd_ujson.encoders.register(Decimal)
	def encoder_2(obj):
		return "Result from second registration"
	
	# Test that we get the expected output from the second encoder
	assert sd_ujson.dumps(Decimal(2)) == '"Result from second registration"'
	
	print(sd_ujson.encoders.registry.items())
	
	# Cleanup
	sd_ujson.encoders.unregister(Decimal)
