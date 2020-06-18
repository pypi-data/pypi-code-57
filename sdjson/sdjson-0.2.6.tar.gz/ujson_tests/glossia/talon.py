from fractions import Fraction
import sd_ujson


# Create a custom encoder for Fraction that turns it into a string
@sd_ujson.encoders.register(Fraction)
def encode_str(obj):
	return str(obj)
