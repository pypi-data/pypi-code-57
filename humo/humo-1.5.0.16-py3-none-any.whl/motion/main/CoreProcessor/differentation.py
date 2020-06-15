import functools

import numpy as np
from scipy import fftpack, signal
from scipy.interpolate import splev, splrep


"""
This is a wrapper for performing differential calculations.
The wrapper accepts self and column names,
and outputs the first-order and second-order differentiated data.

When first-order and second-order differentiation, pass 1 or 2 to the difforder in the wrapper.
"""
def differentation(difforder):
    def differentation_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            if args[0].cfg:
                filtMod = args[0].cfg["diff_filter"]
            else:
                filtMod= ["True", 4, 6, "msec"]
            b,a = signal.butter(filtMod[1], filtMod[2]/50.0, "low", analog=False)
            if difforder == "1st":
                if data.ndim == 2:
                    data = (data[2:,:] - data[:-2,:]) / 0.01*2
                    if filtMod[0] == "True":
                        data = signal.filtfilt(b, a, data, axis=0)
                    else:
                        pass
                elif data.ndim == 3:
                    data = (data[:,2:,:] - data[:,:-2,:]) / 0.01*2
                    if filtMod[0] == "True":
                        data = signal.filtfilt(b, a, data, axis=1)
                    else:
                        pass
                else:
                    print("an expected ndim.")
            elif difforder == "2nd":
                if data.ndim == 2:
                    data = (data[2:] - data[1:-1]*2 + data[:-2]) / 0.01**2
                    if filtMod[0] == "Ture":
                        data = signal.filtfilt(b, a, data, axis=0)
                    else:
                        pass
                elif data.ndim == 3:
                    data = (data[:,2:,:] - data[:,1:-1,:] + data[:,:-2,:]) / 0.01**2
                    if filtMod[0] == "True":
                        data = signal.filtfilt(b, a, data, axis=1)
                    else:
                        pass
            if filtMod[3] == "msec":
                return np.array(data) / 10000.0
            else:
                return np.array(data)
        return wrapper
    return differentation_


#def differentation(difforder):
#    def differentation_(func):
#        @functools.wraps(func)
#        def wrapper(*args, **kwargs):
#            data = func(*args, **kwargs)
#            if args[0].cfg:
#                filtMod = args[0].cfg["diff_filter"]
#            else:
#                filtMod = ["True", 4, 6, "msec"]
#            if difforder == "1st":
#                if filtMod[0] == "True":
#                    if data.ndim == 2:
#                        b,a = signal.butter(filtMod[1],filtMod[2]/50.0,"low",analog=False)
#                        data_ = (data[2:] - data[:-2]) / 0.01*2
#                        data_diff = []
#                        for i in data:
#                            data_diff.append(np.array([signal.filtfilt(b,a,data_[:,axis]) for axis in tuple(np.arange(3))]).T)
#                    else:
#                        data_diff = (data[2:] - data[:-2]) / 0.01*2
#                        b,a = signal.butter(filtMod[1],filtMod[2]/50.0,"low",analog=False)
#                        data_diff = np.array([signal.filtfilt(b,a,data_diff[:,axis]) for axis in tuple(np.arange(3))]).T
#                elif filtMod[0] == "False":
#                    if data.ndim == 2:
#                        data_diff = []
#                        for i in data:
#                            data_diff.append((i[2:] - i[:-2]) / 0.01*2)
#                    else:
#                        data_diff = (i[2:] - i[:-2]) / 0.01*2
#            elif difforder == "2nd":
#                if filtMod[0] == "True":
#                    if data.ndim == 2:
#                        b,a = signal.butter(filtMod[1],filtMod[2]/50.0,"low",analog=False)
#                        data_diff = []
#                        for i in data:
#                            data_ = (i[2:] - i[1:-1]*2 + i[:-2]) / 0.01**2
#                            data_diff.append(np.array([signal.filtfilt(b,a,data_[:,axis]) for axis in tuple(np.arange(3))]).T)
#                    else:
#                        data_diff = (data[2:] - data[1:-1]*2 + data[:-2]) / 0.01**2
#                        b,a = signal.butter(filtMod[1],filtMod[2]/50.0,"low",analog=False)
#                        data_diff = np.array([signal.filtfilt(b,a,data_diff[:,axis]) for axis in tuple(np.arange(3))]).T
#                elif filtMod[0] == "False":
#                    if data.ndim == 2:
#                        data_diff = []
#                        for i in data:
#                            data_diff((i[2:] - i[1:-1]*2 + i[:-2]) / 0.01**2)
#                    else:
#                        data_diff = (data[2:] - data[1:-1]*2 + data[:-2]) / 0.01**2
#            if filtMod[3] == "msec":
#                return np.array(data_diff) / 10000.0
#            elif filtMod == "sec":
#                return np.array(data_diff)
#        return wrapper
#    return differentation_
