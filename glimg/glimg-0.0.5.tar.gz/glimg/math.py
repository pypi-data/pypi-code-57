import math as m
import numpy as np

#------------------- triangle -------------------#
def angle(rad):
    return rad/np.pi*180.

def rad(angle):
    return angle/180.*np.pi

def cos(angle):
    rad = rad(angle)
    return m.cos(rad)

def sin(angle):
    rad = rad(angle)
    return m.sin(rad)

def tan(angle):
    rad = rad(angle)
    return m.tan(rad)

def acos(val):
    rad = m.acos(val)
    return angle(rad)

def asin(val):
    rad = m.asin(val)
    return angle(rad)

def atan(val):
    rad = m.atan(val)
    return angle(rad)