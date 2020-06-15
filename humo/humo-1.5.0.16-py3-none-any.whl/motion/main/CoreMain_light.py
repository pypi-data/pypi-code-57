import os
import sys
import numpy as np
import pandas as pd
from scipy.interpolate import splev, splrep
from scipy import signal
from scipy import fftpack
import functools
import inspect

from .CoreProcessor import *
from .DeviceDefault import CoreDevice
from .ModelDefault import CoreModel
from .MarkerDefault import CoreMarker


class CoreMain(CoreDevice,CoreModel,CoreMarker):
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
	def __init__(self, data, cfg):
		super().__init__(data, cfg)
		

	
	def ismethods(self, name):
		"""

		Find the method that the instance has.
		It outputs a partially matched method.
		
		Parameters
		----------
		arg1 : str
			method name

		Returns
		-------
		list
			List of methods partially matched with arguments
		"""
		methods = []
		for x in inspect.getmembers(self, inspect.ismethod):
			methods.append(x[0])
		findedMethods = []
		for i in methods:
			if name.lower() in i.lower():
				findedMethods.append(i)
		return findedMethods



