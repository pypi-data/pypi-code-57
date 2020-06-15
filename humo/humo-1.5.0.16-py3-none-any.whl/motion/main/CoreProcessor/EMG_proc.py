import numpy as np
from scipy import signal
import functools


def alignBaseline(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		data = func(*args, **kwargs)
		if type(data) == list:
			alignData = []
			for i in data:
				alignData.append(i - i[:100].mean())
			return np.array(alignData)

		else:
			return data - data[:100].mean()
	return wrapper

# ASP, SSPの種類を変更する。
# cfgがなければデフォルトの処理を行うようにする。
def filtEMG(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		data = func(*args, **kwargs)
		if not args[0].cfg:
			order, fq1, fq2 = 4.0, 20.0, 480.0
		else:
			order, fq1, fq2, fq3 = args[0].cfg["EMGfilter"]
		b,a = signal.butter(order,[fq1*2.0/1000,fq2*2.0/1000],"band",analog=False)
		if type(data) == list:
			return np.array([signal.filtfilt(b, a, i) for i in data])
		else:
			return signal.filtfilt(b,a, data)
	return wrapper

def takeAbsvalues(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		data = func(*args, **kwargs)
		if type(data) == list:
			return np.array(np.abs(i) for i in data)
		else:
			return np.abs(data)
	return wrapper

def smoothingEMG(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		data = func(*args, **kwargs)
		if not args[0].cfg:
			order, fq3 = 4.0, 10.0
		else:
			order, fq1, fq2, fq3 = args[0].cfg["EMGfilter"]
		b, a = signal.butter(order,fq3*2.0/1000,"low",analog=False)
		if type(data) == list:
			return np.array([signal.filtfilt(b, a, i) for i in data])
		else:
			return signal.filtfilt(b,a, data)
	return wrapper


def normalized_with_MVC(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		data = func(*args, **kwargs)
		if data.ndim == 1:
			mvc = args[0]._mvc["MVCvalues"][args[1]]
			return data*100 / mvc
		else:
			mvc = np.array([args[0]._mvc["MVCvalues"][name] for name in args[1]])
			return np.array([100*i/j for i,j in zip(data, mvc)])
	return wrapper


#def normalized_with_MVC(func):
#	@functools.wraps(func)
#	def wrapper(*args, **kwargs):
#		if type(args[1]) == int or type(args[1]) == np.int32:
#			name = list(args[0]._mvc["EMG_name"])[args[1]-1]
#		else:
#			name = args[1]
#		mvc = args[0]._mvc["MVCvalues"][name]
#		emg = func(*args, **kwargs)
#		return emg*100.0 / mvc
#	return wrapper


def FFTprocess(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		from scipy.fftpack import fft, fftfreq
		emg, dt = func(*args, **kwargs)
		a = np.abs(fft(emg)[1:int(emg.size/2)])
		b = fftfreq(emg.size,dt)[1:int(emg.size/2)]
		return a, b
	return wrapper

def calc_MPF(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		power, freq = func(*args, **kwargs)
		return np.sum(power*freq) / power.sum()
	return wrapper


def calc_MF(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		power, freq = func(*args,**kwargs)
		from scipy import integrate
		index,next_index = 1, 2
		left,right = integrate.simps(power[0:index]),integrate.simps(power[index:])
		while left < right:
			index +=1
			next_index += 1
			left,right = integrate.simps(power[0:index]),integrate.simps(power[index:])
		else:
			return freq[index]
	return wrapper

def calc_APDF(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		emg = func(*args, **kwargs)
		return np.array([np.where(emg < i)[0].size / emg.size for i in range(100)])
	return wrapper

