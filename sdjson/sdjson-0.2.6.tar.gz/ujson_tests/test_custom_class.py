"""
Test custom encoder for a custom class
"""

# stdlib
import pathlib
from tempfile import TemporaryDirectory

# this package
import sd_ujson
from .utils import nospace


class CustomClassBase:
	def __str__(self):
		return self.__repr__()
	
	def __iter__(self):
		for key, value in self.__dict__().items():
			yield key, value
	
	def __getstate__(self):
		return self.__dict__()
	
	def __setstate__(self, state):
		self.__init__(**state)
	
	def __copy__(self):
		return self.__class__(**self.__dict__())
	
	def __deepcopy__(self, memodict={}):
		return self.__copy__()


class Character(CustomClassBase):
	def __init__(self, name, actor, armed=False):
		self.name = str(name)
		self.actor = str(actor)
		self.armed = bool(armed)
	
	def __repr__(self):
		return f"Character: {self.name} ({self.actor})"
	
	def __dict__(self):
		return dict(name=self.name, actor=self.actor, armed=self.armed)


class Cheese(CustomClassBase):
	def __init__(self, name, properties=None):
		self.name = name
		
		if properties:
			self.properties = properties
		else:
			self.properties = []
	
	def __repr__(self):
		return f"Cheese({self.name})"
	
	def __dict__(self):
		return dict(
				name=self.name,
				properties=self.properties,
				)


class Shop(CustomClassBase):
	"""
	Custom class to encode to JSON
	"""
	
	def __init__(
			self, name, address, open=True, staff=None, customers=None, current_stock=None, music=False, dancing=False,
			):
		
		self.name = str(name)
		self.address = str(address)
		self.open = bool(open)
		self.music = bool(music)
		self.dancing = bool(dancing)
		
		if staff:
			self.staff = staff
		else:
			self.staff = []
		
		if customers:
			self.customers = customers
		else:
			self.customers = []
		
		if current_stock:
			self.current_stock = current_stock
		else:
			self.current_stock = []
	
	def __repr__(self):
		return f"{self.name} ({'Open' if self.open else 'closed'})"
	
	def __dict__(self):
		return dict(
				name=self.name,
				address=self.address,
				open=self.open,
				music=self.music,
				dancing=self.dancing,
				staff=self.staff,
				customers=self.customers,
				current_stock=self.current_stock,
				)


def test_custom_class():
	# Create and register the custom encoders
	# In this example we create three separate encoders even though all three classes
	#  actually share a common subclass. In real usage they might not be.
	@sd_ujson.encoders.register(Character)
	def encode_character(obj):
		return dict(obj)
	
	@sd_ujson.encoders.register(Cheese)
	def encode_cheese(obj):
		return dict(obj)
	
	@sd_ujson.encoders.register(Shop)
	def encode_shop(obj):
		return dict(obj)
	
	# Create instances of classes
	runny_camembert = Cheese("Camembert", ["Very runny"])
	shopkeeper = Character("Mr Wensleydale", "Michael Palin")
	customer = Character("The Customer", "John Cleese")
	cheese_shop = Shop(
			"The National Cheese Emporium",
			address="""12 Some Street
Some Town
England""",
			staff=[shopkeeper],
			customers=[customer],
			current_stock=[runny_camembert],
			music=False,
			dancing=False,
			)
	
	expected_json = (
			'{"name": "The National Cheese Emporium", "address": "12 Some Street\\n'
			'Some Town\\nEngland", "open": true, "music": false, "dancing": false, '
			'"staff": [{"name": "Mr Wensleydale", "actor": "Michael Palin", "armed": false}], '
			'"customers": [{"name": "The Customer", "actor": "John Cleese", "armed": false}], '
			'"current_stock": [{"name": "Camembert", "properties": ["Very runny"]}]}'
			)
	
	with TemporaryDirectory() as tmpdir:
		tmpfile = pathlib.Path(tmpdir) / "output.json"
		
		with open(tmpfile, "w") as fp:
			sd_ujson.dump(cheese_shop, fp)
		
		with open(tmpfile, "r") as fp:
			assert fp.read() == nospace(expected_json)
		
	assert sd_ujson.dumps(cheese_shop) == nospace(expected_json)
		
	# Cleanup
	sd_ujson.unregister_encoder(Character)
	sd_ujson.unregister_encoder(Cheese)
	sd_ujson.unregister_encoder(Shop)
