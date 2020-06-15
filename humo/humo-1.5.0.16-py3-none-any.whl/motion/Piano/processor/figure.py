import numpy as np
import functools
import matplotlib.pylab as plt

def key_onset_figure(func):
    functools.wraps(func)
    def wrapper(*args, **kwargs):
        key1, key2,threshold1, threshold2 = func(*args, **kwargs)
        sps, eps = np.where(key1[:,2] > threshold1, 0, 1), np.where(key2[:,2] > threshold2, 0, 1)
        sps, eps = np.diff(sps), np.diff(eps)
        plt.plot(sps,alpha=0.5,label="start key")
        plt.plot(eps,alpha=0.5,color="r",label="end key")
        plt.axhline(0,color="k",alpha=0.7)
        plt.title("key stroke and key release timing",fontsize=15)
        plt.ylabel("negative:release, positive:stroke",fontsize=15)
        plt.xlabel("Time[100Hz]",fontsize=15)
        plt.legend(fontsize=12)
    return wrapper


