import os
import sys
import numpy as np
import pandas as pd
from scipy.interpolate import splev, splrep
from scipy import signal
import sys
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
checking data
"""
def showheader(types):
	def showheader_(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			if types == "marker":
				header = args[0]._mkheader
			elif types == "model":
				header = args[0]._modelheader
			elif types == "device":
				header = args[0]._deviceheader

			if types == "marker" or types == "model":
				newNameList = []
				for i in header:
					try:
						int(i)
					except:
						newNameList.append(i)
				return newNameList
			else:
				NameList = []
				for i in header:
					if "unnamed" in i or "Unnamed" in i:
						pass
					else:
						NameList.append(i)
				return NameList
		return wrapper
	return showheader_


def find_name(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		NameList, name = func(*args, **kwargs)
		findedList = []
		for i in NameList:
			if name.lower() in i.lower():
				findedList.append(i)
		if not findedList:
			print("There is no columns such as {}...".format(name))
		return findedList
	return wrapper

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Marker
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def isMarkerName(func):
	@functools.wraps(func)
	def wrapper(*args,**kwargs):
		try:
			if type(args[1]) == list:
				ColNumbers = []
				for i in args[1]:
					ColNumbers.append(args[0]._mkheader.index(i.lower()))
				return ColNumbers
			else:
				ColNumber = args[0]._mkheader.index(args[1].lower())
				return ColNumber
		except ValueError:
			print(Error_msg["msg001"].format("="*79, args[1] , "="*79))
			sys.exit("ValueError : Incorrect marker name")
	return wrapper


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Model
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def isModelName(model_parameter):
	def isModelName_(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			if type(args[1]) == list:name = args[1][0]
			else:name = args[1]

			if model_parameter == "angles" or model_parameter == "moment" or model_parameter == "force" or model_parameter == "power":
				if name.lower() + model_parameter in args[0]._modelheader:
					if type(args[1]) == list:
						ColNumber = []
						for i in args[1]:
							ColNumber.append(args[0]._modelheader.index(i.lower() + model_parameter))
					else:
						ColNumber = args[0]._modelheader.index(args[1].lower() + model_parameter)
					return ColNumber
				elif name.lower() + model_parameter + "_m" in args[0]._modelheader:
					if type(args[1]) == list:
						ColNumber = []
						for i in args[1]:
							ColNumber.append(args[0]._modelheader.index(i.lower() + model_parameter + "_m"))
					else:
						ColNumber = args[0]._modelheader.index(args[1].lower() + model_parameter + "_m")
					return ColNumber
				else:
					print(Error_msg["msg001"].format("="*79, args[1] , "="*79))
					sys.exit("ValueError : Incorrect joint name")

			elif model_parameter == "abs":
				#Determine whether the input argument is a list or a single argument.
				if type(args[1]) == list:
					name = []
					for i in args[1]:
						name.append(i.lower()[0] + model_parameter + i.lower()[1:] + "angle")
				else:
					name = args[1].lower()[0] + model_parameter + args[1].lower()[1:] + "angle"
				# Get column number
				if type(name) == list:
					if name[0] in args[0]._modelheader:
						ColNumber = []
						for i in name:
							ColNumber.append(args[0]._modelheader.index(i))
						return ColNumber
					elif name[0] + "_m" in args[0]._modelheader:
						ColNumber = []
						for i in name:
							ColNumber.append(args[0]._modelheader.index(i + "_m"))
						return ColNumber
					else:
						print(Error_msg["msg001"].format(""*79, args[1], "="*79))
						sys.exit("ValueError : Incorrect joint name")
				else:
					if name in args[0]._modelheader:
						ColNumber = args[0]._modelheader.index(name)
						return ColNumber
					elif name + "_m" in args[0]._modelheader:
						ColNumber = args[0]._modelheader.index(name + "_m")
						return ColNumber
					else:
						print(Error_msg["msg001"].format(""*79, args[1], "="*79))
						sys.exit("ValueError : Incorrect joint name")
		return wrapper
	return isModelName_





def isCOMname(floor):
	def isCOMname_(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			if floor == False:
				if "CentreOfMass".lower() in args[0]._modelheader:
					ColNumber = args[0]._modelheader.index("CentreOfMass".lower())
					return ColNumber
				elif "CentreOfMass_M".lower() in args[0]._modelheader:
					ColNumber = args[0]._modelheader.index("CentreOfMass_M".lower())
					return ColNumber
				else:
					print(Error_msg["msg001"].format("="*79, args[1] , "="*79))
					sys.exit("ValueError : Incorrect joint name")

			elif floor == True:
				if "CentreOfMassfloor".lower() in args[0]._modelheader:
					ColNumber = args[0]._modelheader.index("CentreOfMassfloor".lower())
					return ColNumber
				elif "CentreOfMassfloor_M".lower() in args[0]._modelheader:
					ColNumber = args[0]._modelheader.index("CentreOfMassfloor_M".lower())
					return ColNumber
				else:
					print(Error_msg["msg001"].format("="*79, args[1] , "="*79))
					sys.exit("ValueError : Incorrect joint name")
		return wrapper
	return isCOMname_

def isSegmentCOMname(func): # multi outputに対応させるためのアルゴリズムを考える
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		if type(args[1]) == list:
			ColNumber = []
			for each_name in args[1]:
				if each_name[0] == "R":
					ColNumber.append(args[0]._modelheader.index("right" + each_name[1:].lower() + "com"))
				elif each_name[0] == "L":
					ColNumber.append(args[0]._modelheader.index("left" + each_name[1:].lower() + "com"))
				else:
					ColNumber.append(args[0]._modelheader.index(each_name.lower() + "com"))
			print(ColNumber)
			return ColNumber
		else:
			if args[1][0] == "R":
				ColNumber = args[0]._modelheader.index("right" + args[1][1:].lower() + "com")
			elif args[1][0] == "L":
				ColNumber = args[0]._modelheader.index("left" + args[1][1:].lower() + "com")
			else:
				ColNumber = args[0]._modelheader.index(args[1].lower() + "com")
			return ColNumber
	return wrapper








#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Device
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def isDeviceName(types):
	def isDeviceName_(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			if type(args[1]) == list:
				if type(args[1][0]) == str and (args[1][0].lower() == "l" or args[1][0].lower() == "r"):
					if args[0].cfg:
						DeviceName = [args[0].cfg["BeltekName"][i.upper()].lower() + types for i in args[1]]
					else:
						devicename = {
							"L": "S018196L - ",
							"R": "S018197R - "
						}
						DeviceName = [devicename[i.upper()].lower() + types for i in args[1]]
				else:
					DeviceName = ["fp{} - {}".format(i,types) for i in args[1]]
				return [args[0]._deviceheader.index(i) for i in DeviceName]

			else:
				if type(args[1]) == str and (args[1].lower() == "l" or args[1].lower() == "r"):
					if args[0].cfg:
						DeviceName = args[0].cfg["BeltekName"][args[1].upper()].lower() + types
					else:
						devicename = {
							"L": "S018196L - ",
							"R": "S018197R - "
						}
						DeviceName = devicename[args[1].upper()].lower() + types
				else:
					DeviceName = "fp{} - {}".format(args[1],types)
				return args[0]._deviceheader.index(DeviceName)
		return wrapper
	return isDeviceName_


def isSegmentName(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		if type(args[1]) == list:
			ColNumber = []
			for each_name in args[1]:
				ColNumber.append(args[0]._modelheader.index(each_name.lower()))
		else:
			ColNumber = args[0]._modelheader.index(args[1].lower())
		return ColNumber
	return wrapper


def isEMGName(types):
	def isEMGName_(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			if types == "Delsys":
				if args[0].cfg:
					for DeviceName in args[0].cfg["EMGdevice"]:
						if DeviceName.lower() in args[0]._deviceheader:
							return args[0]._deviceheader.index(DeviceName.lower())
				else:
					for DeviceName in ["Delsys - voltage", "Delsys[1000Hz] - voltage"]:
						if DeviceName.lower() in args[0]._deviceheader:
							return args[0]._deviceheader.index(DeviceName.lower())
					#else:
					#	print("There is no name such as {}".format(DeviceName))
		return wrapper
	return isEMGName_

def isMMTName(types):
	def isEMGName_(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			EMG_device_name = [
				"Delsys - voltage",
				"Delsys[1000Hz] - voltage"
			]
			Device_header_list = [i.lower() for i in args[0].DeviceHeader]
			if types == "Delsys":
				for DeviceName in EMG_device_name:
					if DeviceName.lower() in Device_header_list:
						return Device_header_list.index(DeviceName.lower())
					else:
						print("There is no name such as {}".format(DeviceName))
		return wrapper
	return isEMGName_

def isModelany(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		ColNumber = args[0]._modelheader.index(args[1].lower())
		return ColNumber
	return wrapper


