"""Gets data from the IMF (IMF) by connecting to its API."""
import pandas
import requests
import sys

from datapungi_imf.api import *
import datapungi_imf.tests as tests

__version__ = '0.2.0'

#Default starter
#class topCall(sys.modules[__name__].__class__):
#    def __call__(self,*args,**kwargs):
#        coreClass = data()
#        return(coreClass(*args,**kwargs))
#    def __str__(self):
#        starter = "\nSample starter: \n\nimport datapungi_imf as dpf \n\ndata = dpf.data() \nprint(data) \npor just query a time series: \ndpf('gdp')"
#        return(starter)
#
#sys.modules[__name__].__class__ = topCall