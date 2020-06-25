# -*- coding: utf-8 -*-
""" Helper functions for calculating reaction energies.
"""
from collections import defaultdict
import numpy as np
import spinney.tools.formulas as cf

def get_compound_energy_per_formula_unit(energy, formula, formula_unit=None):
    """ Returns the calculated energy of the compound per formula unit
    (unit_energy/f.u.)

    Parameters
    ----------
    energy : float
        the energy of the compound with formula :data:`formula`

    formula : string
        the compound formula

    formula_unit : string
        The formula unit of the compound

    Returns
    -------
    energy : float
        The total energy per formula unit and the number of formula units
        in :data:`formula`
    """
    no_fu = cf.get_number_fu(formula, formula_unit)

    return energy/no_fu, no_fu

def get_compound_energy_per_atom(energy, formula):
    """ Returns the energy of the compound per atom (unit_energy/atom)

    Parameters
    ----------
    energy : float
        the energy of the compound

    formula : string
        the formula of the compound

    Returns
    -------
    energy : float
        The energy per atom
    """
    tot_atoms = cf.count_elements(formula, total=True)[1]

    return energy/tot_atoms


def calculate_reaction_energy(reaction, compound_energies):
    r""" Calculates the reaction energy of a compound

    Parameters
    ----------
    reaction : dict of lists of tuples
        Describes the reaction that will be calculated.
        The dictionary keys are 'reactants' and 'products'.
        The value of 'reactants' is a list with tuples.
        Each tuple contains the FORMULA UNIT of the reactants
        and the number of moles for that reactant in the reaction.
        The value of 'products' is analogous, but for the products.

        The compounds specified in :data:`reaction` will be taken as
        the formula units in calculating the reaction.


    compound_energies : dict of lists
        Analogous structure as in :data:`reaction`, but instead of the number
        of moles, the values are the calculated energies.

        Note:
            the order of the compounds in each list has to match
            that in :data:`reaction`!

        E.g. we calculated the energies of 'Mn2' (bcc Mn cell), 'O2'
        and 'Mn32O48' (Pbca space group)
        Then we would have:

        >>> compound_energies = {
                                  'reactants' : [('Mn2',E1), ('O2', E2)],
                                  'products'  : [('Mn32O48', E3)]
                                 }

    Returns
    -------
    energy : float
        The energy of the reaction specified in :data:`reaction`

    Examples
    --------
    Suppose one is interested in the reaction:

    .. math::

        2\mathrm{Mn} + 3/2 \mathrm{O}_2 \rightarrow
        \mathrm{Mn}_2\mathrm{O}_3

    And one has calculated the energy of Mn2 (bcc cell) and stored it in
    the variable ``E1``, the energy of O2 is stored in ``E2``
    and that of Mn2O3 in ``E3``.
    Then to calculate the reaction energy one can use:

    >>> reaction = {
                    'reactants' : [('Mn', 2), ('O2', 3/2)],
                    'products'  : [('Mn2O3', 1)]
                   }
    >>> compound_energies = {
                             'reactants' : [('Mn2', E1), ('O2', E2)],
                             'products'  : [('Mn2O3', E3)]}
    >>> calculate_reaction_energy(reaction, compound_energies)
    """
    reactants = reaction['reactants']
    products = reaction['products']
    # The compounds specified in *reaction* are taken to be the formula units
    reactants_fu, moles_reactants = list(zip(*reactants))
    products_fu, moles_products = list(zip(*products))

    # Normalize energies to formula units and add eventual corrections
    react_energies_per_fu = []
    prod_energies_per_fu = []

    for i, react in enumerate(compound_energies['reactants']):
        cfu = reactants_fu[i]
        energy_fu = get_compound_energy_per_formula_unit(react[1],
                                                         react[0],
                                                         cfu)[0]
        react_energies_per_fu.append(energy_fu*moles_reactants[i])
    for i, prod in enumerate(compound_energies['products']):
        cfu = products_fu[i]
        energy_fu = get_compound_energy_per_formula_unit(prod[1],
                                                         prod[0],
                                                         cfu)[0]

        prod_energies_per_fu.append(energy_fu*moles_products[i])

    return np.sum(prod_energies_per_fu) - np.sum(react_energies_per_fu)


def calculate_formation_energy_fu(compound_dict, components_dict):
    r""" Calculated the formation energy of a given compound per formula unit

    Parameters
    ----------
    compound_dict, components_dict : dict
        ``formula : energy``
        for each compound needed to calculate the defect formation energy:
        ``formula`` is a string representing the compound formula,
        ``energy`` is a number, representing the corresponding compound
        energy.

    Examples
    --------
    In order to calculate the formation energy of :math:`\mathrm{SrTiO}_3`,
    ``compound_dict`` and ``components_dict`` are:

    >>> compound_dict = {'SrTiO3':Ec}
    >>> components_dict = {'Sr':Esr, 'Ti':Eti, 'O2':Eo2}
    """
    compound_energies = {
                         'reactants' : list(zip(components_dict.keys(),
                                                components_dict.values())),
                         'products' : list(zip(compound_dict.keys(),
                                               compound_dict.values()))
                        }
    if len(compound_energies['products']) != 1:
        raise ValueError('Only the formation energy of exactly one compound '
                         'can be calculated')
    comp = list(compound_dict.keys())[0]
    no_fu = cf.get_number_fu(comp)
    elsp = cf.count_elements(comp)
    reactcomp = list(components_dict.keys())
    elspr = [cf.count_elements(x) for x in reactcomp]
    reactants = []
    for el in elsp:
        for i, react in enumerate(elspr):
            nor = react.get(el, 0)
            if nor == 0:
                continue
            no = elsp[el]/react[el]
            break
        reactants.append((reactcomp[i], no))
    reaction = {
                'products' : [(comp, 1)],
                'reactants' : reactants
               }
    return calculate_reaction_energy(reaction, compound_energies)/no_fu

def calculate_defect_formation_energy(e_defect, e_pristine, chem_potentials,
                                      charge_state, E_corr=0):
    """ Calculate the formation energy of a point defect.

    Parameters
    ----------
    e_defect : dict
        {formula : energy of the defective supercell}

    e_pristine: dict
        {formula : energy of the pristine supercell}

    chem_potentials : dict
        {element_name : chemical_potential}
        element_name is the element symbol, in the case of the electron,
        element_name = electron

    charge_state : int
        the formal charge state of the defect

    E_corr : float
        eventual corrections to the defect formation energy

    Returns
    -------
    formation_energy : float
    """
    def_formula, def_energy = list(e_defect.items())[0]
    prist_formula, prist_energy = list(e_pristine.items())[0]

    el_count_def = cf.count_elements(def_formula)
    el_count_prist = cf.count_elements(prist_formula)

    reaction = defaultdict(list)
    compound_energies = defaultdict(list)
    reaction['products'].append((def_formula, 1))
    compound_energies['products'].append((def_formula, def_energy))
    reaction['reactants'].append((prist_formula, 1))
    compound_energies['reactants'].append((prist_formula, prist_energy))

    for element in [x for x in chem_potentials.keys() if x != 'electron']:
        def_coeff = el_count_def.get(element, 0)
        prist_coeff = el_count_prist.get(element, 0)

        dcoeff = def_coeff - prist_coeff
        if dcoeff < 0:
            reaction['products'].append((element, -dcoeff))
            compound_energies['products'].append((element,
                                                  chem_potentials[element]))
        elif dcoeff > 0:
            reaction['reactants'].append((element, dcoeff))
            compound_energies['reactants'].append((element,
                                                   chem_potentials[element]))

    formation_energy = calculate_reaction_energy(reaction, compound_energies)

    formation_energy += charge_state*chem_potentials['electron']

    return formation_energy + E_corr
