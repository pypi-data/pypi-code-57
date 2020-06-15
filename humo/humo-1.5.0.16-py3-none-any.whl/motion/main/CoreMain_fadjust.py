#import os
#import sys
#import numpy as np
#import pandas as pd
#from scipy.interpolate import splev, splrep
#from scipy import signal
#from scipy import fftpack
#import functools
import inspect
from .CoreProcessor import *
from .DeviceDefault import CoreDevice
from .ModelDefault import CoreModel
from .MarkerDefault import CoreMarker


class CoreMain_fadjust(Values,CoreDevice,CoreModel,CoreMarker):
	"""Summary line.
	The CoreMain class gets the data measured by the 3D motion
	analysis device VICON.
	The keywords of the CoreMain class are as follows;
		1. Easily
		2. Quickly
		3. High expandability
	This class is supposed to use data measured using trigger.
	If there is trigeer data, div type method can be used,
	and it is possible to easily obtain multiple trials
	from a single measurement data.

	Parameters
	----------
	data : Composite type
		This data is made by preprocessing module.
	systemsettings : pkl file
	anallysissettings : pkl file

	Returns
	-------
	CoreMain instance
		This instance has many very useful methods.
		Please confirm from the following HP for details.
		'https://sites.google.com/view/pythonforeveryone/python-for-evryone'
	"""
	def __init__(self, data, cfg, fadjust):
		super().__init__(data, cfg)
		self.fadjust = fadjust


	def getmethod(self):
		"""Summary line.
		Search for a method.

		Parameters
		----------
		None

		Returns
		-------
		list
		All methods of the class.
		"""
		method = []
		for i in inspect.getmembers(self,inspect.ismethod):
			method.append(i[0])
		method.remove("__init__")
		return method


	def ismethod(self, name):
		"""Summary line.
		Search for a method.

		Parameters
		----------
		name : str
			Method name to search.

		Returns
		-------
		list
			all methods including name.
		"""
		if not name:
			return self.getmethod()
		else:
			method = self.getmethod()
			findedmethod = [i for i in method if name[0] in i]
			return findedmethod



