import json
from jinja2 import Template
from dnac.maglev.security.SecurityManager import SecurityManager

class CalibrationModel:
	def __init__(self, name, id = 0, status = 2 ):
		self._name_ = name
		self._id_ = id
		self._status_ = status

	@property
	def name(self):
		return self._name_
	
	@property
	def id(self):
		return self._id_

	@property
	def status(self):
		return self._status_
	
	# Parse the entity Json returned by DNAC and recreate the object
	#
	@classmethod
	def parseJson(cls, cbjsonstr):
		cbs = json.loads(cbjsonstr)
		if isinstance(cbs, list):
			return [ cls(cb['name'], cb['id'], cb['status']) for cb in cbs]

		return cls(cbs['name'], cbs['id'], cbs['status']) if isinstance(cbs, dict) else None

	def _eq_(self, other):
		return self.id == other.id

	# Print out the object
	def _str_(self):
		return '<Id = ' + str(self.id) + ' , Name = ' + self.name + '>'

#
if __name__ == "__main__":
	cbjson = '''
			[
			{"id":74075,"name":"Drywall Office Only","status":2},
			{"id":74077,"name":"Indoor High Ceiling","status":2},
			{"id":74074,"name":"Cubes And Walled Offices","status":2},
			{"id":74076,"name":"Outdoor Open Space","status":2}
			]
		'''

	cbm = '{"id":74075,"name":"Drywall Office Only","status":2}'
	model1 = CalibrationModel.parseJson(cbm)
	print('Model 1')
	print(type(model1))
	print(str(model1))

	model2 = CalibrationModel.parseJson(cbjson)
	print('Model 2')
	print(type(model2))
	for i in model2:
		print(str(i))
