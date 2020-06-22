import re

class StringBuilder():
	def __init__(self, template):
		self.template = template
		self.params = {}

	def build(self):
		tags = re.findall('%\\((.*?)\\)', self.template)
		template_tags = [(tag, self.params.get(tag, 'None')) for tag in tags]

		transformed = self.template
		for tag, value in template_tags:
			transformed = re.sub('%\\((' + tag +')\\)', str(value), transformed)

		return transformed

	def set(self, key, value):
		self.params[key] = value