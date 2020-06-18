from decimal import Decimal
import sd_ujson


# Create a custom encoder for Decimal that turns it into a string
@sd_ujson.encoders.register(Decimal)
def encode_str(obj):
	return str(obj)
