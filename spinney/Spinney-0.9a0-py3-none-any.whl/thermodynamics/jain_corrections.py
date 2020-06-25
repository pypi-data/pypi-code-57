# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 10:53:52 2019

@author: arrigoni

Fit corrections for transition metal oxydes calculated with DFT+U.

Follow the receipt of A. Jain et al., PRB 84, 045115 (2011).

This framework automatically adds +1.36eV to the energy of the O2 molecule, in
order to correct for the GGA binding energy for O2, as explained in
L. Wang et al., PRB 73, 195107 (2006).

!!! Units of energy are in eV.

Delta E_M is the difference between GGA+U and experimental formation energies
divided by the number of transition metal atoms in the compound.

NOTE: for now the module works only with  binary oxides
"""
import numpy as np
from scipy.optimize import curve_fit
import spinney.tools.formulas as cf

def find_correction_term_binary(dft_u_energies, exp_energies,
                                compound_list, metal_atom,
                                fit=False):
    """ Returns Delta E_M = average difference between DFT+U formation energies
    and experimental formation energies of the  binary oxide
    per number of metal atoms in the oxide

    Parameters
    ----------
    dft_u_energies : array
                    formation energies, per FORMULA UNIT, of the binary oxide
                    calculated using DFT + U (INCLUDING  Wang fitting term).
                    What is taken as formula unit for each compound is what 
                    is specified in *compound_list*
    
    exp_energies : array
                    experimental formation energies, per FORMULA UNIT, of the
                    binary oxide
    
    compound_list : list of strings
                    each entry is the FORMULA UNIT of one binary oxide
                    The order of compounds in the two arrays with the formation
                    energies per formula unit must match this order
    
    metal_atom : string
                 the metal atom for which we want to calculate the correction
                 term
    fit : bool
          if True, a least square fit is used to find the parameter;
          otherwise we use the average of the difference (it should return
          almost identical values)
          
    Returns
    -------
        2-ple : the correction term and its estimated standard error
    """
    no_atoms = []
    no_metal_atoms = []
    for compound in compound_list:
        elements = cf.count_elements(compound)
        no_metal_atoms.append(elements[metal_atom])
        no_atoms.append(np.sum(list(elements.values())))
    no_atoms = np.array(no_atoms)
    no_metal_atoms = np.array(no_metal_atoms)

    if fit:
        x = no_metal_atoms/no_atoms
        y = (dft_u_energies - exp_energies)/no_atoms
        def f(x, m):
            return m*x
        popt, pcov = curve_fit(f, x, y)
        return popt, np.sqrt(np.diag(pcov))

    else:
        y = (dft_u_energies/no_metal_atoms - exp_energies/no_metal_atoms)
        return y.mean(), y.std()
