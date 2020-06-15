#-*- coding:utf-8 -*-

"""
	desc: |	
"""


import clr
import sys
from types import *
import os
import ctypes


class EvtExchanger:

	"""
	desc: |
	"""
	EE=None
	@staticmethod
	def Initialise():

		directory = os.path.dirname(__file__)

		try:
			sys.path.insert(0, directory)
			dllname = directory +'\\EventExchanger.dll'
			clr.FindAssembly(dllname)
			clr.AddReference("EventExchanger")
			from ID import EventExchangerLister
            
		except Exception as e:
			raise Exception('EventExchanger (Lib) Initialisation Error')

		try:
			EvtExchanger.EE = EventExchangerLister
			
		except Exception as e:
			raise Exception('EventExchanger Device Error')
		
	@staticmethod
	def Device():
		return EvtExchanger.EE
		
