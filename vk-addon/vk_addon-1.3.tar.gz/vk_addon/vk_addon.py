import vk_api

class VkAddonError(Exception):
	def __init__(self, text):
		self.text = text

class VkAddon:
	def __init__(self, event=None, member_id=None, on=True):
		self.event = event
		self.member_id = member_id

	def connect(self):
		if self.event == None or self.member_id == None:
			raise VkAddonError('Не указан "event" или "member_id"')

		else:
			pass

	def type(self):
		try:
			if self.member_id > 0:
				if self.event['object']['action']['type'] == 'chat_invite_user':
					return 'chat_invite_user'

				elif self.event['object']['action']['type'] == 'chat_kick_user':
					return 'chat_kick_user'

				else:
					return None

		except KeyError:
			if self.event['type'] == 'message_new':				
				return 'message_new'

			elif self.event['type'] == 'message_typing_state':
				return 'message_typing_state'


	def member(self):
		return self.event['object']['from_id']



