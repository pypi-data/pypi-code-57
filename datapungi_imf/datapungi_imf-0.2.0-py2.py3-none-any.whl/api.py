import pandas as pd
import requests
import sys
from datapungi_imf import generalSettings 
from datapungi_imf import drivers
from datapungi_imf.driverCore import driverCore
#from driverCore import driverCore
#import drivers

#TODO: test clipcode, utils (setting folder, options), getting help in each step.
class data():
    '''
       Connect to IMF databases. To start, choose a database group from:

       - list: list of all IMF databases (IMF name DataFlow)
       - params: given a database, get the parameters (IMF name DataStructure)
       - data: given database name and paraameter, returns data (IMF name CompactData)
       - 
       - 
       - 

       For example:
       import datapungi_imf as dpi
       data = dpi.data()
       data.list()
    '''
    def __init__(self,connectionParameters = {}, userSettings = {}):
        self.__connectInfo = generalSettings.getGeneralSettings(connectionParameters = connectionParameters, userSettings = userSettings ) 
        self._metadata = self.__connectInfo.packageMetadata
        self._help     = self.__connectInfo.datasourceOverview
        #load drivers:
        loadInfo = {'baseRequest' : self.__connectInfo.baseRequest, 'connectionParameters' : self.__connectInfo.connectionParameters}
        
        #specific drivers
        self.datasetlist  = drivers.datasetlist(**loadInfo)
        
        #core drivers
        coreDriversParams = driverCore()
        for dbGroupName in [x['group'] for x in coreDriversParams._dbParams]:
            setattr(self, dbGroupName.lower(), driverCore(dbGroupName,**loadInfo))
             
    def __call__(self,*args,**kwargs):
        return(self.series(*args,**kwargs))

    def __str__(self):
        return(self.__doc__)

    def _clipcode(self):
        try:
            self._lastCalledDriver.clipcode()
        except:
            print('Get data using a driver first, eg: ')
            #eg: data.NIPA("T10101", verbose = True)
    

if __name__ == '__main__':            
    d = data()
    d.list()
    