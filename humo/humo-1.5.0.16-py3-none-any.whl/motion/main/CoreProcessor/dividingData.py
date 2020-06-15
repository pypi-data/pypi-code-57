import os
import sys
import numpy as np
import pandas as pd
from scipy.interpolate import splev, splrep
from scipy import signal
from scipy import fftpack
import functools


"""
Dividing data with trigger.
"""
def dividingData(dimension):
    def _dividingData(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            sp, ep = args[0]._spep[0][0], args[0]._spep[0][1]
            if not kwargs:
                pass
            else:
                first_term, tolerance = kwargs["step"][0], kwargs["step"][1]
                sp, ep = sp[first_term::tolerance], ep[first_term::tolerance]
            maxlength = (ep - sp).max()
            if dimension == 3:
                try:
                    if type(args[1]) == list:
                        dividedData = []
                        for eachdata in data:
                            dividedData_ = []
                            for s, e in zip(sp, ep):
                                mat = np.full([maxlength,3],np.nan)
                                mat[:(e-s),:] = eachdata[s:e,:]
                                dividedData_.append(mat)
                            dividedData.append(dividedData_)
                        dividedData = np.array(dividedData)
                    else:
                        dividedData = []
                        for s, e in zip(sp,ep):
                            mat = np.full([maxlength,3],np.nan)
                            mat[:(e-s),:] = data[s:e,:]
                            dividedData.append(mat)
                    return np.array(dividedData)
                except IndexError:
                    dividedData = []
                    for s, e in zip(sp,ep):
                        mat = np.full([maxlength,3],np.nan)
                        mat[:(e-s),:] = data[s:e,:]
                        dividedData.append(mat)
                    return np.array(dividedData)
            else:
                pass
        return wrapper
    return _dividingData
#def dividingData(dimension):
#	def _dividingData(func):
#		@functools.wraps(func)
#		def wrapper(*args, **kwargs):
#			data = func(*args, **kwargs)
#			sp, ep = args[0]._spep[0][0], args[0]._spep[0][1]
#			if not kwargs:
#				pass
#			else:
#				first_term, tolerance = kwargs["step"][0], kwargs["step"][1]
#				sp, ep = sp[first_term::tolerance], ep[first_term::tolerance]
#			dividedData = []
#			if dimension == 3:
#				try:
#					if type(args[1]) == list:
#						for i in data:
#							dividingData_ = []
#							for j in range(len(sp)):
#								dividingData_.append(np.array(i[sp[j]:ep[j],:]))
#							dividedData.append(dividingData_)
#						mat = []
#						for i in dividedData:
#							matsize_index = np.array([j.shape[0] for j in i]).argmax()
#							maxlow, maxcolumn = i[matsize_index].shape
#							mat_ = []
#							for k in i:
#								l, c = k.shape
#								mat__ = np.zeros([maxlow, maxcolumn])
#								mat__[:,:] = np.nan
#								mat__[:l, :c] = k
#								mat_.append(mat__)
#							mat.append(mat_)
#						dividedData = mat
#						del mat, mat_, mat__
#					else:
#						for i in range(len(sp)):
#							dividedData.append(np.array(data[sp[i]:ep[i],:]))
#						matsize_index = np.array([i.shape[0] for i in dividedData]).argmax()
#						maxlow, maxcolumn = dividedData[matsize_index].shape
#						mat = []
#						for i in dividedData:
#							l, c = i.shape
#							mat_ = np.zeros([maxlow, maxcolumn])
#							mat_[:,:] = np.nan
#							mat_[:l, :c] = i
#							mat.append(mat_)
#						dividedData = mat
#						del mat, mat_
#				except IndexError: # for COM, COM_floor. These don't need argments.
#					#for i in range(len(sp)):
#					#	dividedData.append(np.array(data[sp[i]:ep[i],:]))
#					dividedData = [np.array(data[sp[i]:ep[i],:]) for i in range(len(sp))]
#					matsize_index = np.array([i.shape[0] for i in dividedData]).argmax()
#					maxlow, maxcolumn = dividedData[matsize_index].shape
#					mat = []
#					for i in dividedData:
#						l, c = i.shape
#						mat_ = np.zeros([maxlow, maxcolumn])
#						mat_[:,:] = np.nan
#						mat_[:l, :c] = i
#						mat.append(mat_)
#					dividedData = mat
#					del mat, mat_
#			elif dimension == 1:
#				if type(args[1]) == list:
#					for i in data:
#						dividingData_ = []
#						for j in range(len(sp)):
#							dividingData_.append(np.array(i[sp[i]:ep[i]]))
#						dividedData.append(dividingData_)
#				else:
#					for i in range(len(sp)):
#						dividedData.append(np.array(data[sp[i]:ep[i]]))
#			return np.array(dividedData)
#		return wrapper
#	return _dividingData

def dividingDeviceData(dimension):
	def _dividingDeviceData(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			data = func(*args, **kwargs)
			sp, ep = args[0]._spep[1][0], args[0]._spep[1][1]
			if not kwargs:
				pass
			else:
				first_term, tolerance = kwargs["step"][0], kwargs["step"][1]
				sp, ep = sp[first_term::tolerance], ep[first_term::tolerance]
			maxlength = (ep - sp).max()
			if dimension == 3:
				if type(args[1]) == list:
					dividedData = []
					for eachdata in data:
						dividedData_ = []
						for s, e in zip(sp, ep):
							mat = np.full([maxlength,3],np.nan)
							mat[:(e-s),:] = eachdata[s:e,:]
							dividedData_.append(mat)
						dividedData.append(dividedData_)
					dividedData = np.array(dividedData)
				else:
					dividedData = []
					for s, e in zip(sp,ep):
						mat = np.full([maxlength,3],np.nan)
						mat[:(e-s),:] = data[s:e,:]
						dividedData.append(mat)
				return np.array(dividedData)
			elif dimension == 1:
				if type(args[1]) == list:
					dividedData = []
					for eachdata in data:
						dividedData_ = []
						for s, e in zip(sp, ep):
							mat = np.full(maxlength, np.nan)
							mat[:(e-s)] = eachdata[s:e]
							dividedData_.append(mat)
						dividedData.append(dividedData_)
					dividedData = np.array(dividedData)
				else:
					dividedData = []
					for s, e in zip(sp, ep):
						mat = np.full(maxlength,np.nan)
						mat[:(e-s)] = data[s:e]
						dividedData.append(mat)
					dividedData = np.array(dividedData)
				return dividedData
		return wrapper
	return _dividingDeviceData

#def dividingDeviceData(dimension):
#	def _dividingData(func):
#		@functools.wraps(func)
#		def wrapper(*args, **kwargs):
#			data = func(*args, **kwargs)
#			sp, ep = args[0]._spep[1][0], args[0]._spep[1][1]
#			if not kwargs:
#				pass
#			else:
#				first_term, tolerance = kwargs["step"][0], kwargs["step"][1]
#				sp, ep = sp[first_term::tolerance], ep[first_term::tolerance]
#			dividedData = []
#			if dimension == 3:
#				if type(args[1]) == list:
#					for i in data:
#						dividedData_ = []
#						for s,e in zip(sp, ep):
#							dividedData_.append(np.array(i[s:e,:]))
#						dividedData.append(dividedData_)
#					mat = []
#					for i in dividedData:
#						matsize_index = np.array([j.shape[0] for j in i]).argmax()
#						maxlow, maxcolumn = i[matsize_index].shape
#						mat_ = []
#						for k in i:
#							l, c = k.shape
#							mat__ = np.zeros([maxlow, maxcolumn])
#							mat__[:,:] = np.nan
#							mat__[:l, :c] = k
#							mat_.append(mat__)
#						mat.append(mat_)
#					dividedData = mat
#					del mat, mat_, mat__
#				else:
#					for i in range(len(sp)):
#						dividedData.append(np.array(data[sp[i]:ep[i],:]))
#					matsize_index = np.array([i.shape[0] for i in dividedData]).argmax()
#					maxlow, maxcolumn = dividedData[matsize_index].shape
#					mat  = []
#					for i in dividedData:
#						l, c = i.shape
#						mat_ = np.zeros([maxlow, maxcolumn])
#						mat_[:,:] = np.nan
#						mat_[:l, :c] = i
#						mat.append(mat_)
#					dividedData = mat
#					del mat, mat_
#			elif dimension == 1:
#				if type(args[1]) == list:
#					for i in data:
#						dividedData_ = []
#						for s, e in zip(sp, ep):
#							dividedData_.append(np.array(i[s:e]))
#						dividedData.append(dividedData_)
#					mat = []
#					for i in dividedData:
#						matsize_index = np.array([j.shape[0] for j in i]).argmax()
#						maxlow = i[matsize_index].shape[0]
#						mat_ = []
#						for k in i:
#							l = k.shape[0]
#							mat__ = np.zeros([maxlow])
#							mat__[:] = np.nan
#							mat__[:l] =k
#							mat_.append(mat__)
#						mat.append(mat_)
#					dividedData = np.array(mat)
#					del mat, mat_, mat__
#				else:
#					for i in range(len(sp)):
#						dividedData.append(np.array(data[sp[i]:ep[i]]))
#					matsize_index = np.array([i.shape[0] for i in dividedData]).argmax()
#					maxlow = dividedData[matsize_index].shape[0]
#					mat = []
#					for i in dividedData:
#						l = i.shape[0]
#						mat_ = np.zeros([maxlow])
#						mat_[:] = np.nan
#						mat_[:l] = i
#						mat.append(mat_)
#					dividedData = np.array(mat)
#					del mat, mat_
#			return np.array(dividedData)
#		return wrapper
#	return _dividingData


def dividingDeviceData2(dimension):
	def _dividingData(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			data = func(*args, **kwargs)
			#print(data)
			sp, ep = args[0]._spep[1][0], args[0]._spep[1][1]
			dividedData = []
			if dimension == 3:
				for i in range(len(sp)):
					dividedData.append(data[sp[i]:ep[i],:])
			elif dimension == 1:
				for i in range(len(sp)):
					dividedData.append(data[sp[i]:ep[i]])
			return dividedData
		return wrapper
	return _dividingData




