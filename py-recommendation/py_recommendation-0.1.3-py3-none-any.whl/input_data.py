from py_recommendation.error import RecoError
from py_recommendation.data import Item, Users
from py_recommendation.utils import Utils

import pandas as pd
import numpy as np
import sys

class ItemData(Utils):
	"""docstring for ItemData"""
	def __init__(self):
		pass

	@staticmethod
	def format_df(df, req_col):
		df.replace(np.nan, '', regex=True, inplace=True)
		return df[req_col]

	def setItemData(self, df, itemNameField, itemTagField, itemDescField):
		if itemTagField and itemDescField:
			itemData = Item( itemName_list = df[itemNameField].tolist(), 
								itemTags_list = df[itemTagField].tolist(), 
								itemDesc_list = df[itemDescField].tolist() )
		elif itemTagField:
			itemData = Item( itemName_list = df[itemNameField].tolist(), 
								itemTags_list = self.cleanText(df[itemTagField].tolist()) )
		elif itemDescField:
			itemData = Item(itemName_list = df[itemNameField].tolist(), 
								itemDesc_list = self.cleanText(text_list = df[itemDescField].tolist()) )
		else:
			err =  RecoError('Mandatory fields are not present please check the fields used [{}] '.format(df.columns))
			raise err

		return itemData

	def setData(self, data, itemNameField, itemDescField="", itemTagField=""):
		req_col = [itemNameField]
		if itemDescField:
			req_col.append(itemDescField)
		if itemTagField:
			req_col.append(itemTagField)

		try:	
			if isinstance(data, dict):
				df = pd.DataFrame(data)
			elif isinstance(data, list):
				df = pd.DataFrame(data)
			elif isinstance(data, pd.DataFrame):
				df = data

			if not (itemNameField in df.columns and (itemDescField in df.columns or itemTagField in df.columns)):
				err =  RecoError('Required fields not found in given data fields [{}] '.format(df.columns))
				raise err

			df = self.format_df(df = df, req_col = req_col)

			return self.setItemData(df= df, itemNameField=itemNameField, itemTagField=itemTagField, itemDescField=itemDescField)

		except Exception as e:
			err = RecoError('Error occured while loading the items data ' + sys._getframe(1).f_code.co_name + ' ' + str(e))
			raise err
			

	def setData_file(self, filePath, itemNameField, itemDescField="", itemTagField="", itemTag_sep = ",", fileType='xlsx'):
		req_col = [itemNameField]
		if itemDescField:
			req_col.append(itemDescField)
		if itemTagField:
			req_col.append(itemTagField)

		try:
			if fileType == 'xlsx':
				df = pd.read_excel(filePath)
			elif fileType == 'csv':
				df = pd.read_csv(filePath)
			else:
				err =  RecoError('Wrong file type given: [{}] supported:["xlsx", "csv"]'.format(fileType))
				raise err

			df = self.format_df(df = df, req_col = req_col)

			return self.setItemData(df= df, itemNameField=itemNameField, itemTagField=itemTagField, itemDescField=itemDescField)
			

		except Exception as e:
			err = RecoError('Error occured while loading the data ' + sys._getframe(1).f_code.co_name + ' ' + str(e))
			raise err

class UsersData():
	"""docstring for UsersData"""
	def __init__(self):
		pass

	@staticmethod
	def format_df(df, req_col, fillna_dict={}):
		for eachCol, fillNa_val in fillna_dict.items():
			df[[eachCol]] = df[[eachCol]].fillna(value=fillNa_val)
		return df[req_col]

	@staticmethod
	def setUserData(df, userName_col, triedItem_col):
		userData = Users(userIds_list = df[userName_col].tolist(), 
								triedItems_list = df[triedItem_col].tolist() )
		return userData

	def setData(self, data, userNameField, triedItemField):
		if isinstance(data, dict):
			df = pd.DataFrame(data)
		elif isinstance(data, list):
			df = pd.DataFrame(data)
		elif isinstance(data, pd.DataFrame):
			df = data

		if not (userNameField in df.columns and triedItemField in df.columns):
			err =  RecoError('Name field and item field [{}] not found in given data fields [{}] '.format((userNameField, triedItemField, ), df.columns))
			raise err


		req_col = [userNameField, triedItemField]
		df = self.format_df(df = df, req_col = req_col)

		return self.setUserData(df= df, userName_col=userNameField, triedItem_col=triedItemField)
		
