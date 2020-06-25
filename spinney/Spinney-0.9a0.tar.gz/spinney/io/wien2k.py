# -*- coding: utf-8 -*-
""" Helper functions for WIEN2k """
import re
import numpy as np
import ase.io
from spinney.constants import conversion_table
from spinney.structures.pointdefect import DummyAseCalculator

def read_wien2k_vcoul(vcoul_file):
    """ Reads the radial part of the electrostatic potential,
    corresponding to the angular term l=0, m=0, inside the atomic
    sphere.

    Parameters
    ----------
    vcoul_file : str
        the path of the .vcoul file

    Returns
    -------
    result: list of lists
        each list contains the radial potential
        for one atom
    """
    end = 'COULOMB POTENTIAL IN INTERSTITIAL'
    block_id = 'NUMBER OF LM'
    pots = []
    regex = '-?[0-9].[0-9]+E[+-][0-9]{2}'
    with open(vcoul_file, 'r') as f:
        reg = re.compile(regex)
        line_count = -1
        blocks_no = 0
        while True:
            line = next(f).strip()
            if line.startswith(block_id):
                blocks_no = 0
                line_count += 1
                pots.append([])
            elif line == end:
                break
            elif line.startswith('VLM'):
                blocks_no += 1
            if blocks_no == 1:
                match = reg.findall(line)
                if match:
                    pots[line_count] += [float(x) for x in match]
    return pots

def read_wien2k_radial_data(struct_file):
    """ Reads from a .struct file some information about the
    atom-centered spheres related to the radial potential within
    the sphere.

    Parameters
    ----------
    struct_file : str
        path to the struct file

    Returns
    -------
    2D tuple array of shape (No_atoms, 4)
        No_atoms is the number of irreducible atoms in the system,
        for each of them, we store R0, RMT, NPT, MULTI
    """
    regex_int = '[0-9]+'
    regex_float = '[0-9]+\.[0-9]+'
    data = []
    with open(struct_file, 'r') as f:
        next(f)
        line = next(f).strip()
        no_ineq_atoms = int(line.split()[1])
        next(f)
        next(f)
        for atom in range(no_ineq_atoms):
            data.append([])
            next(f)
            line = next(f).strip()
            match = re.search('MULT=\s*' + regex_int, line).group()
            multi = int(re.search(regex_int, match).group())
            for i in range(multi - 1):
                next(f)
            line = next(f).strip()
            npt = re.search('NPT=\s*' + regex_int, line).group()
            npt = int(re.search(regex_int, npt).group())
            r0 = re.search('R0=\s*' + regex_float, line).group()
            r0 = float(re.search(regex_float, r0).group())
            rmt = re.search('RMT=\s*' + regex_float, line).group()
            rmt = float(re.search(regex_float, rmt).group())
            data[atom] += [r0, rmt, npt, multi]
            for i in range(3):
                next(f)
    data = tuple(tuple(x) for x in data)
    return data

def average_core_potential_wien2k(potential, r0, rmax):
    """ Calculates the average core potential within a spherical
    shell with the smallest raius r0 and the largest rmax.

    Parameters
    ----------
    potential : 1D numpy array
        the radial part of the potential corresponding to the
        l=0, m=0 angular component.

    r0 : float
        the smallest radius of the shell

    rmax : float
        the largest radius of the shell

    Returns
    -------
    float : the averaged potential in the spherical shell
    """
    vol = 4*np.pi/3 * (rmax**3 - r0**3)
    n = len(potential)
    r = np.logspace(np.log(r0), np.log(rmax), n, base=np.e)
    drho = (np.log(rmax)-np.log(r0))/n
    integrand = potential*r
    av_pot = np.trapz(integrand, np.log(r), drho)
    av_pot /= vol
    # divide by the spherical harmonic Y_00 included in the vcoul data
    return av_pot*np.sqrt(4*np.pi)

def extract_potential_at_core_wien2k(struct, vcoul):
    """ Extracts the average electrostatic potential within the
    atomic spheres for each atom in the system.

    Parameters
    ----------
    struct : string
        the path to the .struct file

    vcoul : string
        the path to the .vcoul file

    Returns
    -------
    result : 1D numpy array
        for each atom in the system, returns the
        average electrostatic potential within the spherial region
    """
    struct_data = read_wien2k_radial_data(struct)
    pots = read_wien2k_vcoul(vcoul)

    if len(struct_data) != len(pots):
        raise ValueError('Number of atoms in {} is different than '
                         'the number of atoms in {}'.format(struct, vcoul))
    core_pots = []
    for i in range(len(pots)):
        pot = pots[i]
        data = struct_data[i]
        if len(pot) != data[2]:
            raise ValueError(
                'Number of grid points in {} '
                'does not corresponds to the number of grid points '
                'used in {}'.format(struct, vcoul))
        av_pot = average_core_potential_wien2k(pot, data[0], data[1])
        core_pots += [av_pot]*data[3]
    # electron charge +1 in Wien2K
    return -np.array(core_pots)

def prepare_ase_atoms_wien2k(struct_file, scf_file):
    """ Prepare an :class:`ase.Atoms` object compatible with the interface of the
    :class:`PointDefect` class in Spinney.

    Parameters
    ----------
    struct_file : string
        the path to the WIEN2K .struct file

    total_energy : float
        the value of the total energy as found in the WIEN2K .scf file

    Returns
    -------
    ase_wien : :class:`ase.Atoms`
        the :class:`ase.Atoms` object representing the system
    """
    total_energy = read_energy_wien2k(scf_file)
    # ase can open a Wien2K struct file, but has problems with the scf ones
    ase_wien = ase.io.read(struct_file, format='struct')
    # we convert the total energy to eV: the unit used internally by ase
    total_energy *= conversion_table['Ry']['eV']
    # to be able to use the PointDefect class, we need to attach a calculator
    # to the Atoms instance and set the total energy value.
    calc = DummyAseCalculator(ase_wien.copy())
    ase_wien.set_calculator(calc)
    # we need to tell him that we have calculated the energy
    ase_wien.calc.set_total_energy(total_energy)
    return ase_wien

def read_energy_wien2k(scf_file):
    """ Returns the total electronic energy.

    Parameters
    ----------
    scf_file : string
        path to the WIEN2k .scf file

    Returns
    -------
    energy : float
        the energy of the system
    """
    energies = []
    regex = ':ENE'
    with open(scf_file, 'r') as f:
        for line in f:
            line = line.strip()
            if re.findall(regex, line):
                energies.append(float(line.split()[-1]))
    energy = energies[-1]
    return energy
