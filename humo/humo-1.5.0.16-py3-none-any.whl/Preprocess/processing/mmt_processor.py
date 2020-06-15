import functools
from scipy import signal
import numpy as np



def filtEMG(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        order, fq1, fq2 = 4, 20.0, 480.0
        b,a = signal.butter(order,[fq1*2.0/1000,fq2*2.0/1000],"band",analog=False)
        return signal.filtfilt(b,a,args[0].emg)
    return wrapper

def takeAbsValues(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return np.abs(func(*args, **kwargs))
    return wrapper

def smoothingEMG(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        order, fq3 = 4, 10.0
        b, a = signal.butter(order,fq3*2.0/1000,"low",analog=False)
        return signal.filtfilt(b, a, data)
    return wrapper


def calcMVCvalue(ratio_min, ratio_max):
    def calcMVCvalue_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            #sortedEMG = np.sort(data)[::-1]
            #cutoff = int(data.size * ratio)
            mvc = data[(data < data.max()*ratio_max) & (data > data.max()*ratio_min)].mean()
            return mvc
        return wrapper
    return calcMVCvalue_

def calcMVCvalue2(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        return data.max()
    return wrapper



