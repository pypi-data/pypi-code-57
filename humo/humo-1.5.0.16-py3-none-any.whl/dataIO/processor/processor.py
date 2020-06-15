import os
import sys
import json
import functools


def SSP_Path(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		cwd = os.getcwd()
		filepath = os.path.dirname(os.path.abspath(__file__))
		os.chdir(filepath)
		os.chdir("../../motion/settings/SSP")
		func(*args, **kwargs)
		os.chdir(cwd)
	return wrapper

def getSSP(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		cwd = os.getcwd()
		filepath = os.path.dirname(os.path.abspath(__file__))
		os.chdir(filepath)
		os.chdir("../../motion/settings/SSP")
		return func(*args, **kwargs)
		os.chdir(cwd)
	return wrapper


def ASP_Path(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		cwd = os.getcwd()
		filepath = os.path.dirname(os.path.abspath(__file__))
		os.chdir(filepath)
		os.chdir("../../motion/settings/ASP")
		func(*args, **kwargs)
		os.chdir(cwd)
	return wrapper

def getASP(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		cwd = os.getcwd()
		filepath = os.path.dirname(os.path.abspath(__file__))
		os.chdir(filepath)
		os.chdir("../../motion/settings/ASP")
		return func(*args, **kwargs)
		os.chdir(cwd)
	return wrapper

def data_path(func):
	functools.wraps(func)
	def wrapper(*args, **kwargs):
		#cwd = os.getcwd()
		filepath = os.path.dirname(os.path.abspath(__file__))
		#os.chdir(filepath)
		#os.chdir("../../_MeasurementData{}".format(args[1]))
		#return func(*args, **kwargs)
		#os.chdir(cwd)
		return filepath
	return wrapper
