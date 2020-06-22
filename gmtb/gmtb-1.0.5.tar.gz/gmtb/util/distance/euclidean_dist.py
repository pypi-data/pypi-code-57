import numpy as np


def euclidean_dist(x, y):
    return np.sqrt(np.sum(np.power(x-y, 2)))


def euclidean_wm(x,y,alpha):
    return alpha * x + (1-alpha) * y