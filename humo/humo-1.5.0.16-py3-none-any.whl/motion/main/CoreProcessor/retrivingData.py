import os
import sys
import numpy as np
import pandas as pd
from scipy.interpolate import splev, splrep
from scipy import signal
from scipy import fftpack
import functools
import json



cwd = os.getcwd()
filepath = os.path.dirname(os.path.abspath(__file__))
os.chdir(filepath)
os.chdir("./Error_msg")
with open('Error_msg_list.json', 'r') as f:
	Error_msg = json.load(f)
os.chdir(cwd)

"""
retrivingData
"""

def retrivingMarkerData(adjustframes):
	def retrivingData_(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			ColNumber = func(*args, **kwargs)
			if adjustframes == True:
				if type(ColNumber) == list:
					data = []
					for i in ColNumber:
						data.append(args[0]._marker.iloc[1:-1,i:i+3].values)
					try:
						f = args[0].fadjust
						data_ = []
						for i in data:
							data_.append(i[f:,:])
						return np.array(data_)
						#array = HumoArray(np.array(data_), args[1])
						#for name, d in zip(args[1],np.array(data)):
						#	setattr(array, name, HumoArray(d))
						#return array
					except AttributeError:
						#array = HumoArray(np.array(data), args[1])
						#for name, d in zip(args[1], np.array(data)):
						#	setattr(array, name, HumoArray(d))
						#return array
						return np.array(data)
				else:
					data =  args[0]._marker.iloc[1:-1,ColNumber:ColNumber+3].values
					try:
						f = args[0].fadjust
						return data
						#return HumoArray(data[f:,:], args[1])
					except AttributeError:
						return data
						#return HumoArray(data,args[1])
				#if np.isnan(data).any():
				#	print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
				#	sys.exit("NaN value error.")
				#else:
				#	return data
			elif adjustframes == False:
				if type(ColNumber) == list:
					data = []
					for i in ColNumber:
						data.append(args[0]._marker.iloc[:,i:i+3].values)
					try:
						f = args[0].fadjust
						data_ = []
						for i in data:
							data_.append(i[f:,:])
						return np.array(data_)
						#array = HumoArray(np.array(data_), args[1])
						#for name, d in zip(args[1], np.array(data_)):
						#	setattr(array, name, np.array(d))
						#return array
					except AttributeError:
						return np.array(data)
						#array = HumoArray(np.array(data), args[1])
						#for name, d in zip(args[1], np.array(data)):
						#	setattr(array, name, np.array(d))
						#return array
				else:
					data = args[0]._marker.iloc[:,ColNumber:ColNumber+3].values
					try:
						f = args[0].fadjust
						data_ = []
						for i in data:
							data_.append(i[f:,:])
						return data_
						#return HumoArray(data_, args[1])
					except AttributeError:
						return data
						#return HumoArray(data, args[1])
				#if np.isnan(data).any():
				#	print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
				#	sys.exit("NaN value error.")
		return wrapper
	return retrivingData_


def retrivingModelData(adjustframes):
	def retrivingData_(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			ColNumber = func(*args, **kwargs)
			if adjustframes == True:
				if type(ColNumber) == list:
					data = []
					for i in ColNumber:
						data.append(args[0]._model.iloc[1:-1,i:i+3].values)
					try:
						f = args[0].fadjust
						data_ = []
						for i in data:
							data_.append(i[f:,:])
						return np.array(data_)
					except AttributeError:
						return np.array(data)
				else:
					data =  args[0]._model.iloc[1:-1,ColNumber:ColNumber+3].values
					try:
						f = args[0].fadjust
						return np.array(data[f:,:])
					except AttributeError:
						return np.array(data)
					#if np.isnan(data).any():
					#	print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
					#	sys.exit("NaN value error.")
					#else:
					#	return data
			elif adjustframes == False:
				if type(ColNumber) == list:
					data = []
					for i in ColNumber:
						data.append(args[0]._model.iloc[:,i:i+3].values)
					try:
						f = args[0].fadjust
						data_ = []
						for i in data:
							data_.append(i[f:,:])
						return np.array(data_)
					except AttributeError:
						return np.array(data)
				else:
					data = args[0]._model.iloc[:,ColNumber:ColNumber+3].values
					try:
						f = args[0].fadjust
						return np.array(data[f:,:])
					except AttributeError:
						return np.array(data)
					#if np.isnan(data).any():
					#	print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
					#	sys.exit("NaN value error.")
					#else:
					#	return data
		return wrapper
	return retrivingData_

def retrivingModelDataany(adjustframes):
	def retrivingDataany_(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			ColNumber = func(*args, **kwargs)
			if adjustframes == True:
				data =  args[0]._model.iloc[1:-1,ColNumber+args[2]:ColNumber+args[3]].values
				try:
					f = args[0].fadjust
					return np.array(data[f:,:])
				except AttributeError:
					return np.array(data)
				#if np.isnan(data).any():
				#	print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
				#	sys.exit("NaN value error.")
				#else:
				#	return data
			elif adjustframes == False:
				data = args[0]._model.iloc[:,ColNumber+args[2]:ColNumber+args[3]].values
				try:
					f = args[0].fadjust
					return np.array(data[f:,:])
				except AttributeError:
					return np.array(data)
				#if np.isnan(data).any():
				#	print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
				#	sys.exit("NaN value error.")
				#else:
				#	return data
		return wrapper
	return retrivingDataany_

def retrivingSegmentData(adjustframes,types):
	def retrivingSegmentData_(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			ColNumber = func(*args, **kwargs)
			if adjustframes == True:
				if type(ColNumber) == list:
					data = []
					if types == "angle":
						for each_ColNumber in ColNumber:
							d = args[0]._model.iloc[1:-1,each_ColNumber:each_ColNumber+3].values
							try:
								f = args[0].fadjust
								data.append(d[f:,:])
							except AttributeError:
								data.append(d)
					elif types == "abs":
						for each_ColNumber in ColNumber:
							d = args[0]._model.iloc[1:-1,each_ColNumber+3:each_ColNumber+6].values
							try:
								f = args[0].fadjust
								data.append(d[f:,:])
							except AttributeError:
								data.append(d)
					elif types == "rel":
						for each_ColNumber in ColNumber:
							d = args[0]._model.iloc[1:-1,each_ColNumber+6:each_ColNumber+9].values
							try:
								f = args[0].fadjust
								data.append(d[f:,:])
							except AttributeError:
								data.append(d)
					return np.array(data)
				else:
					if types == "angle": data =  args[0]._model.iloc[1:-1,ColNumber:ColNumber+3].values
					elif types == "abs": data =  args[0]._model.iloc[1:-1,ColNumber+3:ColNumber+6].values
					elif types == "rel": data =  args[0]._model.iloc[1:-1,ColNumber+6:ColNumber+9].values
					try:
						f = args[0].fadjust
						return data[f:,:]
					except AttributeError:
						return data
				#if np.isnan(data).any():
				#	print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
				#	sys.exit("NaN value error.")
				#else:
				#	return data
			elif adjustframes == False:
				if type(ColNumber) == list:
					data = []
					if types == "angle":
						for each_ColNumber in ColNumber:
							d = args[0]._model.iloc[:,each_ColNumber:each_ColNumber+3].values
							try:
								f = args[0].fadjust
								data.append(d[f:,:])
							except AttributeError:
								data.append(d)
					elif types == "abs":
						for each_ColNumber in ColNumber:
							d = args[0]._model.iloc[:,each_ColNumber+3:each_ColNumber+6].values
							try:
								f = args[0].fadjust
								data.append(d[f:,:])
							except AttributeError:
								data.append(d)
					elif types == "rel":
						for each_ColNumber in ColNumber:
							d = args[0]._model.iloc[:,each_ColNumber+6:each_ColNumber+9].values
							try:
								f = args[0].fadjust
								data.append(d[f:,:])
							except AttributeError:
								data.append(d)
					return np.array(data)
				else:
					if types == "angle":data =  args[0]._model.iloc[:,ColNumber:ColNumber+3].values
					elif types == "abs":data =  args[0]._model.iloc[:,ColNumber+3:ColNumber+6].values
					elif types == "rel":data =  args[0]._model.iloc[:,ColNumber+6:ColNumber+9].values
					data = args[0]._model.iloc[:,ColNumber+args[2]:ColNumber+args[3]].values
					try:
						f = args[0].fadjust
						return data[f:,:]
					except AttributeError:
						return data
					#if np.isnan(data).any():
					#	print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
					#	sys.exit("NaN value error.")
			else:
				return data
		return wrapper
	return retrivingSegmentData_


def retrivingDeviceData(adjustframes):
	def retrivingDeviceData_(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			ColNumber = func(*args, **kwargs)
			if adjustframes == True:
				if type(ColNumber) == list:
					try:
						f = args[0].fadjust
						data = np.array([args[0]._device.iloc[100+f*10:-100,i:i+3].values for i in ColNumber])
						return data
					except AttributeError:
						data = np.array([args[0]._device.iloc[100:-100,i:i+3].values for i in ColNumber])
						return data
				else:
					data = args[0]._device.iloc[100:-100,ColNumber:ColNumber+3].values
					try:
						f = args[0].fadjust
						return np.array(data[f*10:])
					except AttributeError:
						return np.array(data)
				#if np.isnan(data).any():
				#	print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
				#	sys.exit("NaN value error.")
				#else:
				#	return data
			elif adjustframes == False:
				if type(ColNumber) == list:
					try:
						f = args[0].fadjust
						data = np.array([args[0]._device.iloc[f*10:,i:i+3].values for i in ColNumber])
						return data
					except AttributeError:
						data = np.array([args[0]._device.iloc[:,i:i+3].values for i in ColNumber])
						return data
				else:
					data = args[0]._device.iloc[:,ColNumber:ColNumber+3].values
					try:
						f = args[0].fadjust
						return np.array(data[f*10:])
					except AttributeError:
						return np.array(data)
				#if np.isnan(data).any():
				#	print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
				#	sys.exit("NaN value error.")
				#else:
				#	return data
		return wrapper
	return retrivingDeviceData_

#======================================================
#EMGデータは1からスタートする仕様に変更(2019.02.11)
#	例えば、3番のEMGを取得する場合、引数には3を入力する。
#	内部では、3-1=2で処理される。
#
# retrivingEMGdata修正案
# resampling用のデコレーターを作成する
#======================================================
def retrivingEMGData(adjustframes):
	def retrivingEMGData_(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			if adjustframes == True:
				ColNumber = func(*args, **kwargs)
				if type(args[1]) == list:
					try:
						f = args[0].fadjust
						data = []
						for name in args[1]:
							emg_num = int(args[0]._emg_name[name])
							data.append(args[0]._device.iloc[100:-100, emg_num + ColNumber].values[f*10])
						return data
					except AttributeError:
						data = []
						for name in args[1]:
							emg_num = int(args[0]._emg_name[name])
							data.append(args[0]._device.iloc[100:-100, emg_num + ColNumber].values)
						return data
				else:
					emg_num = int(args[0]._emg_name[args[1]])
					data = args[0]._device.iloc[100:-100, emg_num + ColNumber].values
				try:
					f = args[0].fadjust
					return data[f*10:]
				except AttributeError:
					return data
			elif adjustframes == False:
				if type(args[1]) == list:
					try:
						f = args[0].fadjust
						data = []
						for name in args[1]:
							emg_num = int(args[0]._emg_name[name])
							data.append(args[0]._device.iloc[:, emg_num + ColNumber].values[f*10])
						return data
					except AttributeError:
						data = []
						for name in args[1]:
							emg_num = int(args[0]._emg_name[name])
							data.append(args[0]._device.iloc[:, emg_num + ColNumber].values)
						return data
				else:
					emg_num = int(args[0]._emg_name[args[1]])
					data = args[0]._device.iloc[:, emg_num + ColNumber - 1].values
				try:
					f = args[0].fadjust
					return data[f*10:]
				except AttributeError:
					return data
		return wrapper
	return retrivingEMGData_



#def retrivingEMGData(adjustframes):
#	def retrivingEMGData_(func):
#		@functools.wraps(func)
#		def wrapper(*args, **kwargs):
#			if adjustframes == True:
#				ColNumber = func(*args, **kwargs)
#				if type(args[1]) == int or type(args[1]) == np.int32:
#					data = args[0]._device.iloc[100:-100,args[1] + ColNumber-1].values
#				else:
#					emg_num = int(args[0]._emg_name[args[1]])
#					data = args[0]._device.iloc[100:-100,emg_num + ColNumber].values
#				if np.isnan(data).any():
#					print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
#					sys.exit("NaN value error.")
#				try:
#					f = args[0].fadjust
#					return data[f*10:]
#				except AttributeError:
#					return data
#			elif adjustframes == False:
#				if type(args[1]) == int or type(args[1]) == np.int32:
#					data = args[0]._device.iloc[100:-100,args[1] + ColNumber-1].values
#				else:
#					emg_num = args[0]._emg_name[args[1]]
#					data = args[0]._device.iloc[100:-100,emg_num + ColNumber].values
#				if np.isnan(data).any():
#					print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
#					sys.exit("NaN value error.")
#				try:
#					f = args[0].fadjust
#					return data[f*10:]
#				except AttributeError:
#					return data
#		return wrapper
#	return retrivingEMGData_



def retrivingEMGData4proc(adjustframes):
	def retrivingEMGData_(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			if adjustframes == True:
				ColNumber = func(*args, **kwargs)
				data = args[0]._device.iloc[100:-100,args[1] + ColNumber-1].values
				if np.isnan(data).any():
					print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
					sys.exit("NaN value error.")
				else:
					try:
						f = args[0].fadjust
						return data[f*10:]
					except AttributeError:
						return data

			elif adjustframes == False:
				data = args[0]._device.iloc[:,args[1] + ColNumber-1].values
				if np.isnan(data).any():
					print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
					sys.exit("NaN value error.")
				else:
					try:
						f = args[0].fadjust
						return data[f*10:]
					except AttributeError:
						return data
		return wrapper
	return retrivingEMGData_


def retrivingMMTData(adjustframes):
	def retrivingEMGData_(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			if adjustframes == True:
				ColNumber = func(*args, **kwargs)
				if type(args[1]) == int or type(args[1]) == np.int32:
					data = args[0].Device.iloc[100:-100,args[1] + ColNumber-1].values
				else:
					emg_num = args[0].EMG_name[args[1]]
					data = args[0].Device.iloc[100:-100,emg_num + ColNumber].values
				#if np.isnan(data).any():
				#	print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
				#	os.exit("NaN value error.")
				try:
					f = args[0].fadjust
					return data[f*10:]
				except AttributeError:
					return data
			elif adjustframes == False:
				if type(args[1]) == int or type(args[1]) == np.int32:
					data = args[0].Device.iloc[100:-100,args[1] + ColNumber-1].values
				else:
					emg_num = args[0].EMG_name[args[1]]
					data = args[0].Device.iloc[100:-100,emg_num + ColNumber].values
				#if np.isnan(data).any():
				#	print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
				#	os.exit("NaN value error.")
				try:
					f = args[0].fadjust
					return data[f*10:]
				except AttributeError:
					return data
		return wrapper
	return retrivingEMGData_


def retrivingJointCenterData(adjustframes):
	def retrivingJointCenterData_(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			ColNumber = func(*args, **kwargs)
			if adjustframes == True:
				if type(ColNumber) == list:
					data = []
					for i in ColNumber:
						data.append(args[0]._model.iloc[1:-1,i:i+3].values)
					return np.array(data)
				else:
					data =  args[0]._model.iloc[1:-1,ColNumber:ColNumber+3].values
					if np.isnan(data).any():
						print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
						sys.exit("NaN value error.")
					else:
						try:
							f = args[0].fadjust
							return np.array(data[f:,:])
						except AttributeError:
							return np.array(data)
			elif adjustframes == False:
				if type(ColNumber) == list:
					data = []
					for i in ColNumber:
						data.append(args[0]._model.iloc[1:-1,i:i+3].values)
					return np.array(data)
				else:
					data = args[0]._model.iloc[:,ColNumber:ColNumber+3].values
					if np.isnan(data).any():
						print(Error_msg["msg003"].format("="*79, args[1] , "="*79))
						sys.exit("NaN value error.")
					else:
						try:
							f = args[0].fadjust
							return np.array(data[f:,:])
						except AttributeError:
							return np.array(data)
		return wrapper
	return retrivingJointCenterData_
