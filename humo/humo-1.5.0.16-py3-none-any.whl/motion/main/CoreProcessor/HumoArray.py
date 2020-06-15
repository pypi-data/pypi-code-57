import numpy as np
from collections import namedtuple



class HumoArray(np.ndarray):
    def __new__(cls, input_array, namelist=None, info=None):
        obj = np.asarray(input_array).view(cls)
        obj.info = info
        return obj

    def __init__(self,input_array, namelist=None):
        if input_array.ndim == 2:
            self.x  = input_array[:,0]
            self.y  = input_array[:,1]
            self.z  = input_array[:,2]
            self.xy = input_array[:,[0,1]]
            self.xz = input_array[:,[0,2]]
            self.yz = input_array[:,[1,2]]
            self.name = namelist
        elif input_array.ndim == 3:
            namelist = " ".join(namelist)
            Ntuple = namedtuple("Ntuple", namelist)
            self.x  = Ntuple(*input_array[:,:,0])
            self.y  = Ntuple(*input_array[:,:,1])
            self.z  = Ntuple(*input_array[:,:,2])
            self.xy = Ntuple(*input_array[:,:,[0,1]])
            self.xz = Ntuple(*input_array[:,:,[0,2]])
            self.yz = Ntuple(*input_array[:,:,[1,2]])
            self.name = namelist.split(" ")
            self.values = Ntuple(*input_array)
        else:
            print("An unexpected dimension data structure has been entered.")
            print("The dimension of the input data is {}".format(input_array.ndim))

class HumoArrayEMG(np.ndarray):
    def __new__(cls, input_array, namelist=None, info=None):
        obj = np.asarray(input_array).view(cls)
        obj.info = info
        return obj









