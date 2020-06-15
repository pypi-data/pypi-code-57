import numpy as np
from collections import namedtuple



class interHumoArray(np.ndarray):
    def __new__(cls, input_array, namelist=None, info=None):
        obj = np.asarray(input_array).view(cls)
        obj.info = info
        return obj

    def __init__(self, input_array, namelist=None):
        if input_array.ndim == 1:
            self.x = np.array([i[:,0] for i in input_array])
            self.y = np.array([i[:,1] for i in input_array])
            self.z = np.array([i[:,2] for i in input_array])
            self.xy = np.array([i[:,[0,1]] for i in input_array])
            self.xz = np.array([i[:,[0,2]] for i in input_array])
            self.yz = np.array([i[:,[1,2]] for i in input_array])
            self.name = namelist

        elif input_array.ndim == 2:
            namelist = " ".join(namelist)
            Ntuple = namedtuple("Ntuple", namelist)
            xAxisValues = np.array([[i[:,0] for i in d] for d in input_array])
            yAxisValues = np.array([[i[:,1] for i in d] for d in input_array])
            zAxisValues = np.array([[i[:,2] for i in d] for d in input_array])
            xyAxisValues = np.array([[i[:,[0,1]] for i in d] for d in input_array])
            xzAxisValues = np.array([[i[:,[0,2]] for i in d] for d in input_array])
            yzAxisValues = np.array([[i[:,[1,2]] for i in d] for d in input_array])
            self.x = Ntuple(*xAxisValues)
            self.y = Ntuple(*yAxisValues)
            self.z = Ntuple(*zAxisValues)
            self.xy = Ntuple(*xyAxisValues)
            self.xz = Ntuple(*xzAxisValues)
            self.yz = Ntuple(*yzAxisValues)
            self.name = namelist.split(" ")
        else:
            print("An unexpected dimension data structure has been entered.")
            print("The dimension of the input data is {}".format(input_array.ndim))


class interHumoArrayEMG(np.ndarray):
    def __new__(cls, input_array, namelist=None, info=None):
        obj = np.asarray(input_array).view(cls)
        obj.info = info
        return obj