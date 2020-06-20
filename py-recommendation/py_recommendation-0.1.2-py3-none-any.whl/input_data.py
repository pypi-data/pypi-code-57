from py_recommendation.error import RecoError
from py_recommendation.data import ItemData, UserData
from py_recommendation.utils import Utils

import pandas as pd
import numpy as np
import sys

class InputData(Utils):
	"""docstring for InputData"""
	def __init__(self):
		pass

	@staticmethod
	def format_df(df, req_col):
		df.replace(np.nan, '', regex=True, inplace=True)
		return df[req_col]

	def getData_file(self, filePath, itemName_col, itemDesc_col="", itemTag_col="", itemTag_sep = ",", fileType='xlsx'):
		req_col = [itemName_col]
		if itemDesc_col:
			req_col.append(itemDesc_col)
		if itemTag_col:
			req_col.append(itemTag_col)

		try:
			if fileType == 'xlsx':
				df = pd.read_excel(filePath)
			elif fileType == 'csv':
				df = pd.read_csv(filePath)
			else:
				err =  RecoError('Wrong file type given: [{}] supported:["xlsx", "csv"]'.format(fileType))
				raise err

			df = self.format_df(df = df, req_col = req_col)

			if itemTag_col and itemDesc_col:
				itemData = ItemData( itemName_list = df[itemName_col].tolist(), 
									itemTags_list = df[itemTag_col].tolist(), 
									itemDesc_list = df[itemDesc_col].tolist() )
			elif itemTag_col:
				itemData = ItemData( itemName_list = df[itemName_col].tolist(), 
									itemTags_list = self.cleanText(df[itemTag_col].tolist()) )
			elif itemDesc_col:
				itemData = ItemData(itemName_list = df[itemName_col].tolist(), 
									itemDesc_list = self.cleanText(text_list = df[itemDesc_col].tolist()) )
			else:
				err =  RecoError('Mandatory fields are not present please check the columns used [{}] for the given file [{}] '.format(df.columns, filePath))
				raise err

			return itemData

		except Exception as e:
			err = RecoError('Error occured while loading the data ' + sys._getframe(1).f_code.co_name + ' ' + str(e))
			raise err
