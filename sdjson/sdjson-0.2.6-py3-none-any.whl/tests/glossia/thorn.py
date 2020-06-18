# stdlib
from decimal import Decimal

# this package
import sdjson


# Create a custom encoder for Decimal that turns it into a string
@sdjson.encoders.register(Decimal)
def encode_str(obj):
	return str(obj)
