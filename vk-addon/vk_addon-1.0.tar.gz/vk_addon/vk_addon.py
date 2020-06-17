class VkAddon(Exception):
	def __init__(self, token=None, group_id=None, on=True):
		self.token = token
		self.group_id = group_id
		self.on = on

	def connect(self, working):
		if self.token == None or self.group_id == None:
			raise TypeError('Error connecting, token or group id incorrectly specified')

		else:
			if self.on == True:
				if working == 'dkjfLJjkdf013':
					pass

				else:
					raise VkAddon('Мда, и нахуя?') 

			elif self.on == False:
				raise VkAddon('Error connecting, bot not on')

			else:
				raise TypeError(f"Error connecting, 'on={self.on}' is not. Specify True or False")