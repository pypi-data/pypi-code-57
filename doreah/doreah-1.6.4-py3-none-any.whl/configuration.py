from ._internal import DEFAULT, defaultarguments, DoreahConfig


config = DoreahConfig("configuration",
)

class Configuration:
	def __init__(self,settings):
		self.defaults = {k:settings[k][1] for k in settings}
		self.types = {k:settings[k][0] for k in settings}
		self.expire = {k:settings[k][2] for k in settings}
