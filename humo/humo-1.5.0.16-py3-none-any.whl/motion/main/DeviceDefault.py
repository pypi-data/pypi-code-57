import numpy as np
import pandas as pd
from functools import lru_cache
import pathlib



from .CoreProcessor import * # Core処理用のモジュールをimportする

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

class CoreDevice:

	def __init__(self,data, **kwargs):
		self._ID = data["ID"]
		# each data
		self._device = data["device"][0]
		# header data
		self._deviceheader = [i.lower() for i in data["device"][1]]
		self.deviceheader = data["device"][1]
		# spep
		self._spep = data["spep"]
		if "cfg" in kwargs.keys():
			self.cfg = kwargs["cfg"]
		else:
			self.cfg = None
		# EMG name
		self._emg_name = data["EMG_name"]
		self._mvc = data["MMT"]
		self._rawEMG = data["rawMMT"]


	def getDeviceList(self):
		"""Summary line.
		Display the header of device data.

		Parameters
		----------
		None

		Returns
		-------
		None
		"""
		try:
			header = [i for i in self._device.columns if "Unnamed" not in i]
			print("--------------------------------------")
			print("<< Check the data about Device >>")
			print("The number of device header : {}".format(len(header)))
			print("--------------------------------------")
			for name in ["Force", "Moment", "CoP"]:
				print("Force plate - '{}'".format(name))
				print("=======================")
				for i in header:
					if name in i:
						print("    > {}".format(i))
				print("")
			print("'Others'")
			print("=======================")
			for i in header:
				if ("Force" not in i) & ("Moment" not in i) & ("CoP" not in i):
					print("    > {}".format(i))
		except AttributeError:
			print("Please set Data.")
##########################################################################
# getSwitch
##########################################################################


	def getSwitch(self):
		"""Summary line.
		Get the time series data of the trigger that was input to divide the trials.

		Parameters
		----------
		None

		Returns
		-------
		ndarray

		Note
		------
		- Sampling rate : 1000Hz

		"""
		trigger = list(set(self.cfg["Trigger"]) & set(self.deviceheader))[0]
		trigger_index = self.deviceheader.index(trigger)
		return self._device.iloc[:,trigger_index].values

##########################################################################
# Device Data
#	"getting device data"
##########################################################################
	@cvt_HumoArray(argsType="ForcePlate")
	@retrivingDeviceData(adjustframes=True)
	@isDeviceName(types="force")
	def getFPforce(self,name):
		"""Summary line.
		Get Force data of floor reaction force meter.

		Parameters
		----------
		name : int or str
			force plate number or left and right

		Returns
		-------
		humoArray
			It is output in the order of x axis, y axis, z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		"""
		return


	@cvt_HumoArray(argsType="ForcePlate")
	@retrivingDeviceData(adjustframes=True)
	@isDeviceName(types="moment")
	def getFPmoment(self,name):
		"""Summary line.
		Get moment data of floor reaction force meter.

		Parameters
		----------
		name : int or str
			force plate number or left and right

		Returns
		-------
		humoArray
			It is output in the order of x axis, y axis, z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		"""
		return


	@cvt_HumoArray(argsType="ForcePlate")
	@retrivingDeviceData(adjustframes=True)
	@isDeviceName(types="cop")
	def getFPcop(self, name):
		"""Summary line.
		Get COP data of floor reaction force meter.

		Parameters
		----------
		name : int or str
			force plate number or left and right

		Returns
		-------
		humoArray
			It is output in the order of x axis, y axis, z axis.

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		"""
		return

##########################################################################
# Device Data
##########################################################################


	@cvt_divHumoArray(argsType="ForcePlate")
	@dividingDeviceData(dimension=3)
	def divFPforce(self,name, step=None):
		"""Summary line.
		Get the force of the force plate separated by the trigger.

		Parameters
		----------
		name : int or str
			force plate number or left and right

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		"""
		return self.getFPforce(name)


	@cvt_divHumoArray(argsType="ForcePlate")
	@dividingDeviceData(dimension=3)
	def divFPmoment(self, name, step=None):
		"""Summary line.
		Get the moment of the force plate separated by the trigger.

		Parameters
		----------
		name : int or str
			force plate number or left and right

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		"""
		return self.getFPmoment(name)


	@cvt_divHumoArray(argsType="ForcePlate")
	@dividingDeviceData(dimension=3)
	def divFPcop(self, name, step=None):
		"""Summary line.
		Get COP of the force plate separated by the trigger.

		Parameters
		----------
		name : int or str
			force plate number or left and right

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		"""
		return self.getFPcop(name)



##########################################################################
#EMG Data
#	"gettign EMG data."




##########################################################################


	@cvt_HumoArrayEMG
	@filtEMG
	@alignBaseline
	@retrivingEMGData(adjustframes=True)
	@isEMGName(types="Delsys")
	def getEMGraw(self, name):
		"""Summary line.
		Get raw EMG data.

		Parameters
		----------
		name : str
			Name of muscle to be tested

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		"""
		return


	@cvt_HumoArrayEMG
	@takeAbsvalues
	def getEMGabs(self, name):
		"""Summary line.
		Get abs EMG data.

		Parameters
		----------
		name : str
			Name of muscle to be tested

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		"""
		return self.getEMGraw(name)


	@cvt_HumoArrayEMG
	@smoothingEMG
	def getEMGarv(self, EMG_num):
		"""Summary line.
		Get arv EMG data.

		Parameters
		----------
		name : str
			Name of muscle to be tested

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		- The arv process does the following:
			1. Align the baseline
			2. Butterworth bandpass filtering
				- order: 4
				- Cutoff frequency[Hz]: 20 (low), 480 (high)
			3. Absolute value conversion
			4. Butterworth low pass filtering
				- order: 4
				- Cutoff frequency: 6Hz

		If you want to change the filtering parameters, change cfg.json. 
		Enter the cfg parameter when creating a humo instance.
		
		[Exsample]
		cfg_file = humo.dataIO.load_cfg()
		data = humo.dataIO.load_data()
		obj = humo.motion.CoreMain(data, cfg = cfg_file)
		"""
		return self.getEMGabs(EMG_num)



##########################################################################
#EMG data
#	"gettting EMG data divided with trigger."




##########################################################################


	@cvt_divHumoArrayEMG
	@dividingDeviceData(dimension=1)
	def divEMGraw(self, name, step=None):
		"""Summary line.
		Get raw EMG data separated by triggers.

		Parameters
		----------
		name : str
			Name of muscle to be tested
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
		return self.getEMGraw(name)


	@cvt_divHumoArrayEMG
	@dividingDeviceData(dimension=1)
	def divEMGabs(self, name, step=None):
		"""Summary line.
		Get abs EMG data separated by triggers.

		Parameters
		----------
		name : str
			Name of muscle to be tested
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
		return self.getEMGabs(name)


	@cvt_divHumoArrayEMG
	@dividingDeviceData(dimension=1)
	def divEMGarv(self, EMG_num,step=None):
		"""Summary line.
		Get arv EMG data separated by triggers.

		Parameters
		----------
		name : str
			Name of muscle to be tested
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

		- The arv process does the following:
			1. Align the baseline
			2. Butterworth bandpass filtering
				- order: 4
				- Cutoff frequency[Hz]: 20 (low), 480 (high)
			3. Absolute value conversion
			4. Butterworth low pass filtering
				- order: 4
				- Cutoff frequency: 6Hz

		If you want to change the filtering parameters, change cfg.json. 
		Enter the cfg parameter when creating a humo instance.
		
		[Exsample]
		cfg_file = humo.dataIO.load_cfg()
		data = humo.dataIO.load_data()
		obj = humo.motion.CoreMain(data, cfg = cfg_file)
		"""
		return self.getEMGarv(EMG_num)

##########################################################################
#EMG data normalized with MVC
#	"gettting EMG data divided with trigger."




##########################################################################


	@cvt_HumoArrayEMG
	@normalized_with_MVC
	def getSICraw(self, name):
		"""Summary line.
		Get raw EMG data normalized by MMT.

		Parameters
		----------
		name : str
			Name of muscle to be tested

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		- In order to normalize with MMT, it is necessary to include MMT measurement data during pkl conversion.
		- EMG is normalized by the maximum amplitude when measuring MMT. 
		"""
		return self.getEMGraw(name)


	@cvt_HumoArrayEMG
	@normalized_with_MVC
	def getSICabs(self, name):
		"""Summary line.
		Get abs EMG data normalized by MMT.

		Parameters
		----------
		name : str
			Name of muscle to be tested

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		- In order to normalize with MMT, it is necessary to include MMT measurement data during pkl conversion.
		- EMG is normalized by the maximum amplitude when measuring MMT. 
		"""
		return self.getEMGabs(name)


	@cvt_HumoArrayEMG
	@normalized_with_MVC
	def getSICarv(self, EMG_num):
		"""Summary line.
		Get arv EMG data normalized by MMT.

		Parameters
		----------
		name : str
			Name of muscle to be tested

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		- In order to normalize with MMT, it is necessary to include MMT measurement data during pkl conversion.
		- EMG is normalized by the maximum amplitude when measuring MMT. 

		- The arv process does the following:
			1. Align the baseline
			2. Butterworth bandpass filtering
				- order: 4
				- Cutoff frequency[Hz]: 20 (low), 480 (high)
			3. Absolute value conversion
			4. Butterworth low pass filtering
				- order: 4
				- Cutoff frequency: 6Hz
		"""
		return self.getEMGarv(EMG_num)

##########################################################################
#retrived EMG data normalized with MVC
#	"gettting EMG data divided with trigger."
##########################################################################


	@dividingDeviceData(dimension=1)
	def divSICraw(self, name):
		"""Summary line.
		Get raw EMG data separated by trigger.
		This data is MMT normalized.

		Parameters
		----------
		name : str
			Name of muscle to be tested

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		- In order to normalize with MMT, it is necessary to include MMT measurement data during pkl conversion.
		- EMG is normalized by the maximum amplitude when measuring MMT. 
		"""
		return self.getSICraw(name)


	@dividingDeviceData(dimension=1)
	def divSICabs(self, EMG_num):
		"""Summary line.
		Get abs EMG data separated by trigger.
		This data is MMT normalized.

		Parameters
		----------
		name : str
			Name of muscle to be tested

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		- In order to normalize with MMT, it is necessary to include MMT measurement data during pkl conversion.
		- EMG is normalized by the maximum amplitude when measuring MMT. 
		"""
		return self.getSICabs(EMG_num)


	@dividingDeviceData(dimension=1)
	def divSICarv(self, EMG_num):
		"""Summary line.
		Get arv EMG data separated by trigger.
		This data is MMT normalized.

		Parameters
		----------
		name : str
			Name of muscle to be tested

		Returns
		-------
		humoArray

		note
		------
		- If you want to get multiple data at the same time, enter a list.
		- In order to normalize with MMT, it is necessary to include MMT measurement data during pkl conversion.
		- EMG is normalized by the maximum amplitude when measuring MMT. 

		- The arv process does the following:
			1. Align the baseline
			2. Butterworth bandpass filtering
				- order: 4
				- Cutoff frequency[Hz]: 20 (low), 480 (high)
			3. Absolute value conversion
			4. Butterworth low pass filtering
				- order: 4
				- Cutoff frequency: 6Hz
		"""
		return self.getSICarv(EMG_num)

##########################################################################
#EMG anlysis
##########################################################################


	@FFTprocess
	def FFT(self, EMG_num, dt = 0.001):
		"""
		Summary line.

		Parameters
		----------
		EMG_num : int or str
			the number of EMG or name of muscle
		dt : float
			default is 0.001. sampling rate.

		Returns
		-------
		a : x axis(seq)
			np.array
		b : y aixs(FFT)
			np.array
	"""
		return self.getEMGraw(EMG_num), dt



	@calc_MF
	def FFT2MF(self, EMG_num, dt=0.001):
		"""
		Summary line.
		Calculate the median power frequency.
		A frequency that divides the area of the power spectrum into two equal areas.

		Parameters
		----------
		EMG_num : int or str
			the number of EMG or name of muscle
		dt : float
			default is 0.001. sampling rate.

		Returns
		-------
		median power freqency : float
		"""
		return self.FFT(EMG_num, dt)



	@calc_MPF
	def FFT2MPF(self, EMG_num, dt=0.001):
		"""
		Summary line.
		Calculate the mean power frequency.

		Parameters
		----------
		EMG_num : int or str
			the number of EMG or name of muscle
		dt : float
			default is 0.001. sampling rate.

		Returns
		-------
		mean power freqency : float
		"""
		return self.FFT(EMG_num, dt)



	@calc_APDF
	def APDF(self, EMG_num):
		return self.getSICarv(EMG_num)



	def APDFbasevalue(self, EMG_num):
		a = self.APDF(EMG_num)
		return np.where(a < 0.51)[0][-1]


	def APDFmaxvalue(self, EMG_num):
		a = self.APDF(EMG_num)
		return np.where(a < 1.0)[0][-1]
