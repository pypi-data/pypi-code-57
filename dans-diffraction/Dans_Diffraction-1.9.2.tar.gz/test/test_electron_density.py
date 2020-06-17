"""
Calculate electron density using formular:
14.14 p113
http://jp-minerals.org/vesta/archives/VESTA_Manual.pdf
13/May/2020
"""

import os, time
import numpy as np
import Dans_Diffraction as dif
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import interp2d

xtl = dif.structure_list.Ca2RuO4()

# Resolution = maximum resolution of the structure factor
resolution = 0.4

volume = xtl.Cell.volume()

w = 0.  # fractional position along c-axis
grid_spacing = 0.5 * resolution / xtl.Cell.a  # grid_spacing = resolution/2
grid = np.arange(-grid_spacing, 1+2*grid_spacing, grid_spacing)
#grid = np.linspace(0, 1, np.ceil(1/grid_spacing))
grid_u, grid_v, grid_w = np.meshgrid(grid, grid, w)
uvw = np.array([grid_u.ravel(), grid_v.ravel(), grid_w.ravel()]).T
xyz = xtl.Cell.calculateR(uvw)
grid_x = np.reshape(xyz[:, 0], grid_u.shape)
grid_y = np.reshape(xyz[:, 1], grid_u.shape)
grid_z = np.reshape(xyz[:, 2], grid_u.shape)



# Calcualte Structure-Factors
all_hkl = xtl.Cell.all_hkl(dif.fc.resolution2energy(resolution))
xtl.Scatter._return_structure_factor=True

n_arrays = np.ceil(len(all_hkl)*len(uvw)/100000.)
hkl_array = np.array_split(all_hkl, n_arrays)

density = np.zeros(len(uvw), dtype=np.complex)
for _hkl in hkl_array:
    sf = xtl.Scatter.intensity(_hkl)
    density += np.sum(sf * np.exp(1j * 2 * np.pi * np.dot(uvw, _hkl.T)), axis=1)
density = np.reshape(density, grid_u.shape)
density = density[:, :, 0] / volume
density = np.sqrt(np.real(density * np.conj(density)))
"""
density = np.zeros(grid_u.shape)
for n in range(len(grid)):
    for m in range(len(grid)):
        uvw = np.array([grid_u[n, m], grid_v[n, m], w])
        density[n, m] = np.sum(sf*np.exp(1j*2*np.pi*np.dot(all_hkl, uvw)))
density = density/volume
"""

grid_x = grid_x[:, :, 0]# - resolution / 4
grid_y = grid_y[:, :, 0]# - resolution / 4

# Interpolate data
igrid = np.arange(-grid_spacing, 1+2*grid_spacing, grid_spacing/10.)
igrid_u, igrid_v, igrid_w = np.meshgrid(igrid, igrid, w)
iuvw = np.array([igrid_u.ravel(), igrid_v.ravel(), igrid_w.ravel()]).T
ixyz = xtl.Cell.calculateR(iuvw)
igrid_x = np.reshape(ixyz[:, 0], igrid_u.shape)
igrid_y = np.reshape(ixyz[:, 1], igrid_u.shape)
igrid_z = np.reshape(ixyz[:, 2], igrid_u.shape)
f = interp2d(grid_u[:, :, 0], grid_v[:, :, 0], density, kind='linear')
idensity = f(igrid, igrid)


plt.figure(figsize=[12, 10], dpi=100)
plt.pcolormesh(grid_x, grid_y, density, shading='gouraud')
plt.colorbar()
plt.clim([0, 30])
plt.axis('image')
dif.fp.labels('%s, w=%s' % (xtl.name, w), 'x || a [Å]', 'y || b [Å]')

plt.figure(figsize=[12, 10], dpi=100)
plt.pcolormesh(igrid_x[:, :, 0], igrid_y[:, :, 0], idensity)
plt.colorbar()
plt.clim([0, 30])
plt.axis('image')
dif.fp.labels('%s, w=%s' % (xtl.name, w), 'x || a [Å]', 'y || b [Å]')
plt.show()