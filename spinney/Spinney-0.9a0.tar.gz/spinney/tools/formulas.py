# -*- coding: utf-8 -*-
"""
Module containing functions useful for manipulating chemical formulas
"""
import re
from math import gcd
from functools import reduce
from collections import defaultdict

def get_formula_unit(compound):
    """ Gets the formula unit of a particular compound

    Parameters
    ----------
    compound : string
        the formula of the compound.

    Returns
    -------
    formula_unit : string
        the formula unit of :data:`compound`

    Notes
    -----
    This function automatically reduces the coefficients to the smallest
    integers. It however preserves the number of symbols in the formula;
    e.g. C6H6 will return CH, but CH3COOH will return still CH3COOH.
    """
    re_spec = re.compile(r'([A-Z][a-z]?)([0-9]*)')
    groups = re.findall(re_spec, compound)
    at_symbols = []
    at_numbers = []
    for i in range(len(groups)):
        symbol = groups[i][0]
        # if the number of elements is not matched, it is 1
        if not groups[i][1]:
            number = 1
        else:
            number = int(groups[i][1])
        at_symbols.append(symbol)
        at_numbers.append(number)
    gcdiv = reduce(gcd, at_numbers)
    at_numbers = [x//gcdiv for x in at_numbers]
    formula_unit = ''
    for symb, no in zip(at_symbols, at_numbers):
        if no > 1:
            formula_unit += symb + str(no)
        else:
            formula_unit += symb
    return formula_unit

def count_elements(compound, total=False):
    """ Returns the number of atoms in a chemical system.

    Parameters
    ----------
    compound : str
        the compound of interest

    total : bool
        If True, the total number of atoms in the system is also returned

    Returns
    -------
    el_count : dict/tuple
        Dictionary: ``atom:number of atoms`` for each atom in :data:`compound`.
        If total, returns also the number of elements in :data:`compound`
    """
    re_spec = re.compile(r'([A-Z][a-z]?)([0-9]*)')
    groups_comp = re.findall(re_spec, compound)
    el_count = defaultdict(float)
    for g in groups_comp:
        if g[1]:
            el_count[g[0]] += float(g[1])
        else:
            el_count[g[0]] += 1
    if total:
        return el_count, sum(el_count.values())
    return el_count

def get_stoichiometry(compound, fractional=True):
    """ Given :data:`compound`, it returns its stoichiometry.

    Parameters
    ----------
    compound : string
        the compound's formula

    fractional : bool
        if True, for each element is returned its molar fraction;
        otherwise, it is returned the number of atoms per formula

    Returns
    -------
    elements_count : dict
        A dictionary element:coefficient for each element in :data:`compound`
    """
    elements_count = count_elements(compound)

    if fractional:
        total_atoms = sum(elements_count.values())
        for key in elements_count.keys():
            elements_count[key] /= total_atoms

    return elements_count

def get_number_fu(compound, fu=None):
    """ Returns how many formula units :data:`fu` are present in
    :data:`compound`

    Parameters
    ----------
    compound : string
        the formula of the compound

    fu : string
        the formula unit
        If None, the actual formula unit is used

    Returns
    -------
    no_units : float
        The number of formula units in :data:`compound`
    """
    if fu is None:
        fu = get_formula_unit(compound)
    el_count = count_elements(compound)
    el_count_fu = count_elements(fu)
    multiples = []
    for key, value in el_count.items():
        multi = value/el_count_fu[key]
        try:
            assert multi%1 < 1e-6
        except AssertionError:
            raise AssertionError('The compound {:s} has not an integer number '
                                 'of formula units {:s}'.format(compound, fu))
        multiples.append(int(multi))
    no_units = multiples[0]
    try:
        assert all(x == no_units for x in multiples)
    except AssertionError:
        raise AssertionError('The compound {:s} has not an integer number '
                             'of formula units {:s}'.format(compound, fu))
    return no_units
