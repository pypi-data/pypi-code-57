from ase.io import read, write
from ase import Atoms, Atom


def parse_incar(filename='INCAR'):
    """Read VASP INCAR file and return as a dictionary.

    Parameters
    ----------
    filename : str
        Name of INCAR file. default is 'INCAR'.

    Returns
    -------
    incar_dict
        a dictionary containing INCAR tags and value.
    """
    with open(filename,'r') as incar:
        incar_dict={}
        lines=incar.readlines()
        for line in lines:
            if '=' in line:
                tag,value=line.strip().split('=')
                tag=tag.strip()
                value=value.strip()
                incar_dict[tag]=value
    return incar_dict

def get_mdenergy(filename='OUTCAR'):
    """Read VASP OUTCAR file from a relaxation run and return energy of each molecular dynamics steps
       energies in a array.

    Parameters
    ----------
    filename : str
        Name of OUTCAR file. default is 'OUTCAR'.

    Returns
    -------
    energies
        a array of containing energies of each MD steps.
    """
    energies=[]
    outcar=read(filename,index=':')
    for steps in outcar:
        energies.append(steps.get_potential_energy())
    return energies


