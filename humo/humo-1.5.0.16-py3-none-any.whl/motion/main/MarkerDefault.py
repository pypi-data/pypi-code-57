import os
import sys
import numpy as np
import pandas as pd
from scipy.interpolate import splev, splrep
from scipy import signal
from scipy import fftpack
import functools
import pathlib


from .CoreProcessor import *


'''
Make docstrings consistent with google style.
The following is an example.
Use copy and paste

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

		"""Summary line.

		Parameters
		----------
		arg1 : str
			Name of markers.

		Returns
		-------
		array(3 dimension)
			It is output in the order of x axis, y axis, z axis.
		"""

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''





class CoreMarker:
	def __init__(self,data, **kwargs):
		self._ID = data["ID"]
		# each data
		self._marker = data["marker"][0]
		# header data
		self._mkheader = [i.lower() for i in data["marker"][1]]
		self.mkheader = data["marker"][1]
		# spep
		self._spep = data["spep"]
		try:
			self.cfg = kwargs["cfg"]
		except:
			self.cfg = None
		# EMG name
		self._emg_name = data["EMG_name"]
		self.mvc = data["MMT"]


	def getMarkerList(self):
		try:
			header = [i for i in self._marker.columns if "Unnamed" not in i]
			print("--------------------------------------")
			print("<< Check the data about Markers >>")
			print("The number of model header : {}".format(len(header)))
			for name in ["R", "L"]:
				if name == "R":
					print("{} side marker".format("Right"))
					print("=========================")
				elif name == "L":
					print("{} side marker".format("Left"))
					print("=========================")
				for i in header:
					if name in i[0]:
						print(i)
				print("")
			print("Others data")
			print("=========================")
			for i in header:
				if ("R" != i[0]) & ("L" != i[0]):
					print(i)
		except AttributeError:
			print("Please set Data.")


	def spep(self):
		if self._spep == None:
			print("Did you use Trigger in this measurement?")
			print("If you are using spep data is insufficient.")
		else:
			print("=================================================")
			print("Start and end point of motion decided by trigger")
			print("=================================================")
			print("start point [ 100Hz]  : {}".format(self._spep[0][0]))
			print("end   point [ 100Hz]  : {}".format(self._spep[0][1]))
			print("start point [1000Hz]  : {}".format(self._spep[1][0]))
			print("start point [1000Hz]  : {}".format(self._spep[1][1]))

	"""
	setter : Set it if necessary.
	"""
	@showheader("marker")
	def markerCols(self):
		return

	@find_name
	def is_marker(self, name):
		return self.markerCols(), name


	"""
	Main processing
	"""


	@cvt_HumoArray(argsType="general")
	@retrivingMarkerData(True)
	@isMarkerName
	def getMarker(self, name):
		"""Summary line.
		Output the coordinate data of the specified marker.
		Only one marker name can be accepted.

		Parameters
		----------
		name : str
			Name of markers.

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		"""
		return


	@cvt_HumoArray(argsType="general")
	@differentation(difforder="1st")
	@retrivingMarkerData(False)
	@isMarkerName
	def getMarkerVel(self, name):
		"""Summary line.
		The 'first derivative' of the marker coordinates is output
		with the 'second order accuracy of the central difference method'.
		Only one marker name can be accepted.

		Parameters
		----------
		name : str
			Name of markers.

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		"""
		return


	@cvt_HumoArray(argsType="general")
	@differentation(difforder="2nd")
	@retrivingMarkerData(False)
	@isMarkerName
	def getMarkerAcc(self, name):
		"""Summary line.
		The 'second derivative' of the marker coordinates is output
		with the 'second order accuracy of the central difference method'.
		Only one marker name can be accepted.

		Parameters
		----------
		name : str
			Name of markers.

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		"""
		return


	"""
	dividing data by trigger
	"""
	@cvt_divHumoArray(argsType="general")
	@dividingData(dimension=3)
	def divMarker(self, name, step=None):
		"""Summary line.
		Output marker coordinates delimited by triggers.
		Marker coordinates in each operation are stored in the list and output.

		Parameters
		----------
		name : str
			Name of markers.
		step : list
			It is used when you want to get an even or odd trial.

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
		"""
		data = self.getMarker(name)
		return data


	@cvt_divHumoArray(argsType="general")
	@dividingData(dimension=3)
	def divMarkerVel(self, name, step=None):
		"""Summary line.
		Output marker coordinates delimited by triggers.
		Marker velocity in each operation are stored in the list and output.

		Parameters
		----------
		name : str
			Name of markers.
		step : list
			It is used when you want to get an even or odd trial.

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
		"""
		data = self.getMarkerVel(name)
		return data


	@cvt_divHumoArray(argsType="general")
	@dividingData(dimension=3)
	def divMarkerAcc(self, name, step=None):
		"""Summary line.
		Output marker coordinates delimited by triggers.
		Marker acceleration in each operation are stored in the list and output.

		Parameters
		----------
		name : str
			Name of markers.
		step : list
			It is used when you want to get an even or odd trial.

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		- About step argument
		If you want to get an even numbered trial,

		obj.divEMGraw ("muscle", step = [0,2])

		In short, it's just obj [0 :: 2].
		"""
		data = self.getMarkerAcc(name)
		return data
