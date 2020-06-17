"""
Dans_Diffraction Tests
Check speed of different methods of reading atom_properties.txt file
"""

import os, time
import numpy as np
import matplotlib.pyplot as plt
import Dans_Diffraction as dif

ATOMFILE = dif.fc.ATOMFILE

xma_file = os.path.join(dif.fc.datadir, 'XRayMassAtten_mup.dat')
xma_data = np.loadtxt(xma_file)

element_z = [43, 44, 45]
energy_keV = np.arange(1, 30, 0.01)

energies = xma_data[:, 0] / 1000.
out1 = np.zeros([len(energy_keV), len(element_z)])
out2 = np.zeros([len(energy_keV), len(element_z)])
for n, z in enumerate(element_z):
    out1[:, n] = np.interp(energy_keV, energies, xma_data[:, z])
    # Interpolating the log values is much more reliable
    out2[:, n] = np.exp(np.interp(np.log(energy_keV), np.log(energies), np.log(xma_data[:, z])))


dif.fp.newplot(energy_keV, out1, '-', lw=4)
plt.plot(energy_keV, out2, 'k-', lw=0.5)
plt.plot(energies, xma_data[:, element_z], 'o', ms=8)
plt.yscale('log')
plt.xlim([0, 30])
plt.legend(np.asarray(element_z).reshape(-1), loc=0, frameon=False, fontsize=18)
dif.fp.labels('X-Ray Attenuation', 'Energy [keV]', r'$\mu/\rho$ [cm$^2$/g]', size='big')
plt.show()
