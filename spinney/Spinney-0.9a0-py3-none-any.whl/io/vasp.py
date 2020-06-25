# -*- coding: utf-8 -*-
""" Helper functions for VASP postprocessing """
import re
import numpy as np

def extract_potential_at_core_vasp(file):
    """
    Read the VASP OUTCAR file and extract the values of the electrostatic
    potential evaluated at the ions positions.

    Parameters
    ----------
    file : string
        path to the OUTCAR file

    Returns
    -------
    result : 1D numpy array
        for each atom in the system, returns the electrostatic
        potential at the atomic sites
    """
    look = 'average (electrostatic) potential at core'
    pots = []
    with open(file) as f:
        for line in f:
            line = line.strip()
            if line == look:
                pot = []
                next(f)
                next(f)
                while True:
                    lline = f.readline().strip().split()
                    if lline and lline[0] == 'E-fermi':
                        break
                    elif lline:
                        for x in lline:
                            pot.append(x)
                # flip the sign as for VASP returns the
                # potential energy where the electron
                # charge has magnitude 1
                pots.append(-np.array(pot[1::2]).astype(np.float64))
    return pots[-1]

def extract_dos(vasprun_file, save_dos=False):
    """ From the vasprun.xml file extrat the DOS.

    Parameters
    ----------
    vasprun_file : string
        path to the vasprun.xml file

    save_dos : bool
        if True, the extracted DOS are saved as a text file.
        The first column is the energy (in eV) and the second
        the DOS (states/cell)

    Returns
    -------
    dos : 2-ple, the DOS up and DOS down (if any)
        each element is a 2D numpy array.
        First column

    """
    vasprun = vasprun_file
    ispin = False
    regex = 'ISPIN.+([1-2])'
    with open(vasprun, 'r') as stream:
        e1 = []
        dos1 = []
        e2 = []
        dos2 = []
        while True:
            line = next(stream)
            line = line.strip('\n').strip()
            if re.findall(regex, line):
                isvalue = re.findall(regex, line)[0]
                if isvalue == 2:
                    ispin = True
            if line == '<dos>':
                break
        line = next(stream)
        e_fermi = line.strip('\n').strip().split()[-2]
        for i in range(9):
            next(stream)
        stop = False
        while not stop:
            line = next(stream)
            line = line.strip('\n').strip()
            if line == '</set>':
                stop = True
            else:
                line = line.split()
                e1.append(float(line[1]))
                dos1.append(float(line[2]))
        if ispin:
            next(stream)
            stop = False
            while not stop:
                line = next(stream)
                line = line.strip('\n').strip()
                if line == '</set>':
                    stop = True
                else:
                    line = line.split()
                    e2.append(float(line[1]))
                    dos2.append(float(line[2]))

    dos_up = np.c_[e1, dos1]
    dos_down = np.c_[e2, dos2]

    if save_dos:
        print('\nFermi level = ', e_fermi)
        np.savetxt('dos_up.txt', dos_up, delimiter='    ')
        np.savetxt('dos_down.txt', dos_down, delimiter='    ')

    return (dos_up, dos_down)
