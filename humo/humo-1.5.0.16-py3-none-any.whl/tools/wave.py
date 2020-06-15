import functools
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splev, splrep
from scipy import signal
from scipy import fftpack
from scipy import integrate



def FFT2fig(data,sampling_rate,labeling=True):
    fft_data = fftpack.fft(data) / len(data)
    freq = fftpack.fftfreq(len(data),1/sampling_rate)
    if labeling == True:
        plt.plot(freq[1:int(len(data)/2)],np.abs(fft_data[1:int(len(data)/2)]),alpha=0.8)
        plt.title("Result of Fast Fourier Transform (FFT)",fontsize=15)
        plt.ylabel("Amplitude",fontsize=10)
        plt.xlabel("Frequency",fontsize=10)
    elif labeling == False:
        plt.plot(freq[1:int(len(data)/2)],np.abs(fft_data[1:int(len(data)/2)]),alpha=0.8)
    #sig = np.abs(fft_data[1:int(len(data)/2)])
    #if sampling_rate == 100:
    #    plt.text(40, sig.max()*0.8,"Max amplitude  : {} \nPeak frequency : {}".format(round(sig.max(),1),sig.argmax()))
    #elif sampling_rate == 1000:
    #    plt.text(400, sig.max()*0.8,"Max amplitude  : {} \nPeak frequency : {}".format(round(sig.max(),1),sig.argmax()))


def integrate_simps(divided):
    def integrate_simps_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if divided == False:
                data = func(*args, **kwargs)
                return integrate.simps(data,np.arange(len(data)))
            else:
                data = func(*args, **kwargs)
                result_simps = []
                for i in data:
                    result_simps.append(integrate.simps(i,np.arange(len(i))))
                return result_simps
        return wrapper
    return integrate_simps_

def simps(data):
    if type(data) == list:
        result_simps = []
        for i in data:
            result_simps.append(integrate.simps(i,np.arange(len(i))))
        return result_simps
    else:
        return integrate.simps(data,np.arange(len(data)))

def filt(order, freq):
    def filt_(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            b,a = signal.butter(order,freq/50.0,"low",analog=False)
            if data[0].size == 3:
                fdata = np.array([signal.filtfilt(b,a,data[:,axis]) for axis in tuple(np.arange(3))]).T
                return fdata
            else:
                fdata = signal.filtfilt(b,a,data)
                return fdata
        return wrapper
    return filt_

