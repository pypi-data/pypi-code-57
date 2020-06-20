from py_recommendation.item_profile import ItemProfile
from py_recommendation.error import RecoError

import sys, json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from heapq import nlargest


def getTopReco(scoreNarray, n, removeIndexList):
	np.put(scoreNarray, removeIndexList, [-1])
	indices = np.argpartition(scoreNarray, -n)[-n:]
	indices = indices[np.argsort(-scoreNarray[indices])]
	scores = scoreNarray[indices]
	return list(zip(indices, scores))

class SimilarItem(ItemProfile):
	"""docstring for SimilarItem"""
	def __init__(self, itemData):
		super().__init__(itemData)
		self.similarityMatrix()

	def similarityMatrix(self):
		self.__simMat_itemItem = cosine_similarity(self.itemProfile, self.itemProfile)
		
	def similarItem(self, subItem, recoCount = 5):
		try:
			itemIndex = self.itemData.itemNames.index(subItem)
		except Exception as e:
			err = RecoError('Given item not found in input data items raised the error ' + sys._getframe(1).f_code.co_name + ' ' + str(e))
			raise err

		try:
			scoreList = self.__simMat_itemItem[itemIndex]

			recoIndex_tup = getTopReco(scoreNarray=scoreList, n=recoCount, removeIndexList=[itemIndex])

			return json.dumps([{
									"item":self.itemData.itemNames[each_reco[0]],
									"score":each_reco[1]*100
								} 
											for each_reco in recoIndex_tup])

		except Exception as e:
			err = RecoError('Error occured calculating similar item recommendation] ' + sys._getframe(1).f_code.co_name + ' ' + str(e))
			raise err


