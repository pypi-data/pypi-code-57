"""
Dans_Diffraction tests
Test non-resonant x-ray scattering
"""

import sys,os
import numpy as np
import matplotlib.pyplot as plt # Plotting
import Dans_Diffraction as dif
from mpl_toolkits.mplot3d import Axes3D

xtl = dif.structure_list.Ca2RuO4.build()
xtl.Atoms.changeatom(1, mxmymz=[0, 3, 1])
xtl.generate_structure()

xtl.Scatter._use_magnetic_form_factor = False
hkl = [1,0,3]
energy_kev = 2.967
azim_zero = [0,1,0]
pol = 'sp'
psi = 0
psirange = np.arange(-180,181,1)
a,b,c = xtl.Cell.UV()
moment = dif.fg.norm(xtl.Cell.calculateR(xtl.Structure.mxmymz()[8:12]))
#moment = xtl.Structure.mxmymz()[8:12]
print(moment)
print(xtl.scale)
uvw = xtl.Structure.uvw()[8:12]



def splane(hkl, energy_kev, azim_zero, psi, pol):
    U1, U2, U3 = xtl.Scatter.scatteringbasis(hkl, azim_zero, psi)
    kin, kout, ein, eout = xtl.Scatter.scatteringvectors(hkl, energy_kev, azim_zero, psi, pol)
    return U1, U2, U3, kin, kout, ein, eout

# (1,0,3)
beta = np.abs(dif.fg.ang(xtl.Cell.calculateQ(hkl), [0,0,1]))
# Converstion between lab frame to xtl frame (for (1,0,3) only)
U = np.array([[0, -np.cos(beta), np.sin(beta)], [1, 0, 0], [0, np.sin(beta), np.cos(beta)]])
brag = np.deg2rad(xtl.Cell.tth(hkl, energy_kev))[0]/2

def calfmag(psi):
    azim = np.deg2rad(psi)

    # From paper:
    es = np.array([np.sin(azim), np.cos(azim), 0])
    ep = np.array([-np.sin(brag) * np.cos(azim), np.sin(brag) * np.sin(azim), np.cos(brag)])
    # corrected in test_nonresonant_plot.py
    #es = np.array([-np.sin(azim), np.cos(azim), 0])
    #ep = np.array([-np.sin(brag) * np.cos(azim), -np.sin(brag) * np.sin(azim), np.cos(brag)])

    crys_es = np.dot(es, U.T)
    crys_ep = np.dot(ep, U.T)

    phase = np.exp(1j * 2 * np.pi * np.dot(hkl, uvw.T))
    crosprod = np.cross(crys_ep, crys_es)
    phasemom = np.sum(phase.reshape([-1,1])*moment, axis=0)
    fmag = np.dot(crosprod, phasemom)/4.0
    fmag = np.real(fmag * np.conj(fmag))
    return fmag

def calfmag2(psi):
    azim = np.deg2rad(psi)
    # From paper:
    es = np.array([np.sin(azim), np.cos(azim), 0])
    ep = np.array([-np.sin(brag)*np.cos(azim), np.sin(brag)*np.sin(azim), np.cos(brag)])
    # corrected in test_nonresonant_plot.py
    #es = np.array([-np.sin(azim), np.cos(azim), 0])
    #ep = np.array([-np.sin(brag) * np.cos(azim), -np.sin(brag) * np.sin(azim), np.cos(brag)])

    crys_es = np.dot(es, U.T)
    crys_ep = np.dot(ep, U.T)

    fmag = crys_es[0]*crys_ep[1] - crys_es[1]*crys_ep[0]
    return fmag

sqI = np.array([xtl.Scatter.xray_resonant_magnetic([1,0,3], energy_kev, [0,1,0], psival, 'sp') for psival in psirange])
fmag = np.array([calfmag(psi) for psi in psirange])
fmag2 = np.array([calfmag2(psi) for psi in psirange])
fmag3 = np.array(0.535 - 0.44*np.sin(np.deg2rad(psirange)))


plt.figure()
plt.plot(psirange, sqI, label='Dan')
plt.plot(psirange, fmag, label='phase')
plt.plot(psirange, fmag2**2, label='cross prod')
plt.plot(psirange, fmag3**2, label='Sergio')
plt.legend(loc=0, frameon=False)
plt.show()


print('finished')