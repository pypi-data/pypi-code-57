"""
Dans_Diffraction tests
Test definition of gaussian
27/3/2020
"""

import sys,os
import numpy as np
import matplotlib.pyplot as plt # Plotting

sys.path.insert(0,r'C:\Users\dgpor\Dropbox\Python\Dans_Diffraction')
import Dans_Diffraction as dif

# Gaussian from functions_general.py
def gauss1(x, y=None, height=1, cen=0, FWHM=0.5, bkg=0):
    """
    Define Gaussian distribution in 1 or 2 dimensions
    From http://fityk.nieto.pl/model.html
        x = [1xn] array of values, defines size of gaussian in dimension 1
        y = 0 or [1xm] array of values, defines size of gaussian in dimension 2
        height = peak height
        cen = peak centre
        FWHM = peak full width at half-max
        bkg = background
    """

    if y is None:
        y = cen

    x = np.asarray(x, dtype=np.float).reshape([-1])
    y = np.asarray(y, dtype=np.float).reshape([-1])
    X, Y = np.meshgrid(x, y)
    gauss = height * np.exp(-np.log(2) * (((X - cen) ** 2 + (Y - cen) ** 2) / (FWHM / 2) ** 2)) + bkg

    if len(y) == 1:
        gauss = gauss.reshape([-1])
    return gauss

# Gaussian from Py16progs.py
def gauss2(x,height=1,cen=0,FWHM=0.5,bkg=0):
    "Define Gaussian"
    "From http://fityk.nieto.pl/model.html"
    return height*np.exp(-np.log(2)*((x-cen)/(FWHM/2))**2) + bkg

c = 100
w = 30.23
h = 35.32
x = np.arange(c-w*10, c+w*10, 0.01)
y1 = gauss1(x, y=None, height=h, cen=c, FWHM=w, bkg=0)
y2 = gauss2(x, height=h, cen=c, FWHM=w, bkg=0)

dif.fp.newplot(x, y1, label='Gauss 1')
plt.plot(x, y2, label='Gauss 2')
dif.fp.labels(None, 'x', 'y', legend=True)
plt.axhline(h/2.)
plt.axvline(c-w/2.)
plt.axvline(c+w/2.)
plt.show()