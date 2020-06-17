from .AudioObj import AudioObj
from .AudioEnumIndex import AudioEnumIndex;
class AudioList(list):
	def __init__(self,vk,*params):
		self.vk=vk;
		super().__init__(*params)
	def __str__(self):
		return str(self.toJsonArray())
	def toJsonArray(self):
		ans=[]
		for i in self:
			ans.append(i.toArray())
		return ans
	def reorder(self,from_index:int=None,to_index:int=None):
		self.insert(to_index, self.pop(from_index)) 
		before_index_id=to_index
		if(before_index_id!=0):
			before_index_id=self[before_index_id-1];
		return self[to_index].reorder(before_index_id)

