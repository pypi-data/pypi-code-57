import functools
import numpy as np
from scipy.interpolate import splev, splrep

def normalizingData(dimension):
    def _normalizingData(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data, length = func(*args, **kwargs)
            # args[2] : axis
            ndata = []
            for i in range(data.size):
                x = np.arange(0,len(data[i]))
                if dimension == 3:
                    y = data[i][:,args[2]]
                elif dimension == 1:
                    y = data[i]
                tck = splrep(x,y)
                x_inter = np.linspace(0,x[-1],length)
                y_inter = splev(x_inter, tck)
                ndata.append(y_inter)
            return np.array(ndata)
        return wrapper
    return _normalizingData

def upsampling(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data, size = func(*args, **kwargs)
        x = np.arange(0,data[:,0].size)
        upsampling_data = []
        for i in range(3):
            y = data[:,i]
            tck = splrep(x,y)
            x_inter = np.linspace(0,x[-1],size)
            upsampling_data.append(splev(x_inter, tck))
        return np.array(upsampling_data).T
    return wrapper

def normalizing_point(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        p, sp, ep, num_type = func(*args, **kwargs)
        length = ep - sp - 1
        if num_type == "int":
            return np.array(p*100 / length).astype("int")
        else:
            return np.array(p*100 / length)
    return wrapper


def normalizingData2(dimension):
    def _normalizingData(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data, length, ep = func(*args, **kwargs)
            p = np.array(args[0].get_all_point(100)).T
            # args[2] : axis
            ndata = []
            for i in range(data.size):
                if dimension == 3:
                    x = np.arange(0,p[i][ep])
                    y = data[i][:p[i][ep],args[2]]
                elif dimension == 1:
                    x = np.arange(0,p[i][ep]*10)
                    y = data[i][:p[i][ep]*10]
                tck = splrep(x,y)
                x_inter = np.linspace(0,x[-1],length)
                y_inter = splev(x_inter, tck)
                ndata.append(y_inter)
            return np.array(ndata)
        return wrapper
    return _normalizingData