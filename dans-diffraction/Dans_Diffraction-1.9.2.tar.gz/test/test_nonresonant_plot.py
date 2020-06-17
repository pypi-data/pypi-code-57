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
xtl.Atoms.changeatom(1,mxmymz=[0, 3, 0])
xtl.generate_structure()

xtl.Scatter._use_magnetic_form_factor = False
hkl = [1,0,3]
energy_kev = 2.838
azim_zero = [0,1,0]
pol = 'sp'
psi = 10
psirange = np.arange(-180,181,1)
a,b,c = xtl.Cell.UV()
moment = dif.fg.norm(xtl.Cell.calculateR(xtl.Structure.mxmymz()[8:12]))
uvw = xtl.Structure.uvw()[8:12]
phase = np.exp(1j * 2 * np.pi * np.dot(hkl, uvw.T))


def splane(hkl, energy_kev, azim_zero, psi, pol):
    U1, U2, U3 = xtl.Scatter.scatteringbasis(hkl, azim_zero, psi)
    kin, kout, ein, eout = xtl.Scatter.scatteringvectors(hkl, energy_kev, azim_zero, psi, pol)
    return U1, U2, U3, kin, kout, ein, eout


def calf1(kout):
    ang = [dif.fg.ang(-kout[0], mom, 'deg') for mom in moment]
    f1sp = np.dot(-kout[0], moment.T)
    incphase = f1sp*phase
    tot = np.sum(incphase)
    tot2 = tot * np.conj(tot)
    print('Angle = %s'%ang)
    print('-k''.z = %s'%f1sp)
    print('inc phase = %s'%incphase)
    print('sum = %5.3f'%tot)
    print('sum^2 = %5.3f' % tot2)
    return tot2

def plotplane(hkl, energy_kev, azim_zero, psi, pol):
    U1, U2, U3, kin, kout, ein, eout = splane(hkl, energy_kev, azim_zero, psi, pol)

    tot2 = calf1(kout)

    fig = plt.figure(figsize=[12, 12])
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-1,1])
    ax.set_ylim([-1,1])
    ax.set_zlim([-1,1])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.title('(%1.0f,%1.0f,%1.0f) psi=%3.0f, sum^2 = %5.3f'%(hkl[0],hkl[1],hkl[2],psi, tot2), fontsize=28)

    ax.plot([0, U1[0]], [0, U1[1]], [0, U1[2]], '-k', lw=2)  # U1
    ax.plot([0, U2[0]], [0, U2[1]], [0, U2[2]], '-k', lw=2)  # U2
    ax.plot([0, U3[0]], [0, U3[1]], [0, U3[2]], '-k', lw=3)  # U3

    ax.plot([-kin[0, 0], 0], [-kin[0, 1], 0], [-kin[0, 2], 0], '-b')  # Kin
    ax.plot([0, kout[0, 0]], [0, kout[0, 1]], [0, kout[0, 2]], '-b')  # Kout

    ax.plot([-kin[0, 0], -kin[0, 0] + ein[0, 0]], [-kin[0, 1], -kin[0, 1] + ein[0, 1]],
            [-kin[0, 2], -kin[0, 2] + ein[0, 2]], '-g')  # ein
    ax.plot([kout[0, 0], kout[0, 0] + eout[0, 0]], [kout[0, 1], kout[0, 1] + eout[0, 1]],
            [kout[0, 2], kout[0, 2] + eout[0, 2]], '-g')  # eout

    ax.plot([0, a[0]], [0, a[1]], [0, a[2]], '-m')  # a
    ax.plot([0, b[0]], [0, b[1]], [0, b[2]], '-m')  # b
    ax.plot([0, c[0]], [0, c[1]], [0, c[2]], '-m')  # c

    ax.plot([0, moment[0, 0]], [0, moment[0, 1]], [0, moment[0, 2]], '-r', lw=2)  # moment

    #plt.show()

def sergio_103(energy_kev, psi):
    hkl = [1, 0, 3]
    beta = np.abs(dif.fg.ang(xtl.Cell.calculateQ(hkl), [0, 0, 1]))
    # Converstion between lab frame to xtl frame (for (1,0,3) only)
    U = np.array([[0, -np.cos(beta), np.sin(beta)], [1, 0, 0], [0, np.sin(beta), np.cos(beta)]])
    #U = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    brag = np.deg2rad(xtl.Cell.tth(hkl, energy_kev))[0] / 2.

    azim = np.deg2rad(psi)
    u1 = np.array([np.cos(azim), -np.sin(azim), 0])
    u2 = np.array([np.sin(azim), np.cos(azim), 0])
    u3 = np.array([0, 0, 1])
    ki = np.array([[np.cos(brag) * np.cos(azim), -np.cos(brag) * np.sin(azim),-np.sin(brag)]])
    kf = np.array([[np.cos(brag) * np.cos(azim), -np.cos(brag) * np.sin(azim), np.sin(brag)]])
    # From paper:
    es = np.array([[np.sin(azim), np.cos(azim), 0]])
    ep = np.array([[-np.sin(brag) * np.cos(azim), np.sin(brag) * np.sin(azim), np.cos(brag)]])
    # changed to work:
    #es = np.array([[-np.sin(azim), np.cos(azim), 0]])
    #ep = np.array([[-np.sin(brag) * np.cos(azim), -np.sin(brag) * np.sin(azim), np.cos(brag)]])

    U1 = np.dot(u1, U.T)
    U2 = np.dot(u2, U.T)
    U3 = np.dot(u3, U.T)
    kin = np.dot(ki, U.T)
    kout = np.dot(kf, U.T)
    ein = np.dot(es, U.T)
    eout = np.dot(ep, U.T)
    return U1, U2, U3, kin, kout, ein, eout


def plotsergio_103(energy_kev, psi):
    U1, U2, U3, kin, kout, ein, eout = sergio_103(energy_kev, psi)
    tot2 = calf1(kout)

    fig = plt.figure(figsize=[12, 12])
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-1,1])
    ax.set_ylim([-1,1])
    ax.set_zlim([-1,1])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.title('(%1.0f,%1.0f,%1.0f) psi=%3.0f, sum^2 = %5.3f'%(hkl[0],hkl[1],hkl[2],psi, tot2), fontsize=28)

    ax.plot([0, U1[0]], [0, U1[1]], [0, U1[2]], '-k', lw=2)  # U1
    ax.plot([0, U2[0]], [0, U2[1]], [0, U2[2]], '-k', lw=2)  # U2
    ax.plot([0, U3[0]], [0, U3[1]], [0, U3[2]], '-k', lw=3)  # U3

    ax.plot([-kin[0, 0], 0], [-kin[0, 1], 0], [-kin[0, 2], 0], '-b')  # Kin
    ax.plot([0, kout[0, 0]], [0, kout[0, 1]], [0, kout[0, 2]], '-b')  # Kout

    ax.plot([-kin[0, 0], -kin[0, 0] + ein[0, 0]], [-kin[0, 1], -kin[0, 1] + ein[0, 1]],
            [-kin[0, 2], -kin[0, 2] + ein[0, 2]], '-g')  # ein
    ax.plot([kout[0, 0], kout[0, 0] + eout[0, 0]], [kout[0, 1], kout[0, 1] + eout[0, 1]],
            [kout[0, 2], kout[0, 2] + eout[0, 2]], '-g')  # eout

    ax.plot([0, a[0]], [0, a[1]], [0, a[2]], '-m')  # a
    ax.plot([0, b[0]], [0, b[1]], [0, b[2]], '-m')  # b
    ax.plot([0, c[0]], [0, c[1]], [0, c[2]], '-m')  # c

    ax.plot([0, moment[0, 0]], [0, moment[0, 1]], [0, moment[0, 2]], '-r', lw=2)  # moment

    #plt.show()

plotplane(hkl, energy_kev, azim_zero, psi, pol)
plotsergio_103(energy_kev, psi)
plt.show()
print('finished')