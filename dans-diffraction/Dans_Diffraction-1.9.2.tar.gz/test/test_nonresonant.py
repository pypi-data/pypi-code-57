"""
Dans_Diffraction tests
Test non-resonant x-ray scattering
"""

import sys,os
import numpy as np
import matplotlib.pyplot as plt # Plotting
sys.path.insert(0,'C:\Users\dgpor\Dropbox\Python\Dans_Diffraction')
import Dans_Diffraction as dif

xtl = dif.structure_list.Ca2RuO4.build()
xtl.Atoms.changeatom(1,mxmymz=[0, 3, 1])
xtl.generate_structure()

xtl.Scatter._use_magnetic_form_factor = False
hkl = [[1,0,0], [0,1,3], [1,0,3], [0,0,3], [2,0,0]]
hkl = [0,1,3]
psi = np.arange(-180,181,1)

# Non resonant magnetic scattering
out1 = xtl.Scatter.xray_nonresonant_magnetic(hkl, 3, [0,1,0], 0, 'sp')
out2 = xtl.Scatter.xray_nonresonant_magnetic(hkl, 3, [0,1,0], 90, 'sp')

for h,i,ii in zip(hkl, out1, out2):
    print(h, i, ii)

val1 = np.array([xtl.Scatter.xray_nonresonant_magnetic([0,1,3], 3, [0,1,0], psival, 'sp') for psival in psi])
val2 = np.array([xtl.Scatter.xray_nonresonant_magnetic([1,0,3], 3, [0,1,0], psival, 'sp') for psival in psi])
val3 = np.array([xtl.Scatter.xray_nonresonant_magnetic([1,0,0], 3, [0,1,0], psival, 'sp') for psival in psi])

plt.figure()
plt.plot(psi, val1/val1.max(), '-', lw=2, label='(0,1,3)')
plt.plot(psi, val2/val2.max(), '-', lw=2, label='(1,0,3)')
plt.plot(psi, val3/val3.max(), '-', lw=2, label='(1,0,0)')
plt.legend(loc=0, frameon=False)
dif.fp.labels('non-resonant', 'psi [Deg]', 'Intensity')

# resonant magnetic scattering
out1 = xtl.Scatter.xray_resonant_magnetic(hkl, 2.838, [0,1,0], 0, 'sp')
out2 = xtl.Scatter.xray_resonant_magnetic(hkl, 2.838, [0,1,0], 90, 'sp')
out3 = xtl.Scatter.xray_resonant_magnetic(hkl, 2.838, [0,1,0], 180, 'sp')

for h,i,ii in zip(hkl, out1, out2):
    print(h, i, ii)

val1 = np.array([xtl.Scatter.xray_resonant_magnetic([0,1,3], 2.838, [0,1,0], psival, 'sp', F0=0, F1=1, F2=0) for psival in psi])
val2 = np.array([xtl.Scatter.xray_resonant_magnetic([1,0,3], 2.838, [0,1,0], psival, 'sp', F0=0, F1=1, F2=0) for psival in psi])
val3 = np.array([xtl.Scatter.xray_resonant_magnetic([1,0,0], 2.838, [0,1,0], psival, 'sp', F0=0, F1=1, F2=0) for psival in psi])

plt.figure()
plt.plot(psi, val1/val1.max(), '-', lw=2, label='(0,1,3)')
plt.plot(psi, val2/val2.max(), '-', lw=2, label='(1,0,3)')
plt.plot(psi, val3/val3.max(), '-', lw=2, label='(1,0,0)')
plt.legend(loc=0, frameon=False)
dif.fp.labels('resonant new', 'psi [Deg]', 'Intensity')

# Old resonant method
out1 = xtl.Scatter.xray_resonant(hkl, energy_kev=2.838, polarisation='sp', F0=0, F1=1, F2=0, azim_zero=[0,1,0], PSI=0)
out2 = xtl.Scatter.xray_resonant(hkl, energy_kev=2.838, polarisation='sp', F0=0, F1=1, F2=0, azim_zero=[0,1,0], PSI=90)

for h,i,ii in zip(hkl, out1, out2):
    print(h, i, ii)

val1= np.array([xtl.Scatter.xray_resonant([0,1,3], energy_kev=2.838, polarisation='sp',F0=0,F1=1,F2=0,azim_zero=[0,1,0],PSI=psival)[0,0] for psival in psi])
val2= np.array([xtl.Scatter.xray_resonant([1,0,3], energy_kev=2.838, polarisation='sp',F0=0,F1=1,F2=0,azim_zero=[0,1,0],PSI=psival)[0,0] for psival in psi])
val3= np.array([xtl.Scatter.xray_resonant([1,0,0], energy_kev=2.838, polarisation='sp',F0=0,F1=1,F2=0,azim_zero=[0,1,0],PSI=psival)[0,0] for psival in psi])

plt.figure()
plt.plot(psi, val1/val1.max(), '-', lw=2, label='(0,1,3)')
plt.plot(psi, val2/val2.max(), '-', lw=2, label='(1,0,3)')
plt.plot(psi, val3/val3.max(), '-', lw=2, label='(1,0,0)')
plt.legend(loc=0, frameon=False)
dif.fp.labels('resonant old', 'psi [Deg]', 'Intensity')


plt.figure()
mb013 = (0.37 + 0.62*np.cos(np.deg2rad(psi)))**2
mb100 = (np.cos(np.deg2rad(psi)))**2
mc103 = (0.535 - 0.44*np.sin(np.deg2rad(psi)))**2
plt.plot(psi, mb013, '-', lw=2, label='mb (013)')
plt.plot(psi, mc103, '-', lw=2, label='mc (103)')
plt.plot(psi, mb100, '-', lw=2, label='mb (100)')
plt.legend(loc=0, frameon=False)
dif.fp.labels('Sergio', 'psi [Deg]', 'Intensity')
plt.show()