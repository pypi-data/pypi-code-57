# -*- coding: utf-8 -*-
""" Module with general tools and classes for handling chemical
potential-related quantities.

The :class:`Range` class allows to calculate valid chemical potential
values given competing phases.
"""
from collections import defaultdict
from functools import reduce
import itertools
from math import gcd
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.optimize import linprog, brentq
from spinney.constants import (conversion_table, available_units,
                               UnitNotFoundError, _k)
from spinney import containers
from spinney.tools.formulas import get_formula_unit

def ideal_gas_chemical_potential(mu_standard, partial_pressure, T,
                                 energy_units='eV', pressure_units='Pa'):
    r"""
    Temperature and pressure-dependent chemical potential of an ideal gas

    .. math::

        \mu = \mu^\circ + k_B T \ln \left(\frac{p}{p^\circ}\right)

    Parameters
    ----------
    mu_standard : float
        the gas molecule chemical potential at standard pressure

    partial_pressure : array or float
        the gas partial pressure with respect to the standard pressure

    T : array or float
        the temperature range of interest

    energy_units : string
        the units in which energy is expressed

    pressure_unit : string
        the units in which pressure is expressed

    Returns
    -------
    chem_pots : array/float
        The chemical potentials as a 2D numpy array of shape
        (len(T), len(partial_pressure)) if both T and partial_pressure
        are arrays; otherwise a 1D numpy array of length len(partial_pressure)
        if partial_pressure is an array and T a float; otherwise a 2D array
        of shape (len(T), 1) if partial_pressure is a float and T an array;
        finally if both T and partial_pressure are float, the result is a float
    """
    if type(mu_standard) in containers:
        raise TypeError('The chemical potential has to be a scalar')
    if energy_units not in available_units:
        raise UnitNotFoundError('{} is not a valid unit.'
                                .format(energy_units))
    conv_factor = conversion_table['J'][energy_units]
    kb = _k * conv_factor
    if pressure_units not in available_units:
        raise UnitNotFoundError('{} is not a valid unit.'
                                .format(pressure_units))
    p_std = 1e5*conversion_table['Pa'][pressure_units]
    if type(partial_pressure) in containers:
        partial_pressure = np.array(partial_pressure)
    if type(T) in containers:
        T = np.array(T)
        T = T[:, np.newaxis]
    return mu_standard + kb*T*np.log(partial_pressure/p_std)

# tools for finding the partial pressure which gives a given chemical potential
def find_p_closure(mu, mu_standard, T, energy_units, pressure_units):
    def find_p(pressure):
        return ideal_gas_chemical_potential(mu_standard, pressure, T,
                                            energy_units, pressure_units) - mu
    return find_p

def find_partial_pressure_given_mu(mu, mu_standard, T, pa=1e-12, pb=1e9,
                                   energy_units='eV', pressure_units='Pa'):
    """ Finds the partial pressure required to change the chemical potential
    of the ideal gas from ``mu_standard`` to ``mu`` at
    temperature ``T``.

    Parameters
    ----------
    mu : float
        the desired value of the chemical potential

    mu_standard : float
        the standard state chemical potential of the ideal gas

    T : float
        the temperature of interest

    pa : float
        the lower bound for the partial pressure

    pb : float
        the upperbound for the partial pressure

    energy_units : string
        the unit of energy used for the value of ``mu`` and
        ``mu_standard``

    pressure_units : string
        the unit of pressure

    Returns
    -------
    p : float
        the partial pressure giving ``mu``
    """
    p_function = find_p_closure(mu, mu_standard, T, energy_units,
                                pressure_units)
    pa *= conversion_table['Pa'][pressure_units]
    pb *= conversion_table['Pa'][pressure_units]
    if type(T) in containers:
        raise TypeError('Temperature must be a scalar')
    try:
        p = brentq(p_function, pa, pb)
    except ValueError:
        print('Cannot find the root, decrease pa and increase pb')

    return p

class IdealGasChemPot:
    """ Class for modelling the chemical potential of an ideal gas molecule

    Parameters
    ----------
    energy_units : string
        the units to be used for the energy

    pressure_units : string
        the units to be used for the pressure
    """
    equation_parameters1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    equation_parameters2 = [x + '2' for x in equation_parameters1] 
    equation_parameters3 = [x + '3' for x in equation_parameters1] 
    equation_parametersT = ['T1', 'T2', 'T3', 'T4']
    class_parameters = equation_parameters1 + equation_parameters2
    class_parameters += equation_parameters3 + equation_parametersT
    class_parameters.append('dH_std')
    
    def __init__(self, energy_units='eV', pressure_units='Pa'):
        if energy_units not in available_units:
            raise UnitNotFoundError('{} is not a valid unit.'
                                    .format(energy_units))
        self.energy_units = energy_units
        if pressure_units not in available_units:
            raise UnitNotFoundError('{} is not a valid unit.'
                                    .format(pressure_units))
        self.pressure_units = pressure_units
        self.conv_factor = conversion_table['kJ/mol'][self.energy_units]

    def __getattr__(self, attr):
        if attr in self.class_parameters:
            try:
                return self.__dict__[attr]
            except KeyError:
                raise AttributeError('The parameter "{}" '
                                     'must be manually set'.format(attr))
        else:
            return self.__dict__[attr]
        
    def _get_parameters_values(self, T):
        if self.T1 <= T <= self.T2:
            A = self.A
            B = self.B
            C = self.C
            D = self.D
            E = self.E
            F = self.F
            G = self.G
            H = self.H
        elif self.T2 < T <= self.T3:
            A = self.A2
            B = self.B2
            C = self.C2
            D = self.D2
            E = self.E2
            F = self.F2
            G = self.G2
            H = self.H2
        elif self.T3 < T <= self.T4:
            A = self.A3
            B = self.B3
            C = self.C3
            D = self.D3
            E = self.E3
            F = self.F3
            G = self.G3
            H = self.H3
        else:
            raise ValueError('{} is not a valid Temperature for the '
                             'Shomate equation: range {}K to {}K'.format(
                                 T, self.T1, self.T4))
        return (A, B, C, D, E, F, G, H)

    def _H_diff_from_TR_Shomate_Eq(self, T):
        """ The ideal gas molecule enthalpy at standard pressure wrt
        the enthalpy at 298.15 K calculated using the Shomate equation.
        See:
            Chase, M.W., Jr., NIST-JANAF Themochemical Tables, Fourth Edition,
            J. Phys. Chem. Ref. Data, Monograph 9, 1998, 1-1951.

        Result in [kJ/mol]
        """
        t = T/1000
        A, B, C, D, E, F, G, H = self._get_parameters_values(T)
        return A*t + B*t**2/2 + C*t**3/3 + D*t**4/4 - E/t + F - H

    def _H_Shomate_Eq(self, T):
        """ Calculate the molecule enthalpy wrt to 0K using the Shomate
        equation.
        Results in kJ/mol
        """
        return self._H_diff_from_TR_Shomate_Eq(T) - self.dH_std

    def _S_Shomate_Eq(self, T):
        """ Calculates the molecule entropy wrt to 0K using the
        Shomate equation

        Result J/mol/K """
        t = T/1000
        A, B, C, D, E, F, G, H = self._get_parameters_values(T)
        return  A*np.log(t) + B*t + C*t**2/2 + D*t**3/3 - E/(2*t**2) + G

    def G_diff_Shomate_Eq(self, T):
        """ Calculate the standard Gibbs free energy at temperature ``T``
        with respect to the standard one at 0 K using Shomate equation.

        Parameters
        ----------
        T : float
            the temperature

        Returns
        -------
        gibbs_energy : float
            the standard Gibbs free energy at ``T`` in the units
            of :attr:`self.energy_units`
        """
        if type(T) in containers:
            raise TypeError('The temperature must be a scalar')
        # enthalpy at T wrt enthaply at 0 K
        H_diff = self._H_Shomate_Eq(T)
        # entropy at T wrt entropy at 0 K
        S_diff = self._S_Shomate_Eq(T)/1000 # to kJ/mol/K
        G_diff = H_diff - T*S_diff
        return G_diff*self.conv_factor

    def get_ideal_gas_chemical_potential_Shomate(self, mu_standard,
                                                 partial_pressure, T):
        r"""
        Given the standard chemical potential at 0K, e.g. calculated with
        DFT, returns the value at given temperature obtained using the
        Shomate equation and the ideal gas formulas.

        .. math::

            \mu(T, p) = h(0, p^\circ) +
            [g(T, p^\circ) - g(0, p^\circ)] +
             k_BT\ln\left(\frac{p}{p^\circ}\right)

        Parameters
        ----------
        mu_standard : float
            standard-state chemical potential of the molecule at 0K

        partial_pressure : array or float
            the partial pressure

        T : array or float
            the gas temperature

        Returns
        -------
        chem_pot : numpy array/float
            The chemical potentials as a 2D numpy array of shape
            (len(T), len(partial_pressure)) if both T and partial_pressure
            are arrays; otherwise a 1D numpy array of length
            len(partial_pressure)

            if partial_pressure is an array and T a float; otherwise a 2D array
            of shape (len(T), 1) if partial_pressure is a float and T an array;
            finally if both T and partial_pressure are float,
            the result is a float
        """
        if type(T) in containers:
            T = np.array(T)
            T = T[:, np.newaxis]

            G_diff = []
            for temp in T:
                G_diff.append(self.G_diff_Shomate_Eq(temp[0]))
            G_diff = np.array(G_diff)
            chem_pot_vs_T = []
            for i, temp in enumerate(T):
                chem_pot_vs_T.append(ideal_gas_chemical_potential(
                    mu_standard + G_diff[i],
                    partial_pressure, temp[0],
                    energy_units=self.energy_units,
                    pressure_units=self.pressure_units))
            chem_pot_vs_T = np.array(chem_pot_vs_T)
            # keep uniform outputs
            if len(chem_pot_vs_T.shape) < 2:
                chem_pot_vs_T = chem_pot_vs_T[:, np.newaxis]
        else:
            G_diff = self.G_diff_Shomate_Eq(T)
            chem_pot_vs_T = ideal_gas_chemical_potential(
                                mu_standard + G_diff,
                                partial_pressure, T,
                                energy_units=self.energy_units,
                                pressure_units=self.pressure_units)

        return chem_pot_vs_T

class OxygenChemPot(IdealGasChemPot):
    r"""
    Class for modelling the chemical potential of the :math:`\mathrm{O}_2`
    gas molecule

    Parameters
    ----------
    energy_units : string
        the units to be used for the energy

    pressure_units : string
        the units to be used for the pressure
    """
    # Temperature definying the domain of validity of the Shomate Parameters
    T1 = 100
    T2 = 700
    T3 = 2000
    T4 = 6000
    # Parameters for Shomate equation. See NIST-JANAF tables for O2
    # on gas-phase thermochemistry data
    # 100-700 K range
    A = 31.32234
    B = -20.23531
    C = 57.86644
    D = -36.50624
    E = -0.007374
    F = -8.903471
    G = 246.7945
    H = 0
    # 700 - 2000K range
    A2 = 30.0323
    B2 = 8.772972
    C2 = -3.988133
    D2 = 0.788313
    E2 = -0.741599
    F2 = -11.32468
    G2 = 236.1663
    H2 = 0
    # 2000 - 6000K range
    A3 = 20.91111
    B3 = 10.72071
    C3 = -2.020498
    D3 = 0.146449
    E3 = 9.245722
    F3 = 5.337651
    G3 = 237.6185
    H3 = 0

    # exp standard enthalpy at 0K wrt value at 298.15K
    # kJ/mol, still found on NIST-JANAF tables for O2
    dH_std = -8.683

class NitrogenChemPot(IdealGasChemPot):
    r"""
    Class for modelling the chemical potential of the :math:`\mathrm{N}_2`
    gas molecule

    Parameters
    ----------
    energy_units : string
        the units to be used for the energy

    pressure_units : string
        the units to be used for the pressure
    """
    # Temperature definying the domain of validity of the Shomate Parameters
    T1 = 100
    T2 = 500
    T3 = 2000
    T4 = 6000
    # Parameters for Shomate equation. See NIST-JANAF tables for N2
    # on gas-phase thermochemistry data
    # 100-500 K range
    A = 28.98641
    B = 1.853978
    C = -9.647459
    D = 16.63537
    E = 0.000117
    F = -8.671914
    G = 226.4168
    H = 0.0
    # 500 - 2000K range
    A2 = 19.50583
    B2 = 19.88705
    C2 = -8.598535
    D2 = 1.369784
    E2 = 0.527601
    F2 = -4.935202
    G2 = 212.3900
    H2 = 0.0
    # 2000 - 6000K range
    A3 = 35.51872
    B3 = 1.128728
    C3 = -0.196103
    D3 = 0.014662
    E3 = -4.553760
    F3 = -18.97091
    G3 = 224.9810
    H3 = 0.0

    # exp standard enthalpy at 0K wrt value at 298.15K
    # kJ/mol, still found on NIST-JANAF tables for N2
    dH_std = -8.670

class ChlorineChemPot(IdealGasChemPot):
    r"""
    Class for modelling the chemical potential of the :math:`\mathrm{Cl}_2`
    gas molecule

    Parameters
    ----------
    energy_units : string
        the units to be used for the energy

    pressure_units : string
        the units to be used for the pressure
    """
    # Temperature definying the domain of validity of the Shomate Parameters
    T1 = 298
    T2 = 1000
    T3 = 3000
    T4 = 6000
    # Parameters for Shomate equation. See NIST-JANAF tables for Cl2
    # on gas-phase thermochemistry data
    # 298-1000 K range
    A = 33.05060
    B = 12.22940
    C = -12.06510
    D = 4.385330
    E = -0.159494
    F = -10.83480
    G = 259.0290
    H = 0.0
    # 1000 - 3000K range
    A2 = 42.67730
    B2 = -5.009570
    C2 = 1.904621
    D2 = -0.165641
    E2 = -2.098480
    F2 = -17.28980
    G2 = 269.8400
    H2 = 0.0
    # 3000 - 6000K range
    A3 = -42.55350
    B3 = 41.68570
    C3 = -7.126830
    D3 = 0.387839
    E3 = 101.1440
    F3 = 132.7640
    G3 = 264.7860
    H3 = 0.0

    # exp standard enthalpy at 0K wrt value at 298.15K
    # kJ/mol, still found on NIST-JANAF tables for Cl2
    dH_std = -9.181

class FluorineChemPot(IdealGasChemPot):
    r"""
    Class for modelling the chemical potential of the :math:`\mathrm{F}_2`
    gas molecule

    Parameters
    ----------
    energy_units : string
        the units to be used for the energy

    pressure_units : string
        the units to be used for the pressure
    """
    # Temperature definying the domain of validity of the Shomate Parameters
    T1 = 298
    T2 = 1000
    T3 = 3000
    T4 = 6000
    # Parameters for Shomate equation. See NIST-JANAF tables for F2
    # on gas-phase thermochemistry data
    # 298-1000 K range
    A = 31.44510
    B = 8.413831
    C = -2.778850
    D = 0.218104
    E = -0.211175
    F = -10.43260
    G = 237.2770
    H = 0.0
    # 1000 - 3000K range
    A2 = A
    B2 = B
    C2 = C
    D2 = D
    E2 = E
    F2 = F
    G2 = G
    H2 = H
    # 3000 - 6000K range
    A3 = A
    B3 = B
    C3 = C
    D3 = D
    E3 = E
    F3 = F
    G3 = G
    H3 = H

    # exp standard enthalpy at 0K wrt value at 298.15K
    # kJ/mol, still found on NIST-JANAF tables for F2
    dH_std = -8.825

class HydrogenChemPot(IdealGasChemPot):
    r"""
    Class for modelling the chemical potential of the :math:`\mathrm{H}_2`
    gas molecule

    Parameters
    ----------
    energy_units : string
        the units to be used for the energy

    pressure_units : string
        the units to be used for the pressure
    """
    # Temperature definying the domain of validity of the Shomate Parameters
    T1 = 298
    T2 = 1000
    T3 = 2500
    T4 = 6000
    # Parameters for Shomate equation. See NIST-JANAF tables for H2
    # on gas-phase thermochemistry data
    # 298-1000 K range
    A = 33.066178
    B = -11.363417
    C = 11.432816
    D = -2.772874
    E = -0.158558
    F = -9.980797
    G = 172.707974
    H = 0.0
    # 1000 - 2500K range
    A2 = 18.563083
    B2 = 12.257357
    C2 = -2.859786
    D2 = 0.268238
    E2 = 1.977990
    F2 = -1.147438
    G2 = 156.288133
    H2 = 0.0
    # 2500 - 6000K range
    A3 = 43.413560
    B3 = -4.293079
    C3 = 1.272428
    D3 = -0.096876
    E3 = -20.533862
    F3 = -38.515158
    G3 = 162.081354
    H3 = 0.0

    # exp standard enthalpy at 0K wrt value at 298.15K
    # kJ/mol, still found on NIST-JANAF tables for H2
    dH_std = -8.467

# book keeping of all ideal gases classes implemented here
available_ideal_gases = dict(O2=OxygenChemPot, N2=NitrogenChemPot,
                             Cl2=ChlorineChemPot, F2=FluorineChemPot,
                             H2=HydrogenChemPot)

class Range:
    r"""
    Class for finding the allowed ranges for the chemical potentials
    of given elements given the competing phases.

    Parameters
    ----------
    coeff_equalities : 2D tuples
        the coefficients of the linear equalities.
        For each equality there should be an array with
        the corresponding coefficients.
        **Each element in the tuple must contain the same
        number of elements**. If a variable appears at
        least once in the constraint equations,
        it must be set to 0 in all the other equations.

    const_equalities : 1D tuple
        the constant values of the linear equalities.
        const_equalities[i] has to be the constant value
        of the linear equation with coefficients
        coeff_equalities[i].

        Example:

            We have the linear constraints given by these equations:

            .. math::
                :nowrap:

                \begin{align*}
                ax + by + cz &= d \\
                a'x + b'y + c'z &= d' \\
                a''x + b''y = d'' 
                \end{align*}

            then:
                coeff_equalities = ((a,b,c), (a', b', c'), (a'', b'', 0))

                const_equalities = (d, d', d'')

            .. warning::

                If a variable is present **anywhere** in either the equality
                or inequality constraints, then it must be explicitly given
                even if its value is zero (the coefficient of z in the
                last equation of the previous example).

        coeff_inequalities and const_inequalities are analogously defined,
        but for the inequality conditions.

    bounds : tuple of tuples
        the bounds of the independent variables. If not present,
        they will be set to (None, None) for each independent variable,
        which will be treated as -inf and +inf

    Attributes
    ----------
    number_of_variables : int
        number of chemical potentials

    variables_extrema : 2D numpy array
        shape = (number elements, 2)
        for each element, returns the minimum and maximum possible values
        for its chemical potential

    variables_extrema_2d : 2D numpy array
        shape = (2, 2)
        for each element, returns the minimum and maximum possible values
        for its chemical potential. Calculated after an intersection with a plane
        has been performed.

    mu_labels : tuple
        the symbols labeling the elements for which we caculate the chemical
        potentials

    Notes
    -----
    **ALL INEQUALITIES SHOULD BE IN THE FORM:**

        coeff_inequalities * x <= const_inequalities

    Examples
    --------
    Suppose that we want to find the chemical potential extrema for Ti and O in
    rutile TiO2.

    We have the following constraints:

    .. math::
        :nowrap:
  
        \begin{align*}
        \mu_\mathrm{Ti} + 2\mu_\mathrm{O} &= \mu_\mathrm{TiO_2}\\
        \mu_\mathrm{Ti} + \mu_\mathrm{O} &\leq \mu_\mathrm{TiO}\\
        2\mu_\mathrm{Ti} + 3\mu_\mathrm{O} &\leq \mu_\mathrm{Ti_2O_3}\\
        \mu_\mathrm{Ti} &\leq \mu_\mathrm{Ti}(HCP)\\
        \mu_\mathrm{O} &\leq \frac{1}{2} \mu_\mathrm{O_2}
        \end{align*}

    So, we will have to type:

        >>> coeff_equalities = ((1,2))
        >>> const_equalities = (mu_TiO2, )
        >>> coeff_inequalities = ((1, 1), (2, 3))
        >>> const_inequalities = (mu_TiO, mu_Ti2O3)
        >>> bounds = ((None, mu_Ti(HCP)), (None, 1/2 mu_O2))
    """
    def __init__(self,
                 coeff_equalities, const_equalities,
                 coeff_inequalities, const_inequalities,
                 bounds):
        if coeff_equalities is None and const_equalities is None:
            self.coeff_equalities = None
            self.const_equalities = None
        else:
            self.coeff_equalities = tuple(tuple(x) for x in coeff_equalities)
            self.const_equalities = tuple(const_equalities)
        if coeff_inequalities is None and const_inequalities is None:
            self.coeff_inequalities = None
            self.const_inequalities = None
        else:
            self.coeff_inequalities = tuple(tuple(x) for x in  coeff_inequalities)
            self.const_inequalities = tuple(const_inequalities)
        if bounds is None:
            self.bounds = None
        else:
            self.bounds = tuple(tuple(x) for x in bounds)

        if (self.coeff_equalities  and
            len(self.coeff_equalities) != len(self.const_equalities)):
            raise ValueError('Number of equality coefficients does not match '
                             'the number of equality constants')
        if (self.coeff_inequalities and
            len(self.coeff_inequalities) != len(self.const_inequalities)):
            raise ValueError('Number of inequality coefficients '
                             'does not match the number of '
                             'inequality constants')

        self._no_variables = np.max([len(self.coeff_equalities[0]),
                                    len(self.coeff_inequalities[0])])

        self._coeff_equalities_tmp = np.array(self.coeff_equalities)
        self._const_equalities_tmp = np.array(self.const_equalities)
        self._coeff_inequalities_tmp = np.array(self.coeff_inequalities)
        self._const_inequalities_tmp = np.array(self.const_inequalities)

        # check bounds
        if not self.bounds:
            self.bounds = ((None, None) for
                           x in range(self._no_variables))
        else:
            if len(self.bounds) != self._no_variables:
                raise ValueError('Found {} variables and {} variable bounds. '
                                 'Variable bounds must be specified for '
                                 'all compounds or None.'.format(
                                     self._no_variables, len(self.bounds)))
        # self.variables_extrema[i][0] = minimum value of variable i
        # self.variables_extrema[i][1] = maximum value of variable i
        self._variables_extrema_global = None
        self.equality_compounds = None
        self.inequality_compounds = None
        self.bound_compounds = None

        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.Set1.colors)
        self._color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

    @property
    def number_of_variables(self):
        return self._no_variables

    @property
    def variables_extrema(self):
        if self._variables_extrema_global is None:
            val = self._find_variables_extrema(self.coeff_inequalities,
                                               self.const_inequalities,
                                               self.coeff_equalities,
                                               self.const_equalities,
                                               self.bounds, self._no_variables)
            self._variables_extrema_global = val
        return self._variables_extrema_global.copy()

    @property
    def variables_extrema_2d(self):
        return self._variables_extrema.copy()

    @property
    def mu_labels(self):
        if hasattr(self, '_mu_labels'):
            return self._mu_labels
        raise ValueError('The labels of the chemical potentials '
                         'have not been set. Use '
                         '"set_chemical_potential_labels"')

    def set_color_map(self, cmap):
        """ Set the color map to be used in the plot

        Parameters
        ----------
        cmap : matplotlib.cm class
            one of the color maps offered by matplotlib.
            By default Set1 is used, which is fine when
            less than 10 compounds are considered
        """
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=cmap.colors)
        self._color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

    def set_chemical_potential_labels(self, labels):
        """ Set the name of the independent variables.

        Parameters
        ----------
        labels : list
            the names of the independent variables, one should use the
            same order used in ``self.coeff_*``
        """
        if len(labels) != self._no_variables:
            raise ValueError('Number of labels does not agree with '
                             'the number of independent variables')

        self._mu_labels = tuple(labels)

    def set_compound_dict(self, compounds_dict):
        """ Set a dictionary which contains the compound names relative to
        the equality, inequality and bound conditions.

        Valid names are: formula + _ + description.

        description is any string that described the compound

        Note:
            Note that the validity of the name format is not
            checked internally and should be done by the user.

        compounds_dict : dict

            .. code-block::

                {'equality' : [compoundA1, ...],
                 'inequality' : [compound1, ...],
                 'bound' : [compoundA, ...]}

            the order of the elements in the dictionary values has
            to be the same of the order used in the relative
            ``const_equalities``, ``const_inequalities``
            and ``bounds`` lists
        """
        try:
            self.equality_compounds = tuple(compounds_dict['equality'])
        except KeyError:
            self.equality_compounds = None
        try:
            self.inequality_compounds = tuple(compounds_dict['inequality'])
        except KeyError:
            self.inequality_compounds = None
        try:
            self.bound_compounds = tuple(compounds_dict['bound'])
        except KeyError:
            self.bound_compounds = None

    def _find_min_variable(self, variable_function, ineq_coeffs, ineq_const,
                           eq_coeffs, eq_const, bounds):
        """ MINIMIZES an independent variable with the constraints

        Parameter:
        ----------
        variable_function : list
            1 corresponds to the variable that we want to
            minimize, all other variables have to be set to 0

            Example:

                We have the independent variables x,y,z and we
                want to minimize y. Then variable_function = [0,1,0]
        """
        # the element where 1 appears is the index of the variable we want
        variable_index = variable_function.index(1)
        variable_function = np.array(variable_function)
        res = linprog(variable_function,
                      A_ub=ineq_coeffs,
                      b_ub=ineq_const,
                      A_eq=eq_coeffs,
                      b_eq=eq_const,
                      bounds=bounds,
                      method='interior-point',
                      options={'sym_pos':False})
        if res.success:
            self._variables_extrema[variable_index][0] = res.fun
        else:
            if res.status == 3:
                self._variables_extrema[variable_index][0] = -np.inf
            else:
                raise ValueError('No optimal solution could be found '
                                 'for minimizing variable number {}. '
                                 'Error no. {}'
                                 .format(variable_index,
                                         res.status))

    def _find_max_variable(self, variable_function, ineq_coeffs, ineq_const,
                           eq_coeffs, eq_const, bounds):
        """ MAXIMIZES an independent variable with the constraints

        Parameters
        ----------
        variable_function : list
            1 corresponds to the variable that we want to
            minimize, all other variables have to be set to 0

            Example:

                We have the independent variables x,y,z and we
                want to minimize y. Then variable_function = [0,1,0]
        """
        # Note the minus signs
        variable_index = variable_function.index(1)
        variable_function = np.array(variable_function)
        res = linprog(-variable_function,
                      A_ub=ineq_coeffs,
                      b_ub=ineq_const,
                      A_eq=eq_coeffs,
                      b_eq=eq_const,
                      bounds=bounds,
                      method='interior-point',
                      options={'sym_pos':False})
        if res.success:
            self._variables_extrema[variable_index][1] = -res.fun
        else:
            if res.status == 3:
                self._variables_extrema[variable_index][1] = np.inf
            else:
                raise ValueError('No optimal solution could be found '
                                 'for maximizing variable number {}. '
                                 'Error no. {}'
                                 .format(variable_index,
                                         res.status))

    def _find_variables_extrema(self, ineq_coeffs, ineq_const,
                                eq_coeffs, eq_const, bounds, no_vars):
        """ Finds the maximum and minimum for each variable """
        self._variables_extrema = np.zeros((no_vars, 2),
                                           dtype=np.float64)
        base = [0]*no_vars
        base[0] = 1
        variables_functions = set(list(itertools.permutations(base)))
        for funct in variables_functions:
            variable_function = list(funct)
            self._find_min_variable(variable_function, ineq_coeffs, ineq_const,
                                    eq_coeffs, eq_const, bounds)
            self._find_max_variable(variable_function, ineq_coeffs, ineq_const,
                           eq_coeffs, eq_const, bounds)
        return self._variables_extrema

    def check_value_variables(self, variables, eq_tol=1e-6):
        """
        Checks whether a set of variables is within the feasible
        region.

        Parameters
        ----------
        variables : array
            the length is given by :attr:`no_variables`: the number of
            elements in the system

        eq_tol : float
            tolerance on equality conditions

        Returns
        -------
        result : tuple
            a booleand and a numpy array of shape
            :attr:`self.no_variables` times the number of constraints

            - First element:

                  True, if ``variables`` is within the feasible region,
                  False, otherwise.

            - Second element:

                  Array of shape:
                  :attr:`no_variables` times the number of constraints
                  where the number of contraints is the number of equalities
                  plus inequalities plus bounds conditions.

                  This array is a 2D array whose rows represent the
                  variables and whose columns represents the various
                  constraints, the order is:

                  equalities, inequalities and bound down, bound up

                  in the same order given by the user at initialization.
                  The values of such matrices are bool.

                  Example:

                      Suppose we have two variables, one equality and two
                      inequality and 2 bounds constraints.
                      If both variables satisfy the equality,
                      first inequality and bounds. But variable 2 does not
                      satisfy the second inequality; the funcion will return
                      a np.ndarray ``result`` of shape (2,5):

                      .. code-block::

                          result = [[True, True, True, True, True],
                                    [True, True, False, True, True]]
        """
        if not isinstance(variables, np.ndarray):
            variables = np.array(variables)

        if variables.ndim > 1:
            raise ValueError('The input must be a 1D array')

        # equalities
        A_eq = np.array(self.coeff_equalities)
        b_eq = np.array(self.const_equalities)
        no_eq = len(b_eq)
        # inequalities
        A_ub = np.array(self.coeff_inequalities)
        b_ub = np.array(self.const_inequalities)
        no_ub = len(b_ub)

        s = variables.shape[0]

        # s has to be the number of variables, it is not accepted an input
        # which does not specify the value of each variable
        if  s != self._no_variables:
            raise ValueError('A value for each variable has to be specified')
        # equalitites, inequalities, bond bottom ,bound up
        no_tot = no_eq + no_ub + 2

        validity = np.full((s, no_tot), False, dtype=bool)

        # check for the bounds

        bounds_down = np.zeros(s, dtype=np.float64)
        bounds_up = np.zeros_like(bounds_down)
        for i, (v_min, v_max) in enumerate(self.bounds):
            if v_min or v_min == 0: # 0 is False
                bounds_down[i] = v_min
            else:
                bounds_down[i] = -np.inf
            if v_max or v_max == 0:
                bounds_up[i] = v_max
            else:
                bounds_up[i] = np.inf
        validity[:, -2] = variables >= bounds_down
        validity[:, -1] = variables <= bounds_up

        eq = np.abs(np.dot(variables, A_eq.T) - b_eq) < eq_tol
        # we need to repeat the result for each variable in the
        # case of equalities and inequalities
        validity[:, :no_eq] = np.tile(eq, s).reshape(s, -1)

        ineq = np.dot(variables, A_ub.T) <= b_ub
        validity[:, no_eq:no_eq+no_ub] = np.tile(ineq, s).reshape(s, -1)

        return validity.all(), validity

    def _get_plot_dict(self, intersection):
        labels_ineq = self.inequality_compounds
        labels_bounds = self.bound_compounds
        if labels_ineq is None:
            raise ValueError('The labels of the compounds giving the '
                             'inequality conditions are not set. '
                             'Use "self.set_compound_dict"')
        if labels_bounds is None:
            raise ValueError('The labels of the compounds giving the boundary '
                             'values are not set. Use '
                             '"self.set_compound_dict"')
        symbol1 = get_formula_unit(labels_bounds[intersection[0]])
        symbol2 = get_formula_unit(labels_bounds[intersection[1]])

        compounds_dict = defaultdict(list)
        coeff_compounds = tuple([tuple(x) for x
                                 in self._coeff_inequalities_tmp]) + (0, 1)
        list_compounds = (labels_ineq +
                          (labels_bounds[intersection[0]],
                           labels_bounds[intersection[1]])
                         )
        const_ineq = tuple([x for x in self._const_inequalities_tmp])
        energy_compounds = (const_ineq +
                            (self.bounds[intersection[0]][1],
                             self.bounds[intersection[1]][1])
                           )
        for ii, energy in enumerate(energy_compounds):
            try: # a label for a compound is taken to be in general something
                 # like: Formula_other strings
                formula, ids = list_compounds[ii].split('_')
                ids = ids.lower()
            except ValueError:
                formula = list_compounds[ii]
                ids = formula
            name = ' '.join(list_compounds[ii].split('_'))
            if ii < len(const_ineq):
                no_1 = coeff_compounds[ii][intersection[0]]
                no_2 = coeff_compounds[ii][intersection[1]]
            else:
                if coeff_compounds[ii] == 0: # variable 1
                    no_1 = 1
                    no_2 = 0
                else: # variable 2
                    no_1 = 0
                    no_2 = 1
            key = (no_1, no_2)
            compounds_dict[key].append((energy, name))
        return compounds_dict

    def _get_intersection_points(self, intersection, tol):
        """ Find the points where the line representing the compound
        stoichiometries intersect on a given point.
        The independent variables are indexed in `intersection`
        """
        N_var = len(self._const_inequalities_tmp)
        bounds = np.array(self.bounds)[intersection]
        A_ub = self._coeff_inequalities_tmp[:, intersection]
        b_ub = self._const_inequalities_tmp
        points = []
        # limits feasible region, same bounds
        for j in range(N_var):
            for k in range(2):
                if k == 0:
                    c = [1, 0]
                elif k == 1:
                    c = [0, 1] 
                A_eq = A_ub[j]
                b_eq = b_ub[j]
                if A_eq.ndim == 1:
                    A_eq = A_eq[np.newaxis, :]
                    b_eq = [b_eq]    
                tmp_A_ub = np.delete(A_ub, [j], axis=0)
                tmp_b_ub = np.delete(b_ub, [j], axis=0)
                solve = linprog(c, A_ub=tmp_A_ub, b_ub=tmp_b_ub,
                                A_eq=A_eq, b_eq=b_eq, bounds=bounds,
                                method='simplex')
                if solve.status == 0 or solve.status == 1:
                    point = solve.x
                elif solve.status == 2:
                    point = np.zeros(2)
                else:
                    continue
                points.append(point)
        c = np.array([1, 0])
        solve = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds,
                        method='simplex')
        if solve.status == 0 or solve.status == 1:
            points.append(solve.x)
        elif solve.status == 2:
            points.append(np.zeros(2))
        c = np.array([0, 1])
        solve = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds,
                        method='simplex')
        if solve.status == 0 or solve.status == 1:
            points.append(solve.x)
        elif solve.status == 2:
            points.append(np.zeros(2))
        points = np.unique(points, axis=0)
        return points

    def _get_limit_lines(self, edges_points, compounds_dict, tol):
        # retrieve the limit lines
        xx = edges_points[0]; yy = edges_points[1]
        lines = defaultdict(list)
        for ii in range(len(xx) - 2):
            x1 = xx[ii]; x2 = xx[ii+1]
            y1 = yy[ii]; y2 = yy[ii+1]
            if x1 == x2 and y1 == y2: # just a point
                continue
            if np.abs(x2-x1) > 1e-6:
                slope = (y2-y1)/(x2-x1)
                q = y1 - slope*x1
            else: # x = something
                slope = np.inf
                q = -np.inf
            # find which compound originates this line
            for key in compounds_dict.keys():
                comp = compounds_dict[key]
                for cc in comp:
                    energy, label = cc

                    if (abs(key[1]) > tol):
                        comp_slope = -key[0]/key[1]
                        comp_q = energy/key[1]
                    elif (abs(key[0]) > tol): # x = c
                        comp_slope = np.inf
                        comp_q = -np.inf

                    to_append = False
                    if ((comp_slope is slope) and (comp_q is q)):
                        to_append = True
                    elif ((abs(comp_slope - slope) < tol) 
                          and ((abs(comp_q - q) < tol))):
                        to_append = True 
                    if to_append:
                        label = label.split()
                        formula = label[0]
                        regex = re.compile(r'([A-Z][a-z]?)([0-9]*)')
                        groups_comp = re.findall(regex, formula)
                        name = r''
                        for g in groups_comp:
                            if g[1]:
                                name += g[0] + r'$_{' + g[1] + r'}$'
                            else:
                                name += g[0]
                        try:
                            label = ' '.join([name, label[1]])
                        except IndexError:
                            label = name
                        lines[label].append(([x1, x2], [y1, y2], label))
        return lines

    def _intersect_values(self, plane_axes, plane_values=None):
        """ The equalities and inequalities consditions at the
        intersection plane.

        Parameters
        ----------
        plane_axes : 1D array of length 2
            the array specifies the indices of the variables which will
            form the axes of the plane with which the intersection will
            take place.

        plane_values : 1D array of length self.number_of_variables - 2
            For example, if we are considering a ternary system A, B, C,
            and we want to intersect with the plane (A,C), B = b, then
            plane_axes = [0, 2], plane_values = [b]
            By default the array will be filled with zeros.
        """
        all_args = np.arange(self.number_of_variables)
        rem_args = list(set(all_args) ^ set(plane_axes))
        if rem_args:
            rem_args = np.sort(rem_args)
        else:
            return
        if plane_values is None:
            plane_values = np.zeros_like(rem_args)
        else:
            plane_values = np.array(plane_values)
        values = self._coeff_inequalities_tmp[:, rem_args]*plane_values
        self._const_inequalities_tmp = self.const_inequalities - values.ravel()
        values = self._coeff_equalities_tmp[:, rem_args]*plane_values
        self._const_equalities_tmp = self.const_equalities - values.ravel()

    def _find_feasible_region_grid(self, xx, yy, plane_axes):
        """ Find the feasible region given a grid of points
        Note: be sure to have projected the feasible region beforhand.
        This function should not be used outside the main plotting function """
        conditions = []
        for j, cond in enumerate(self._coeff_inequalities_tmp[:, plane_axes]):
            con = (cond[0]*xx + cond[1]*yy <= self._const_inequalities_tmp[j])
            conditions.append(con)
        # add bounds
        conditions.extend([(xx <= 0), (yy <= 0)])
        region = conditions[0]
        for cond in conditions[1:]:
            region = region & cond
        return region

    def plot_feasible_region_on_plane(self, plane_axes,
                                      plane_values=None,
                                      save_plot=False, tol=1e-6, **kwargs):
        """ Plot the feasibile region intersection with the plane specified by
        ``plane_axes``.

        Parameters
        ----------
        plane_axes : 1D array of length 2
            the array specifies the indices of the variables which will
            form the axes of the intersection plane.

        plane_values : 1D array of length self.number_of_variables - 2
            Constant value specifying the plane.

        save_plot : bool
            if True, the plot will be saved

        tol : float
            a numerical tolerance for determining the points
            giving the feasible region

        kwargs : dict, optional
            optional key:value pairs for plotting the diagram

        Returns
        -------
        the figure instance of the plot.

        Example
        -------
        For example, if we are considering a ternary system A, B, C,
        and we want to intersect the feasible region with
        the plane B = b, using the axes given by variables A and B, then
        plane_axes = [0, 2], plane_values = [b]. 
        This specifies the plane :math:`B = b`.

        By default `plane_values` is filled with zeros.
        """
        if len(self.bounds) != self.number_of_variables:
            raise ValueError('The bounds of all {} variables '
                             'must be explicitly given in order to '
                             'plot the feasible region'.format(
                                 self.number_of_variables))
        try:
            no_axes = len(plane_axes)
        except TypeError:
            print('Error: plane_axes must be an array!')
        if no_axes != 2:
            raise ValueError('Error: exactly 2 plane axes '
                             'must be specified ')
        if plane_values is not None:
            try:
                len(plane_values)
            except TypeError:
                raise TypeError('Error: plane_values must be an array '
                      'even for one variable!')
            no_items = self.number_of_variables - len(plane_axes)
            if len(plane_values) > no_items:
                raise ValueError('Too many elements in plane_values!')
            elif len(plane_values) < no_items:
                raise ValueError('Too few elements in plane_values!')
        self._intersect_values(plane_axes, plane_values)
        # relevant lines in this plane
        compounds_dict = self._get_plot_dict(plane_axes)
        figsize = kwargs.pop('figsize', (10, 10))
        title = kwargs.pop('title', '')
        save_title = kwargs.pop('save_title', None)
        x_val_min = kwargs.pop('x_val_min', None)
        y_val_min = kwargs.pop('y_val_min', None)
        x_val_max = kwargs.pop('x_val_max', None)
        y_val_max = kwargs.pop('y_val_max', None)
        linewidth = kwargs.pop('linewidth', 3)
        try:
            x_lab = self.mu_labels[plane_axes[0]]
            y_lab = self.mu_labels[plane_axes[1]]
        except ValueError:
            x_lab = 'x'
            y_lab = 'y'
        x_label = kwargs.pop('x_label', x_lab)
        y_label = kwargs.pop('y_label', y_lab)
        fsize = kwargs.pop('fontsize', 26)
        plt.rcParams.update({'font.size': fsize})
        labels_eq = self.equality_compounds
        if labels_eq is None:
            raise ValueError('The labels of the compounds giving the equality '
                             'conditions are not set. Use '
                             '"self.set_compound_dict"')
        points = self._get_intersection_points(plane_axes, tol)
        valid_points = []
        fact = 1
        for point in points:
            condition = (point[0] == -np.inf or point[1] == -np.inf)
            if not condition:
                valid_points.append(point)
            else:
                fact = 2
        points = valid_points
        bounds_max = [bound[1] for bound in self.bounds]

        fig = plt.figure(figsize=figsize)
        ax = plt.gca()
        if title:
            fig.suptitle(title, fontsize=fsize+2)
            ax.title.set_position([.5, 1.10])

        if x_val_min is None:
            x_vals = [x[0] for x in points]
            x_val_min = np.min(x_vals)
            if x_val_min <= 0:
                 x_val_min *= fact*1.5
            elif x_val_min > 0:
                x_val_min *= fact*0.5
        if y_val_min is None:
            y_vals = [x[1] for x in points]
            y_val_min = np.min(y_vals)
            if y_val_min <= 0:
                y_val_min *= fact*1.5
            elif y_val_min > 0:
                y_val_min *= fact*0.5

        if x_val_max is None:
            x_val_max = bounds_max[plane_axes[0]]
            if x_val_max <= 0:
                x_val_max *= 1.5
            elif x_val_max > 0:
                x_val_max *= 0.5
        if y_val_max is None:
            y_val_max = bounds_max[plane_axes[1]]
            if y_val_max <= 0:
                y_val_max *= 1.5
            elif y_val_max > 0:
                y_val_max *= 0.5

        if x_val_min == x_val_max:
            raise RuntimeError('Not enough points for estimating the range '
                               'of {}, set "x_val_min"/"x_val_max" '
                               'manually'.format(x_label))
        if y_val_min == y_val_max:
            raise RuntimeError('Not enough points for estimating the range '
                               'of {}, set "y_val_min"/"y_val_max" '
                               'manually'.format(y_label))
        max_points = 2000
        deltad = kwargs.pop('resolution', 1e-4)
        x_points = (x_val_max - x_val_min)/deltad
        y_points = (y_val_max - y_val_min)/deltad
        while (x_points > max_points or y_points > max_points):
            deltad *= 1.5
            x_points = (x_val_max - x_val_min)/deltad
            y_points = (y_val_max - y_val_min)/deltad
        xd = np.linspace(x_val_min, x_val_max, int(x_points))
        yd = np.linspace(y_val_min, y_val_max, int(y_points))
        xx, yy = np.meshgrid(xd, yd)
        region = self._find_feasible_region_grid(xx, yy, plane_axes)
        ax.imshow(region.astype(int), cmap='Greys', origin='lower', alpha=0.3,
                  extent=(xx.min(), xx.max(), yy.min(), yy.max()),
                  zorder=0)
        # find the compounds giving the edges of the polygon
        lines = defaultdict(list)
        dtol = deltad
        for key in compounds_dict.keys():
            comp = compounds_dict[key]
            # coefficients of the line
            cx, cy = key
            for cc in comp:
                energy, label = cc
                vals = np.abs(cx*xx + cy*yy - energy) <= dtol/2
                in_region = region & vals
                if in_region.any():
                    x1 = np.min(xx[in_region])
                    x2 = np.max(xx[in_region])
                    y1 = np.min(yy[in_region])
                    y2 = np.max(yy[in_region])
                    # finer grid
                    # for lines not parallel to axes
                    if cx != 0 and cy != 0: 
                        new_deltad = deltad/20
                        new_x_points = abs(x2 - x1)/new_deltad
                        new_y_points = abs(y2 - y1)/new_deltad
                        while (new_x_points > max_points or
                               new_y_points > max_points):
                            new_deltad *= 1.5
                            new_x_points = abs(x2 - x1)/new_deltad
                            new_y_points = abs(y2 - y1)/new_deltad
                        xd = np.linspace(x1, x2, int(new_x_points))
                        yd = np.linspace(y1, y2, int(new_y_points))
                        nxx, nyy = np.meshgrid(xd, yd)
                        new_region = self._find_feasible_region_grid(nxx, nyy,
                                                                     plane_axes)
                        new_vals = np.abs(cx*nxx + cy*nyy - energy) <= new_deltad/2
                        in_region = new_region & new_vals
                        try:
                            x1 = np.min(nxx[in_region])
                            x2 = np.max(nxx[in_region])
                            y1 = np.min(nyy[in_region])
                            y2 = np.max(nyy[in_region])
                        except ValueError:
                            # it might happen that points are not found
                            # on the finer grid
                            pass
                    elif cx == 0:
                        y2 = y1
                    elif cy == 0:
                        x1 = x2
 
                    label = label.split()
                    formula = label[0]
                    regex = re.compile(r'([A-Z][a-z]?)([0-9]*)')
                    groups_comp = re.findall(regex, formula)
                    name = r''
                    for g in groups_comp:
                        if g[1]:
                            name += g[0] + r'$_{' + g[1] + r'}$'
                        else:
                            name += g[0]
                    try:
                        label = ' '.join([name, label[1]])
                    except IndexError:
                        label = name
                    lines[label].append(([x1, x2], [y2, y1], label))
        tot_lines = len(lines.keys())
        if tot_lines > len(self._color_cycle):
            self.set_color_map(plt.cm.tab20)
        for i, line_lab in enumerate(lines.keys()):
            for j, line in enumerate(lines[line_lab]):
                if j == 0:
                    ax.plot(line[0], line[1], label=line[2],
                            color=self._color_cycle[i], linewidth=linewidth)
                else:
                    ax.plot(line[0], line[1], color=self._color_cycle[i],
                            linewidth=linewidth)
        # plot the equality condition and variables extrema
        for line_coeff, line_const in zip(self._coeff_equalities_tmp,
                                          self._const_equalities_tmp):
            coeffs = line_coeff[plane_axes]
            if coeffs[1] == 0 and coeffs[0] != 0: # x = something
                ax.axvline(line_const/coeffs[0], color='black', linewidth=2,
                           zorder=10)
            elif coeffs[0] == 0 and coeffs[1] != 0: # y = something
                ax.axhline(line_const/coeffs[1], color='black', linewidth=2,
                           zorder=10)
            else:
                x_vals = np.linspace(x_val_min, x_val_max)  
                ax.plot(x_vals,
                        line_const/coeffs[1] - coeffs[0]*x_vals/coeffs[1],
                        color='black', linewidth=2)
        ineq_coeffs = self._coeff_inequalities_tmp[:, plane_axes]
        ineq_const = self._const_inequalities_tmp
        eq_coeffs = self._coeff_equalities_tmp[:, plane_axes]
        eq_const = self._const_equalities_tmp
        bounds = np.array(self.bounds)[plane_axes]
        try:
            values = self._find_variables_extrema(ineq_coeffs, ineq_const,
                                                  eq_coeffs, eq_const,
                                                  bounds, 2)
            ax.scatter(values[0, 0], values[1, 1], color='black', zorder=10)
            ax.scatter(values[0, 1], values[1, 0], color='black', zorder=10)
        except ValueError:
            pass

        plt.legend(prop={'size':fsize-4}, loc='best')
        ax.set_xlim(x_val_min, x_val_max)
        ax.set_ylim(y_val_min, y_val_max)
        ax.set_xlabel(x_label); ax.set_ylabel(y_label)
        fig.tight_layout()
        if save_plot:
            if save_title is None:
                title = ('feasible_region_plane_' +
                         '_'.join([str(x) for x in plane_axes]) + '.pdf')
            else:
                title = save_title + '.pdf'
            plt.savefig(title)
        plt.show()
        fig.clf()


def parse_mu_from_string(string, delimiter=None):
    """ Reads and parses a string and returns a dictionary with the elements,
    coefficients, and the constants of the equality/inequality conditions.

    Parameters
    ----------
    string : str
        the string that has to be parsed. The format has to be:
        ``Formula_unit(delimiter)Energy_of_the_compound_per_fu # comments``

       Example:
           SrTiO3    -12.3

           will return:

           ``result = {'Sr':1/5, 'Ti':1/5, 'O':3/5, 'energy':-12.3}``

    delimiter : str
        the symbol used to separate compound names from energy values

    Returns
    -------
    result : dict
        as in the example above
    """
    result = {}
    re_spec = re.compile(r'([A-Z][a-z]?)([0-9]*)')
    l = string.strip().split(delimiter)
    if len(l) != 2:
        if len(l) > 2:
            if l[2].startswith('#'):
                l_t = []
                l_t.append(l[0])
                l_t.append(l[1])
                l = l_t
        else:
            raise ValueError('Invalid entry: ', string)
    comp, energy = l
    groups_comp = re.findall(re_spec, comp)
    for g in groups_comp:
        if not g[1]: #  deal with elements whose coefficients is 1
            result[g[0]] = 1
        else:
            result[g[0]] = int(g[1])
    g_common_divisor = reduce(gcd, result.values())
    for key in result.keys():
        result[key] /= g_common_divisor
    no_atoms = np.sum(list(result.values()))
    for k in result.keys():
        result[k] /= no_atoms
    result['energy'] = float(energy)/no_atoms
    return result

def get_conditions_from_file(file, order, delimiter=None):
    """ Reads and parses a file and returns a triplet with the elements,
    coefficients, and the constants.
    These values can be used for the inequality or equality conditions in
    :class:`Range`.

    Lines starting with '#' will be skipped.

    Parameters
    ----------
    file : str
        the file that has to be read. The format has to be:
        ``Compound_formula_unit(delimiter)Energy_of_the_compound_per_fu``

    Note:
        **All inequalities are indented as** "<=": pay attention to prepare the
        input file in this way

    order : array
        the name of the elements in the order that has to be used for the
        coefficients. Eg, for the Mn-O system, ``order`` can be
        ['Mn', 'O'] or ['O', 'Mn']

    delimiter : str
        the symbol used to separate compound names from energy values.

    Returns
    -------
    compound_dict : dictionary of 3-ple:
        the keys are the compound identifiers as read from the file.
        The elements of the tuple are:

        - the formula unit of the compound

        - the stoichiometric coefficients for the elements in the compound

        - the (formation) energy per atom of the compound
    """
    no_variables = len(order)
    compounds_list = []
    fu_list = []
    coeff_list = []
    const_list = []
    with open(file, 'r') as stream:
        for line in stream:
            line = line.strip('\n')
            line = line.strip()
            if line:
                if line.startswith('#'):
                    continue
                compound = line.split(delimiter)[0]
                compounds_list.append(compound)
                fu = get_formula_unit(compound.split('_')[0])
                fu_list.append(fu)
                if delimiter is None:
                    delimiter2 = '    '
                line_pass = delimiter2.join([compound.split('_')[0],
                                            line.split(delimiter)[-1]])
                res = parse_mu_from_string(line_pass, delimiter=delimiter2)
                for key in res.keys():
                    if key != 'energy':
                        if not key in order:
                            raise ValueError('Found unexpected element: {}'
                                .format(key))
                const_list.append(res['energy'])
                res.pop('energy')
                els = []
                tmp = np.zeros(no_variables)
                for i, x in enumerate(order):
                    try:
                        tmp[i] = res[x]
                        els.append(x)
                    except KeyError:
                        tmp[i] = 0
                coeff_list.append(list(tmp))
    compound_dict = {compound: (fu, coeffs, const) for
                     compound, fu, coeffs, const in
                     zip(compounds_list, fu_list, coeff_list, const_list)}

    return compound_dict

def get_chem_pots_conditions(file, order, equality_compounds, delimiter=None):
    """
    Reads ``file`` and returns the data needed to initialize
    a :class:`Range` class as well the dictionary describing the various
    compounds.

    Parameters
    ----------
    file : str
        the location of the file with the required information
        The format of this file must be:

        ``Label_compound(delimiter)energy``

        Label_compound is a string, whose different entries must be separated
        by an underscore.

        delimiter is a string specifying the delimiter used to separate
        Label_compound from energy

        energy is a float representing the (formation) energy of the compound

    order : array
        ordered list of the chemical symbols to be used in specifying the
        equality and inequality conditions

    equality_compounds : array of strings
        the compounds in file corresponding to the equality conditions

    Returns
    -------
    result: tuple of 6 elements
        The first 5 elements are needed to initialize a
        :class:`Range` instance.

        The last element is the argument for the method
        :meth:`Range.set_compound_dict`
    """
    compound_dict = get_conditions_from_file(file, order, delimiter)

    new_compound_dict = defaultdict(list)
    coeff_equalities = []
    coeff_inequalities = []
    const_equalities = []
    const_inequalities = []
    bounds = []
    parsed = []
    # parse bounds in the specified order
    for el in order:
        for key, value in compound_dict.items():
            if el == value[0] and not key in parsed:
                parsed.append(key)
                new_compound_dict['bound'].append(key)
                bound = (None, value[2])
                bounds.append(bound)
    if len(bounds) == 0:
        bounds = None
    for el in equality_compounds:
        for key, value in compound_dict.items():
            if el == key and not key in parsed:
                parsed.append(key)
                new_compound_dict['equality'].append(el)
                coeff = value[1]
                const = value[2]
                coeff_equalities.append(coeff)
                const_equalities.append(const)
    if len(coeff_equalities) == 0:
        coeff_equalities = None
        const_equalities = None
    for key, value in compound_dict.items():
        if not key in parsed:
            new_compound_dict['inequality'].append(key)
            coeff = value[1]
            const = value[2]
            coeff_inequalities.append(coeff)
            const_inequalities.append(const)
    if len(coeff_inequalities) == 0:
        coeff_inequalities = None
        const_inequalities = None

    return (coeff_equalities, const_equalities, coeff_inequalities,
            const_inequalities, bounds, new_compound_dict)
