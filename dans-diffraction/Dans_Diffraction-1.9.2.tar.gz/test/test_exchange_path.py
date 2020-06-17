"""
Calculate exchange path between Ru ions in Ca2RuO4
13/May/2020
"""

import os, time
import numpy as np
import Dans_Diffraction as dif
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

xtl = dif.structure_list.Ca2RuO4()


cen_idx = 11
nearest_neighbor_distance = 6.6
exchange_type = 'O'

cen_uvw = xtl.Structure.uvw()[cen_idx, :]
cen_xyz = xtl.Cell.calculateR(cen_uvw)
cen_type = xtl.Structure.type[cen_idx]

# Generate lattice of muliple cells to remove cell boundary problem
uvw, type, label, occ, uiso, mxmymz = xtl.Structure.generate_lattice(1, 1, 1)
xyz = xtl.Cell.calculateR(uvw)
all_bonds = cen_xyz - xyz

# Exchange type
#exchange_type = 1  # all atoms
exchange_allowed = type == exchange_type

# Inside unit cell
incell = np.all((uvw>=0)*(uvw<=1), axis=1)

# Bond distances
mag = dif.fg.mag(all_bonds)
neighbor_idx = np.where(incell*(type == cen_type)*(mag < nearest_neighbor_distance)*(mag > 0.01))[0]

# Sort order by distance to central atom
srt_idx = np.argsort(mag[neighbor_idx])
neighbor_idx = neighbor_idx[srt_idx]

# Goup distances
group_val, array_index, group_index, group_count = dif.fg.group(mag[neighbor_idx])
neighbor_idx = neighbor_idx[group_index]

exchange_paths = []
exchange_distances = []
for nidx in neighbor_idx:
    n_xyz = xyz[nidx, :]
    n_uvw = uvw[nidx, :]
    n_type = label[nidx]
    n_dist = mag[nidx]
    print('\n%3d %4s (%6.2f,%6.2f,%6.2f)' % (nidx, n_type, n_uvw[0], n_uvw[1], n_uvw[2]))
    print(' %s-%s distance: %5.3f A' % (cen_type, n_type, n_dist))
    # Distance to average position
    av_pos = (cen_xyz + n_xyz) / 2
    av_dis = dif.fg.mag(av_pos - cen_xyz) * 1.1
    av_dis_idx = dif.fg.mag(av_pos - xyz) < av_dis
    print(' %d ions < %5.2f A to bond' % (sum(av_dis_idx), av_dis))

    # Distace from Ru1
    dist1_idx = (mag > 0.01)*(mag < av_dis)
    print(' %d ions < %5.2f A to Ru1' % (sum(dist1_idx), av_dis))

    # Distance from Ru2
    all_bonds2 = n_xyz - xyz
    mag2 = dif.fg.mag(all_bonds2)
    dist2_idx = (mag2 > 0.01)*(mag2 < av_dis)
    print(' %d ions < %5.2f A to Ru2' % (sum(dist2_idx), av_dis))

    # bond angle from ru1
    bond = cen_xyz - n_xyz
    bond_angles1 = np.array([dif.fg.ang(bond, bnd) for bnd in all_bonds])
    ang1_idx = abs(bond_angles1) < np.pi/4
    print(' %d ions < 30Deg to Ru1' % (sum(ang1_idx)))

    # bond angle from ru2
    bond = n_xyz - cen_xyz
    bond_angles2 = np.array([dif.fg.ang(bond, bnd) for bnd in all_bonds2])
    ang2_idx = abs(bond_angles2) < np.pi / 4
    print(' %d ions < 30Deg to Ru2' % (sum(ang2_idx)))

    # Distance to bond
    unit_bond = all_bonds[nidx] / mag[nidx]
    vec_arb = all_bonds - np.dot(all_bonds, unit_bond) * unit_bond  # vector normal from bond to atom
    dist2bond = dif.fg.mag(vec_arb)

    # Atoms near bond
    exchange_idx = av_dis_idx * (dist1_idx + dist2_idx) * ang1_idx * ang2_idx * exchange_allowed
    near_bond_idx = np.where(exchange_idx)[0]
    print('Exchange ions: %d' % len(near_bond_idx))

    # Sort by distance to central atom
    srt_idx = np.argsort(mag[exchange_idx])
    near_bond_idx = near_bond_idx[srt_idx]

    exchange_dist = 0.
    exchange_paths += [[[cen_idx, cen_type, cen_xyz[0]]]]
    for idx in near_bond_idx:
        near_uvw = uvw[idx, :]
        near_xyz = xyz[idx, :]
        near_type = label[idx]
        dist12 = '%4sRu1: %6.2f' % (near_type, mag[idx])
        dist21 = '%4sRu2: %6.2f' % (near_type, mag2[idx])
        ang12 = 'ang1: %3.0fDeg' % np.rad2deg(bond_angles1[idx])
        ang21 = 'ang2: %3.0fDeg' % np.rad2deg(bond_angles2[idx])
        print('   %4s (%6.2f,%6.2f,%6.2f) %s %s %s %s' % (
            near_type, near_uvw[0], near_uvw[0], near_uvw[0],
            dist12, dist21, ang12, ang21
        ))
        exchange_dist += dif.fg.mag(near_xyz - exchange_paths[-1][-1][2])
        exchange_paths[-1] += [[idx, near_type, near_xyz]]
    exchange_dist += dif.fg.mag(n_xyz - exchange_paths[-1][-1][2])
    exchange_paths[-1] += [[nidx, n_type, n_xyz]]
    exchange_distances += [exchange_dist]
    print('Exchange dist: %5.3f A' % exchange_dist)

print('\n\n\nExchange Paths from [%3d] %4s (%5.2f,%5.2f,%5.2f) < %1.2f A' % (
    cen_idx, cen_type, cen_uvw[0], cen_uvw[1], cen_uvw[2], nearest_neighbor_distance))

# Print results
for ex, dis in zip(exchange_paths, exchange_distances):
    str_exchange_path = '.'.join([e[1] for e in ex])
    n_uvw = uvw[ex[-1][0], :]
    str_neigh = '%4s(%5.2f,%5.2f,%5.2f)' % (ex[-1][1], n_uvw[1], n_uvw[0], n_uvw[2])
    bond_dist = mag[ex[-1][0]]
    print('%s %12s BondDist=%5.3fA. ExchangeDist=%5.3fA' % (str_neigh, str_exchange_path, bond_dist, dis))

# Plot results
xtl.Plot.plot_crystal()
ax = plt.gca()
for ex, dis in zip(exchange_paths, exchange_distances):
    x = [el[2][0] for el in ex]
    y = [el[2][1] for el in ex]
    z = [el[2][2] for el in ex]
    ax.plot3D(x, y, z, '-', lw=5)
plt.show()


