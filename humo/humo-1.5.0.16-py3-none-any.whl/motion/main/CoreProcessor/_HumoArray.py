import numpy as np
from collections import namedtuple
import functools
from scipy.interpolate import splev, splrep

class HumoArray3D(np.ndarray):
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
            xAxisValues  = np.array([i[:,0] for i in input_array])
            yAxisValues  = np.array([i[:,1] for i in input_array])
            zAxisValues  = np.array([i[:,2] for i in input_array])
            xyAxisValues = np.array([i[:,[0,1]] for i in input_array])
            xzAxisValues = np.array([i[:,[0,2]] for i in input_array])
            yzAxisValues = np.array([i[:,[1,2]] for i in input_array])
            self.name = namelist.split(" ")
            self.values = Ntuple(*input_array)
            self.x = Ntuple(*xAxisValues)
            self.y = Ntuple(*yAxisValues)
            self.z = Ntuple(*zAxisValues)
            self.xy = Ntuple(*xyAxisValues)
            self.xz = Ntuple(*xzAxisValues)
            self.yz = Ntuple(*yzAxisValues)
        else:
            print("An unexpected data structure was entered.")

class divHumoArray3D(np.ndarray):
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
            print("An unexpected data structure was entered.")

class interHumoArray3D(np.ndarray):
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
            print("An unexpected data structure was entered.")

class normHumoArray3D(np.ndarray):
    def __new__(cls, input_array, namelist=None, info=None):
        obj = np.asarray(input_array).view(cls)
        obj.info = info
        return obj

    def __init__(self, input_array, namelist=None):
        if input_array.ndim == 3:
            self.x = np.array([i[:,0] for i in input_array])
            self.y = np.array([i[:,1] for i in input_array])
            self.z = np.array([i[:,2] for i in input_array])
            self.xy = np.array([i[:,[0,1]] for i in input_array])
            self.xz = np.array([i[:,[0,2]] for i in input_array])
            self.yz = np.array([i[:,[1,2]] for i in input_array])
            self.name = namelist

        elif input_array.ndim == 4:
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
            print("An unexpected data structure was entered.")

def convert_ndarray2HumoArray(dimension):
    def convert_ndarray2HumoArray_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            if dimension == 3:
                array = HumoArray3D(data, args[1])
                if type(args[1]) == list:
                    for name, d in zip(args[1], np.array(data)):
                        setattr(array, name, HumoArray3D(d))
                else:
                    pass
                return array
            else:
                pass
        return wrapper
    return convert_ndarray2HumoArray_


def convert_ndarray2divHumoArray(dimension):
    def convert_ndarray2divHumoArray_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            if dimension == 3:
                array = divHumoArray3D(data, args[1])
                if type(args[1]) == list:
                    for name, d in zip(args[1], data):
                        setattr(array, name, divHumoArray3D(d))
                else:
                    pass
                return array
            else:
                pass
        return wrapper
    return convert_ndarray2divHumoArray_

def convert_ndarray2interHumoArray(dimension):
    def convert_ndarray2interHumoArray_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            if dimension == 3:
                array = interHumoArray3D(data, args[1])
                if type(args[1]) == list:
                    for name, d in zip(args[1], data):
                        setattr(array, name, interHumoArray3D(d))
                else:
                    pass
                return array
            else:
                pass
        return wrapper
    return convert_ndarray2interHumoArray_

def convert_ndarray2normHumoArray(dimension):
    def convert_ndarray2normHumoArray_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            if dimension == 3:
                array = normHumoArray3D(data, args[1])
                if type(args[1]) == list:
                    for name, d in zip(args[1], data):
                        setattr(array, name, normHumoArray3D(d))
                else:
                    pass
                return array
            else:
                pass
        return wrapper
    return convert_ndarray2normHumoArray_

def convert_ndarray2HumoArrayforNoargs(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        return HumoArray3D(data)
    return wrapper

def convert_ndarray2divHumoArrayNoargs(dimension):
    def convert_ndarray2divHumoArrayNoargs_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            array = divHumoArray3D(data)
            return array
        return wrapper
    return convert_ndarray2divHumoArrayNoargs_

def convert_ndarray2interHumoArrayNoargs(dimension):
    def convert_ndarray2interHumoArrayNoargs_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            array = interHumoArray3D(data)
            return array
        return wrapper
    return convert_ndarray2interHumoArrayNoargs_

def convert_ndarray2normHumoArrayNoargs(dimension):
    def convert_ndarray2normHumoArrayNoargs_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            array = normHumoArray3D(data)
            return array
        return wrapper
    return convert_ndarray2normHumoArrayNoargs_


def convert_ndarray2HumoArrayforForcePlate(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        if type(args[1]) == list:
            names = ["plate"+str(i) for i in args[1]]
            array = HumoArray3D(data, names)
            for name, d in zip(names, np.array(data)):
                setattr(array, name, HumoArray3D(d))
            return array
        else:
            return HumoArray3D(data, "plate"+str(args[1]))
    return wrapper

def convert_ndarray2divHumoArrayforForcePlate(dimension):
    def convert_ndarray2divHumoArrayforForcePlate_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            names = ["plate"+str(i) for i in args[1]]
            array = divHumoArray3D(data, names)
            if type(args[1]) == list:
                for name, d in zip(names, np.array(data)):
                    setattr(array, name, divHumoArray3D(d, names))
                return array
            else:
                return divHumoArray3D(data, "plate"+str(args[1]))
        return wrapper
    return convert_ndarray2divHumoArrayforForcePlate_

def convert_ndarray2interHumoArrayforForcePlate(dimension):
    def convert_ndarray2interHumoArrayforForcePlate_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            names = ["plate"+str(i) for i in args[1]]
            if dimension == 3:
                array = interHumoArray3D(data, names)
                if type(args[1]) == list:
                    for name, d in zip(names, data):
                        setattr(array, name, interHumoArray3D(d))
                else:
                    pass
                return array
            else:
                pass
        return wrapper
    return convert_ndarray2interHumoArrayforForcePlate_

def convert_ndarray2normHumoArrayforForcePlate(dimension):
    def convert_ndarray2normHumoArrayforForcePlate_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            names = ["plate"+str(i) for i in args[1]]
            if dimension == 3:
                array = normHumoArray3D(data, names)
                if type(args[1]) == list:
                    for name, d in zip(names, data):
                        setattr(array, name, normHumoArray3D(d))
                else:
                    pass
                return array
            else:
                pass
        return wrapper
    return convert_ndarray2normHumoArrayforForcePlate_


# inter系メソッドのためのデコレータ
def intermethod(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data, sp, ep = func(*args, *kwargs)
        if type(args[1]) == list:
            d = []
            for i in data:
                d_ = []
                for num, j in enumerate(i):
                    d_.append(j[sp[num]:ep[num],:])
                d.append(d_)
            d = np.array(d)
        else:
            d = []
            for num, i in enumerate(data):
                d.append(i[sp[num]:ep[num],:])
            #for num, i in enumerate(data):
            #    d.append(i[sp[num]:ep[num],:])
            d = np.array(d)
        return d
    return wrapper

# normalize処理のためのデコレータ
def normalize(data, length):
    x = np.arange(0, len(data[:,0]))
    x_inter = np.linspace(0,x[-1], length)
    y_inter = []
    for i in range(3):
        y = data[:,i]
        tck = splrep(x,y)
        y_inter.append(splev(x_inter, tck))
    return np.array(y_inter).T

# norm系メソッドのためのデコレータ
def normmethod(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data, length = func(*args, **kwargs)
        if type(args[1]) == list:
            d = []
            for i in data:
                d_ = []
                for j in i:
                    d_.append(normalize(j, length))
                d.append(d_)
            d = np.array(d)
        else:
            d = []
            for i in data:
                d.append(normalize(i,length))
            d = np.array(d)
        return d
    return wrapper

