

class ItemData(object):
	"""docstring for ItemData"""
	def __init__(self, itemName_list, itemTags_list=[], itemDesc_list=[]):
		self.itemNames = itemName_list
		self.itemTags = itemTags_list
		self.itemDescs = itemDesc_list


class UserData(object):
	"""docstring for UserData"""
	def __init__(self, userId, triedItemData):
		self.userId = userId
		self.triedItemData = triedItemData
		
		
