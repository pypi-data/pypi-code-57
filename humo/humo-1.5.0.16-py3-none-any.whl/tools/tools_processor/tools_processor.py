import functools
import numpy as np
from scipy import signal
import sys

def calc_vector(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        ep, sp = func(*args, **kwargs)
        try:
            vec = ep - sp
            return vec
        except TypeError:
            sys.exit("end_point2 is not set.")
    return wrapper

def calc_vecLength(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        vec = func(*args, **kwargs)
        try:
            return np.linalg.norm(vec,axis=1)
        except IndexError:
            return np.linalg.norm(vec)
    return wrapper

def calc_NormedVecotor(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        vec, Lvec = func(*args, **kwargs)
        return vec / np.array([Lvec]*3).T
    return wrapper

def calc_cross(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        v1, v2 = func(*args, **kwargs)
        return np.cross(v1, v2)
    return wrapper


def calc_angle(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        vec1,vec2, Lvec1, Lvec2 = func(*args, **kwargs)
        inner_dot = np.dot(vec1, vec2.T).diagonal()
        length_dot = Lvec1*Lvec2
        angle = np.rad2deg(np.arccos(inner_dot / length_dot))
        b, a = signal.butter(4,10*2.0/100,"low",analog=False)
        return signal.filtfilt(b,a,angle)
    return wrapper

def calc_basis_vector(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        v1, v2, v3 = func(*args, **kwargs)
        newv2 = np.cross(v3,v2)
        v = np.hstack([v1,newv2,v3])
        size = int(v.size / 9)
        return v.reshape(size,3,3,order="F")
    return wrapper



