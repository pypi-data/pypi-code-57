import os
import glob
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from skimage.external import tifffile
from scipy.optimize import curve_fit


def logistics(x, a, x0, k):
    return 1 - (a / (1 + np.exp(-k * (x - x0))))


def plot_history(history):
    fig = plt.plot(history['loss'], label='training loss')
    plt.plot(history['val_loss'], label='validation loss')
    x_vals = np.array(range(1, len(history['loss']) + 1))
    try:
        (res, _) = curve_fit(logistics, x_vals, history['val_loss'])
        plt.plot(logistics(x_vals, res[0], res[1],
                           res[2]), label='logistics fit')
        title = 'extrapolated loss: {0:.2f}, learning affinity: {2:.3f}, offset: {1:.0f}'.format(
            1 - res[0], res[1], res[2])
    except RuntimeError:
        title = 'unable to fit logistics function to validation loss'
    plt.legend()
    plt.xlabel('training epoch')
    plt.ylabel('dice loss')
    plt.ylim((0, 1))
    plt.title(title)
    return fig


class Timer(object):

    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        if self.name:
            print('[%s]' % self.name,)
        print('Elapsed: %s' % (time.time() - self.tstart))
