# -*- coding: utf-8 -*-
"""
Module: functions_scattering.py

By Dan Porter, PhD
Diamond
2018

Usage:
    - Run this file in an interactive console
    OR
    - from Dans_Diffraction import functions_crystallography as fc

Version 0.1
Last updated: 11/11/18

Version History:
11/11/18 0.1    Version History started.

@author: DGPorter
"""

import sys, os, re
import numpy as np

from . import functions_general as fg
from . import functions_crystallography as fc

__version__ = '0.1'


def phase_factor(hkl, uvw):
    """
    Return the complex phase factor:
        phase_factor = exp(i.2.pi.HKL.UVW')
    :param HKL: array [n,3] integer reflections
    :param UVW: array [m,3] atomic positions in atomic basis units
    :return: complex array [n,m]
    """

    hkl = np.asarray(np.rint(hkl), dtype=np.float).reshape([-1, 3])
    uvw = np.asarray(uvw, dtype=np.float).reshape([-1, 3])

    dotprod = np.dot(hkl, uvw.T)
    return np.exp(1j * 2 * np.pi * dotprod)


def phase_factor_qr(q, r):
    """
    Return the complex phase factor:
        phase_factor = exp(i.Q.R')
    :param q: array [n,3] reflection positions in A^-1
    :param r: array [m,3] atomic positions in A
    :return: complex array [n,m]
    """

    q = np.asarray(q, dtype=np.float).reshape([-1, 3])
    r = np.asarray(r, dtype=np.float).reshape([-1, 3])

    dotprod = np.dot(q, r.T)
    return np.exp(1j * dotprod)


def structure_factor(scattering_factor, occupancy, debyewaller, phase):
    """
    Return the complex structure factor:
        structure_factor = sum_i( sf.occ.dw.phase )
    :param scattering_factor: array [n,m] or [n]: radiation dependent scattering factor/ form factor,/ scattering length
    :param occupancy: array [m]: occupancy of each atom
    :param debyewaller: array [n,m]: thermal vibration factor of each atom and reflection
    :param phase: array [n,m]: complex phase factor
    :return: complex array [n]
    """
    nrefs, natoms = phase.shape
    scattering_factor = np.asarray(scattering_factor, dtype=np.float).reshape([nrefs, -1])
    occupancy = np.asarray(occupancy, dtype=float).reshape([-1, natoms])
    return np.sum(scattering_factor * occupancy * debyewaller * phase, axis=1)


def intensity(structurefactor):
    """
    Returns the squared structure factor
    :param structurefactor: complex array [n] structure factor
    :return: array [n]
    """
    return np.real( structurefactor * np.conj(structurefactor) )


def sf_xray(hkl, uvw, occ, formfactor, debyewaller=1.0):
    """
    Calculate the structure factor for the given HKL, using x-ray scattering factors
    Reference: Nielsen & McMorrow, Int. Tables C
    :param hkl: [n,3] array of hkl reflections
    :param uvw: [m,3] array of atomic positions in r.l.u.
    :param occ: [m,1] array of atomic occupancies
    :param formfactor: [n,m] array of atomic  x-ray form factors for each atom for each reflection
    :param debyewaller: [n,m] array of thermal factors for each atom and reflection
    :return sf: [n,1] complex array of structure factors
    Returns an array with the same length as hkl, giving the complex strucure factor for each reflection
    """

    hkl = np.asarray(hkl, dtype=np.float).reshape(-1, 3)
    uvw = np.asarray(uvw, dtype=np.float).reshape(-1, 3)
    occ = np.asarray(occ, dtype=np.float).reshape(len(uvw), 1)
    formfactor = np.asarray(formfactor, dtype=np.float).reshape(-1, len(hkl))
    debyewaller = np.asarray(debyewaller)
    if debyewaller.size == 1:
        debyewaller = debyewaller*np.ones((len(uvw), len(hkl)))
    else:
        debyewaller = debyewaller.reshape(-1, len(hkl))

    # Calculate structure factor
    # Broadcasting used on 2D ff
    dot = np.dot(hkl, uvw.T)
    sf = np.sum(formfactor * debyewaller * occ * np.exp(1j * 2 * np.pi * dot), axis=1)
    # SF = np.zeros(Nref,dtype=np.complex)
    # for ref in range(Nref):
    #    for at in range(Nat):
    #        SF[ref] += ff[ref,at]*dw[ref,at]*occ[at]*np.exp(1j*2*np.pi*dot_KR[ref,at])
    return sf


def sf_xray_fast(hkl, uvw, occ, z, debyewaller=1.0):
    """
    Calculate the structure factor for the given HKL, using atomic number only
    :param hkl: [n,3] array of hkl reflections
    :param uvw: [m,3] array of atomic positions in r.l.u.
    :param occ: [m,1] array of atomic occupancies
    :param z: [m] array of atomic numbers (pseudo scattering length) for each atom
    :param debyewaller: [n,m] array of thermal factors for each atom and reflection
    :return sf: [n] complex array of structure factors
    Returns an array with the same length as hkl, giving the complex strucure factor for each reflection
    """

    hkl = np.asarray(hkl, dtype=np.float).reshape(-1, 3)
    uvw = np.asarray(uvw, dtype=np.float).reshape(-1, 3)
    occ = np.asarray(occ, dtype=np.float).reshape(len(uvw), 1)
    z = np.asarray(z, dtype=np.float).reshape(len(uvw), 1)
    debyewaller = np.asarray(debyewaller)
    if debyewaller.size == 1:
        debyewaller = debyewaller * np.ones((len(uvw), len(hkl)))
    else:
        debyewaller = debyewaller.reshape(-1, len(hkl))

    # Calculate dot product
    dot = np.dot(hkl, uvw.T)

    # Calculate structure factor
    sf = np.sum(z * debyewaller * occ * np.exp(1j * 2 * np.pi * dot), axis=1)
    return sf


def sf_neutron(hkl, uvw, occ, scatteringlength, debyewaller=1.0):
    """
    Calculate the structure factor for the given HKL, using neutron scattering lengths
    Reference:  Squires
    :param hkl: [n,3] array of hkl reflections
    :param uvw: [m,3] array of atomic positions in r.l.u.
    :param occ: [m,1] array of atomic occupancies
    :param scatteringlength: [n] array of bound coherent scattering length for each atom
    :param debyewaller: [n,m] array of thermal factors
    :return sf: [n] complex array of structure factors
    Returns an array with the same length as HKL, giving the complex structure factor at each reflection.
    """

    hkl = np.asarray(hkl, dtype=np.float).reshape(-1, 3)
    uvw = np.asarray(uvw, dtype=np.float).reshape(-1, 3)
    occ = np.asarray(occ, dtype=np.float).reshape(1, len(uvw))
    scatteringlength = np.asarray(scatteringlength, dtype=np.float).reshape(1, len(uvw))
    debyewaller = np.asarray(debyewaller)
    if debyewaller.size == 1:
        debyewaller = debyewaller * np.ones((len(hkl), len(uvw)))
    else:
        debyewaller = debyewaller.reshape(1, len(uvw))

    # Calculate dot product
    dot = np.dot(hkl, uvw.T)

    # Calculate structure factor
    sf = np.sum(scatteringlength * debyewaller * occ * np.exp(1j * 2 * np.pi * dot), axis=1)
    return sf


def sf_magnetic_neutron(q, r, occ, moment, magnetic_formfactor=None, debyewaller=1.0):
    """
    Calculate the magnetic structure factor for the given HKL, using neutron magnetic form factor
    Assumes an unpolarised incident beam.
        Reference: G. L. Squires, Introduction to the Theory of Thermal Neutron Scattering (Cambridge University Press, 1997).
    :param q: [n,3] array of hkl reflections
    :param r: [m,3] array of atomic positions in r.l.u.
    :param occ: [m,1] array of atomic occupancies
    :param moment: [m,3] array of magnetic moment direction in orthogonal basis
    :param magnetic_formfactor: [n,m] array of magnetic form factors for each atom and relection
    :param debyewaller: [n,m] array of thermal factors for each atom and reflection
    :return sf: [n] complex array of structure factors
    Returns an array with the same length as HKL, giving the complex structure factor at each reflection.
    """

    q = np.asarray(q, dtype=np.float).reshape((-1, 3))
    r = np.asarray(r, dtype=np.float).reshape((-1, 3))
    occ = np.asarray(occ, dtype=np.float).reshape((len(r), 1))
    moment = np.asarray(moment, dtype=np.float).reshape((-1, 3))

    if magnetic_formfactor is None:
        magnetic_formfactor = np.ones([len(q), len(r)])

    # Calculate dot product
    dot = np.dot(q, r.T)
    # direction of q
    qhat = fg.norm(q).reshape([-1, 3])

    # Calculate structure factor
    sf = np.zeros(len(q), dtype=np.complex)
    for n, qh in enumerate(qhat):
        sfm = [0., 0., 0.]
        for m, mom in enumerate(moment):
            # Calculate Magnetic part
            qm = mom - np.dot(qh, mom) * qh

            # Calculate structure factor
            sfm = sfm + (magnetic_formfactor[n, m] * occ[m] * np.exp(1j * dot[n, m]) * qm)

        # Calculate polarisation with incident neutron
        #sf[n] = np.dot(sfm, incident_polarisation_vector)
        # SF[n] = np.dot(SFm,SFm) # maximum possible
        # average polarisation
        sf[n] = (np.dot(sfm, [1, 0, 0]) + np.dot(sfm, [0, 1, 0]) + np.dot(sfm, [0, 0, 1])) / 3
    return sf


def sf_magnetic_neutron_polarised(q, r, occ, moment, incident_polarisation_vector=[1,0,0],
                                  magnetic_formfactor=None, debyewaller=1.0):
    """
    Calculate the magnetic structure factor for the given HKL, using neutron magnetic form factor
    Assumes an unpolarised incident beam.
        Reference: G. L. Squires, Introduction to the Theory of Thermal Neutron Scattering (Cambridge University Press, 1997).
    :param q: [n,3] array of hkl reflections
    :param r: [m,3] array of atomic positions in r.l.u.
    :param occ: [m,1] array of atomic occupancies
    :param moment: [m,3] array of magnetic moment direction in orthogonal basis
    :param incident_polarisation_vector: [1,3] direction of incident polarisation
    :param magnetic_formfactor: [n,m] array of magnetic form factors for each atom and relection
    :param debyewaller: [n,m] array of thermal factors for each atom and reflection
    :return sf: [n] complex array of structure factors
    Returns an array with the same length as HKL, giving the complex structure factor at each reflection.
    """

    q = np.asarray(q, dtype=np.float).reshape((-1, 3))
    r = np.asarray(r, dtype=np.float).reshape((-1, 3))
    occ = np.asarray(occ, dtype=np.float).reshape((len(r), 1))
    moment = np.asarray(moment, dtype=np.float).reshape((-1, 3))

    if magnetic_formfactor is None:
        magnetic_formfactor = np.ones([len(q), len(r)])

    # Calculate dot product
    dot = np.dot(q, r.T)
    # direction of q
    qhat = fg.norm(q).reshape([-1, 3])

    # Calculate structure factor
    sf = np.zeros(len(q), dtype=np.complex)
    for n, qh in enumerate(qhat):
        sfm = np.array([0., 0., 0.])
        for m, mom in enumerate(moment):
            # Calculate Magnetic part
            qm = mom - np.dot(qh, mom) * qh

            # Calculate structure factor
            sfm = sfm + (magnetic_formfactor[n, m] * occ[m] * np.exp(1j * dot[n, m]) * qm)

        # Calculate polarisation with incident neutron
        sf[n] = np.dot(sfm, incident_polarisation_vector)
    return sf


def sf_magnetic_xray(q, r, occ, moment, magnetic_formfactor=None, debyewaller=1.0):
    """
    Calculate the non-resonant magnetic component of the structure factor
    :param q: [n,3] array of hkl reflections
    :param r: [m,3] array of atomic positions in r.l.u.
    :param occ: [m,1] array of atomic occupancies
    :param moment: [m,3] array of magnetic moment direction in orthogonal basis
    :param incident_polarisation_vector: [1,3] direction of incident polarisation
    :param magnetic_formfactor: [n,m] array of magnetic form factors for each atom and relection
    :param debyewaller: [n,m] array of thermal factors for each atom and reflection
    :return sf: [n] complex array of structure factors
    Returns an array with the same length as HKL, giving the complex structure factor at each reflection.

    From Hill+McMorrow Acta Cryst. 1996 A52, 236-244 Equ. (2)
    Book: "X-ray Scattering and Absorption by Magnetic Materials" by Loevesy and Collins. Ch 2. Eqn.2.21+1
    No orbital component assumed
    magnetic moments assumed to be in the same reference frame as the polarisation
    """

    q = np.asarray(q, dtype=np.float).reshape((-1, 3))
    r = np.asarray(r, dtype=np.float).reshape((-1, 3))
    occ = np.asarray(occ, dtype=np.float).reshape((len(r), 1))
    moment = np.asarray(moment, dtype=np.float).reshape((-1, 3))

    if magnetic_formfactor is None:
        magnetic_formfactor = np.ones([len(q), len(r)])

    # Calculate dot product
    dot = np.dot(q, r.T)

    # Calculate structure factor
    sf = np.zeros(len(q), dtype=np.complex)
    for n in range(len(q)):
        # Calculate vector structure factor
        sfm = np.array([0., 0., 0.])
        for m, mom in enumerate(moment):
            sfm = sfm + magnetic_formfactor[n, m] * occ[m] * np.exp(1j * dot[n, m]) * mom

        # Calculate polarisation with incident x-ray
        # The reference frame of the x-ray and the crystal are assumed to be the same
        # i.e. pol=[1,0,0] || mom=[1,0,0] || (1,0,0)
        #sf[n] = np.dot(sfm, self._polarisation_vector_incident)
        # SF[n] = np.dot(SFm,SFm) # maximum possible
        # average polarisation
        sf[n] = (np.dot(sfm, [1, 0, 0]) + np.dot(sfm, [0, 1, 0]) + np.dot(sfm, [0, 0, 1])) / 3
    return sf


def sf_xray_resonant(q, r, occ, moment, energy_kev=None, polarisation='sp', F0=1, F1=1, F2=1, azi_ref_q=(1, 0, 0), psi=0,
                  debyewaller=1.0):
    """
    Calculate structure factors using resonant scattering factors in the dipolar approximation
      I = Scattering.xray_resonant(HKL,energy_kev,polarisation,F0,F1,F2)
    Returns an array with the same length as HKL, giving the real intensity at each reflection.
        energy_kev = x-ray energy in keV
        polarisation = x-ray polarisation: 'ss',{'sp'},'ps','pp'
        F0/1/2 = Resonance factor Flm
        azim_zero = [h,k,l] vector parallel to the origin of the azimuth
        psi = azimuthal angle defining the scattering plane

    Uses the E1E1 resonant x-ray scattering amplitude:
        fxr_n = (ef.ei)*F0 -i(ef X ei).z_n*F1 + (ef.z_n)(ei.z_n)F2

    Where ei and ef are the initial and final polarisation states, respectively,
    and z_n is a unit vector in the direction of the magnetic moment of the nth ion.
    The polarisation states are determined to be one of the natural synchrotron
    states, where sigma (s) is perpendicular to the scattering plane and pi (p) is
    parallel to it.
            ( s-s  s-p )
            ( p-s  p-p )

    From Hill+McMorrow Acta Cryst. 1996 A52, 236-244 Equ. (15)
    """

    q = np.asarray(q, dtype=np.float).reshape((-1, 3))
    r = np.asarray(r, dtype=np.float).reshape((-1, 3))
    occ = np.asarray(occ, dtype=np.float).reshape((len(r), 1))
    moment = np.asarray(moment, dtype=np.float).reshape((-1, 3))
    psi = np.asarray(psi, dtype=np.float).reshape([-1])
    npsi = len(psi)

    # Calculate dot product
    dot = np.dot(q, r.T)

    sf = np.zeros([len(q), npsi], dtype=np.complex)
    for psival in range(npsi):
        # Get resonant form factor
        fxres = xray_resonant_scattering_factor(q, moment, energy_kev, polarisation, F0, F1, F2, azi_ref_q, psi[psival])

        # Calculate structure factor
        # Broadcasting used on 2D fxres
        sf[:, psival] = np.sum(fxres * debyewaller * occ * np.exp(1j * 2 * np.pi * dot), axis=1)

    return sf


def xray_resonant_scattering_factor(q, moment, energy_kev=None, polarisation='sp', F0=1, F1=1, F2=1, psi=0,
                                    azi_ref_q=(1, 0, 0)):
    """
    Calcualte fxres, the resonant x-ray scattering factor
      fxres = Scattering.xray_resonant_scattering_factor(HKL,energy_kev,polarisation,F0,F1,F2,azim_zero,psi)
    energy_kev = x-ray energy in keV
        polarisation = x-ray polarisation: 'ss',{'sp'},'ps','pp'
        F0/1/2 = Resonance factor Flm
        azim_zero = [h,k,l] vector parallel to the origin of the azimuth {[1,0,0]}
        psi = azimuthal angle defining the scattering plane {0}

    :param q: [n*3] array of reflection coordinates in cartesian basis (Q)
    :param moment: [mx3] array of magnetic moments in cartesian basis
    :param energy_kev: float energy in keV
    :param polarisation: polarisation condition: 'sp', 'ss', 'ps', 'pp'. s=sigma, p=pi
    :param F0: 1/0 Resonance factor Flm
    :param F1: 1/0 Resonance factor Flm
    :param F2: 1/0 Resonance factor Flm
    :param azi_ref_q: azimuthal refence, in cartesian basis (Q)
    :param psi: float, azimuthal angle
    :param disp: False*/True display scattering components
    :return: fxres [n*1] array of resonant x-ray scattering factors

    Uses the E1E1 resonant x-ray scattering amplitude:
        fxr_n = (ef.ei)*F0 -i(ef X ei).z_n*F1 + (ef.z_n)(ei.z_n)F2

    Where ei and ef are the initial and final polarisation states, respectively,
    and z_n is a unit vector in the direction of the magnetic moment of the nth ion.
    The polarisation states are determined to be one of the natural synchrotron
    states, where sigma (s) is perpendicular to the scattering plane and pi (p) is
    parallel to it.
            ( s-s  s-p )
            ( p-s  p-p )

    From Hill+McMorrow Acta Cryst. 1996 A52, 236-244 Equ. (15)
    """

    q = np.asarray(q, dtype=np.float).reshape((-1, 3))
    moment = np.asarray(moment, dtype=np.float).reshape((-1, 3))
    nref = len(q)
    nat = len(moment)

    qmag = fg.mag(q)
    tth = fc.cal2theta(qmag, energy_kev)

    fxres = np.zeros([nref, nat], dtype=np.complex)
    for ref in range(nref):
        # Resonant scattering factor
        # Electric Dipole transition at 3d L edge
        # F0,F1,F2 = 1,1,1 # Flm (form factor?)
        z1, z2, z3 = scatteringcomponents(moment, q[ref], azi_ref_q, psi).T
        tthr = np.deg2rad(tth[ref])

        polarisation = polarisation.lower().replace('-', '').replace(' ', '')
        if polarisation in ['sigmasigma', 'sigsig', 'ss']:  # Sigma-Sigma
            f0 = 1 * np.ones(nat)
            f1 = 0 * np.ones(nat)
            f2 = z2 ** 2
        elif polarisation in ['sigmapi', 'sigpi', 'sp']:  # Sigma-Pi
            f0 = 0 * np.ones(nat)
            f1 = z1 * np.cos(tthr) + z3 * np.sin(tthr)
            f2 = -z2 * (z1 * np.sin(tthr) - z3 * np.cos(tthr))
        elif polarisation in ['pisigma', 'pisig', 'ps']:  # Pi-Sigma
            f0 = 0 * np.ones(nat)
            f1 = z3 * np.sin(tthr) - z1 * np.cos(tthr)
            f2 = z2 * (z1 * np.sin(tthr) + z3 * np.cos(tthr))
        elif polarisation in ['pipi', 'pp']:  # Pi-Pi
            f0 = np.cos(2 * tthr) * np.ones(nat)
            f1 = -z2 * np.sin(2 * tthr)
            f2 = -(np.cos(tthr) ** 2) * (z1 ** 2 * np.tan(tthr) ** 2 + z3 ** 2)
        else:
            raise ValueError('Incorrect polarisation. pol should be e.g. ''ss'' or ''sp''')
        fxres[ref, :] = F0 * f0 - 1j * F1 * f1 + F2 * f2
    return fxres


def scatteringcomponents(moment, q, azi_ref_q=(1, 0, 0), psi=0):
    """
    Transform magnetic vector into components within the scattering plane
    :param moment: [n*3] array of magnetic moments in a cartesian basis
    :param q: [1*3] reflection vector in a cartesian basis
    :param azi_ref_q: [1*3] azimuthal reference in a cartesian basis
    :param psi: float azimuthal angle
    :return: (z1, z2, z3) components of the magnetic moment along the reflection direction
    """

    # Define coordinate system I,J,Q (U1,U2,U3)
    Qhat = fg.norm(q)  # || Q
    AxQ = fg.norm(np.cross(azi_ref_q, Qhat))
    Ihat = fg.norm(np.cross(Qhat, AxQ))  # || to azim_zero
    Jhat = fg.norm(np.cross(Qhat, Ihat))  # -| to I and Q

    # Rotate coordinate system by azimuth
    Ihat_psi = fg.norm(np.cos(np.deg2rad(psi)) * Ihat + np.sin(np.deg2rad(psi)) * Jhat)
    Jhat_psi = fg.norm(np.cross(Qhat, Ihat_psi))

    # Determine components of the magnetic vector
    U = np.vstack([Ihat_psi, Jhat_psi, Qhat])
    z1z2z3 = np.dot(moment, U.T)  # [mxmymz.I, mxmymz.J, mxmymz.Q]
    return fg.norm(z1z2z3)


def scatteringvectors(xtl, hkl, energy_kev=None, azim_zero=[1, 0, 0], psi=0, polarisation='s-p'):
    """
    Determine the scattering and polarisation vectors of a reflection based on energy, azimuth and polarisation.
    :param xtl: Crystal Class
    :param hkl: [n,3] array of reflections
    :param energy_kev: x-ray scattering energy in keV
    :param azim_zero: [1,3] direction along which the azimuthal zero angle is determind
    :param psi: float angle in degrees about the azimuth
    :param polarisation: polarisation with respect to the scattering plane, options:
                'ss' : sigma-sigma polarisation
                'sp' : sigma-pi polarisation
                'ps' : pi-sigma polarisation
                'pp' : pi-pi polarisation
    :return: kin, kout, ein, eout
    Returned values are [n,3] arrays
        kin : [n,3] array of incident wavevectors
        kout: [n,3] array of scattered wavevectors
        ein : [n,3] array of incident polarisation
        eout: [n,3] array of scattered polarisation

    The basis is chosen such that Q defines the scattering plane, sigma and pi directions are normal to this plane.
    """

    if energy_kev is None:
        energy_kev = self._energy_kev

    # Define coordinate system I,J,Q (U1,U2,U3)
    # See FDMNES User's Guide p20 'II-11) Anomalous or resonant diffraction'
    Qhat = fg.norm(xtl.Cell.calculateQ(hkl))  # || Q
    AxQ = fg.norm(np.cross(azim_zero, Qhat))
    Ihat = fg.norm(np.cross(Qhat, AxQ))  # || to azim_zero
    Jhat = fg.norm(np.cross(Qhat, Ihat))  # -| to I and Q

    # Determine wavevectors
    bragg = xtl.Cell.tth(hkl, energy_kev)
    rb = np.deg2rad(bragg)
    rp = np.deg2rad(psi)
    kin = np.cos(rb) * np.cos(rp) * Ihat - np.cos(rb) * np.sin(rp) * Jhat - np.sin(rb) * Qhat
    kout= np.cos(rb) * np.cos(rp) * Ihat - np.cos(rb) * np.sin(rp) * Jhat + np.sin(rb) * Qhat
    esig = np.sin(rp)*Ihat + np.cos(rb)*Jhat # sigma polarisation (in or out)
    piin = np.cross(kin, esig) # pi polarisation in
    piout= np.cross(kout, esig) # pi polarisation out

    # Polarisations
    polarisation = polarisation.replace('-', '').replace(' ', '')
    if polarisation in ['sigmasigma', 'sigsig', 'ss']:
        ein = 1.0*esig
        eout = 1.0*esig
    elif polarisation in ['sigmapi', 'sigpi', 'sp']:
        ein = 1.0*esig
        eout= 1.0*piout
    elif polarisation in ['pisigma', 'pisig', 'ps']:
        ein = 1.0*piin
        eout= 1.0*esig
    elif polarisation in ['pipi', 'pp']:
        ein = 1.0*piin
        eout= 1.0*piout
    else:
        raise ValueError('Incorrect polarisation. pol should be e.g. ''ss'' or ''sp''')
    return kin, kout, ein, eout


def xray_nonresonant_magnetic(xtl, HKL, energy_kev=None, azim_zero=[1, 0, 0], psi=0, polarisation='s-p'):
    """
    Calculate the non-resonant magnetic component of the structure factor
    for the given HKL, using x-ray rules and form factor
      Scattering.xray_magnetic([1,0,0])
      Scattering.xray_magnetic([[1,0,0],[2,0,0],[3,0,0])
    Returns an array with the same length as HKL, giving the real intensity at each reflection.

    From Hill+McMorrow Acta Cryst. 1996 A52, 236-244 Equ. (2)
    Book: "X-ray Scattering and Absorption by Magnetic Materials" by Loevesy and Collins. Ch 2. Eqn.2.21+1
    No orbital component assumed
    magnetic moments assumed to be in the same reference frame as the polarisation
    """

    HKL = np.asarray(np.rint(HKL), dtype=np.float).reshape([-1, 3])
    Nref = len(HKL)

    uvw, type, label, occ, uiso, mxmymz = xtl.Structure.get()
    Nat = len(uvw)

    kin, kout, ein, eout = scatteringvectors(xtl, HKL, energy_kev, azim_zero, psi, polarisation)

    Qmag = xtl.Cell.Qmag(HKL)

    # Get magnetic form factors
    if self._use_magnetic_form_factor:
        ff = fc.magnetic_form_factor(type, Qmag)
    else:
        ff = np.ones([len(HKL), Nat])

    # Calculate moment
    momentmag = fg.mag(mxmymz).reshape([-1, 1])
    momentxyz = xtl.Cell.calculateR(mxmymz)  # moment direction in cartesian reference frame
    moment = momentmag * fg.norm(momentxyz)  # broadcast n*1 x n*3 = n*3
    moment[np.isnan(moment)] = 0.

    # Magnetic form factor
    # f_non-res_mag = i.r0.(hw/mc^2).fD.[.5.L.A + S.B] #equ 2 Hill+McMorrow 1996
    # ignore orbital moment L
    B = np.cross(eout, ein) + \
        np.cross(kout, eout)*np.dot(kout, ein) - \
        np.cross(kin, ein)*np.dot(kin, eout) - \
        np.cross(np.cross(kout, eout), np.cross(kin, ein))
    fspin = 1j * ff * np.dot(moment, B)

    # Calculate dot product
    dot_KR = np.dot(HKL, uvw.T)

    # Calculate structure factor
    sf = np.sum(fspin * occ * np.exp(1j * 2 * np.pi * dot_KR), axis=1)

    SF = SF / xtl.scale

    if self._return_structure_factor: return SF

    # Calculate intensity
    I = SF * np.conj(SF)
    return np.real(I)