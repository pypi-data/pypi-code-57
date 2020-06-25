# -*- coding: utf-8 -*-
"""
Functions and classes for calculating defect and carrier concentrations
and related quantities from their formation energies.
"""
import copy
from collections import defaultdict
import numpy as np
import pandas as pd
from scipy.optimize import newton, bisect, brentq
from spinney.constants import (conversion_table, UnitNotFoundError,
                               available_units, _k)
from spinney import containers

class FermiDiracDistribution:
    r"""
    Implementation of the Fermi-Dirac distribution:

    .. math::

        \frac{1}{1 + e^{(E-\mu_e)/k_B T}}

    Parameters
    ----------
    energy : float or 1D darray
        the energies of the 1-electron levels

    mu : float
        the electron chemical potential

    T : float or 1D array
        the temperature

    energy_units : string
        the units in which :data:`energy` and :data:`mu` are expressed.
        :data:`T` is always assumed to be in K.

    Attributes
    ----------
    mu : float
        the electrom chemical potential

    kb : float
        Boltzman constant in terms of :data:`energy_units`

    values : numpy 2D array of shape (len(energy), len(T))
        The values of the Fermi distribution for those values of energy
        and temperature.
    """
    def __init__(self, energy, mu, T, energy_units='eV'):
        if type(mu) in containers:
            raise TypeError("The chemical potential has to be a scalar")
        self._mu = mu

        if type(energy) not in containers:
            self._energy = np.array([energy])
        elif not isinstance(energy, np.ndarray):
            self._energy = np.array(energy)
        else:
            self._energy = energy
        self._energy = self._energy[:, np.newaxis]
        if type(T) not in containers:
            self._T = np.array([T])
        elif not isinstance(T, np.ndarray):
            self._T = np.array(T)
        else:
            self._T = T
        self._T = self._T[np.newaxis, :]

        if energy_units in available_units:
            self._energy_units = energy_units
        else:
            raise UnitNotFoundError('{} is not a valid unit.'
                                    .format(energy_units))
        conv_factor = conversion_table['J'][self._energy_units]
        self._kb = _k * conv_factor

    @property
    def mu(self):
        return self._mu

    @property
    def kb(self):
        return self._kb

    @property
    def values(self):
        return self._get_values()

    def _get_values(self):
        """ Calculates the distribution at given values of energy, mu and T.
        These variables have the same meaning of those defined in *__init__*.

        Returns
        -------
        values : 2D np.ndarray with shape (len(energy), len(temperature))
        """
        energy = self._energy
        temper = self._T
        mu = self.mu
        with np.errstate(divide='ignore', over='raise'):
            ### we take care of division by 0 using np.where,
            ### so we can safely silence the warning errors
            try:
                fd = 1/(1 + np.exp((energy - mu)/(self.kb * temper)))
            except FloatingPointError: # in case the exponent will overflow,
                                       # use the largest data type

                fd = (1/(1 + np.exp((energy.astype(np.float128) - mu)/
                                    (self.kb * temper))))

            values = np.where(temper > 0, fd,
                              np.where(energy > mu, 0,
                                       np.where(energy < mu, 1, 0.5)))

        return values

class Carrier:
    """
    Object describing a free carrier in a semiconductor.

    Parameters
    ----------
    dos : 2D array
        the first column stores the 1-electron energy levels,
        the second column stores the corresponding DOS.
        The energy must be sorted by increasing values.

    vbm : float
        the energy level corresponding to the valence band maximum

    cbm : float
        the energy level corresponding to the conduction band minimum

    mu : float
        the electron chemical potential

    T : float or array
        the temperature range where the concentration will be
        calculated

    dos_down : 2D array
        If left to None, then the spin-down electrons are
        considered to have the same dos as :data:`dos`.

        Note:

            in case the spin down dos is reported using
            negative numbers, you need to flip the sign before using
            them in this function.

    units : str
        the units of energy

    Attributes
    ----------
    mu : float
        electron chemical potential

    T : float or 1D numpy array
        the temperature for which the Fermi Dirac distribution is
        calculated
    """
    def __init__(self, dos, vbm, cbm, mu, T, dos_down=None,
                 energy_units='eV'):
        if type(mu) in containers:
            raise ValueError("Non-scalar chemical potential!")
        self._mu = mu
        self._T = T
        self._vbm = vbm
        self._cbm = cbm
        if not isinstance(dos, np.ndarray):
            self._dos_up = np.array(dos)
        else:
            self._dos_up = dos.copy()
        if dos_down is not None:
            self.spinpol = True
            if not isinstance(dos_down, np.ndarray):
                self._dos_down = np.array(dos)
            else:
                self._dos_down = dos_down.copy()
        else:
            self._dos_down = None
            self.spinpol = False
        if energy_units in available_units:
            self._energy_units = energy_units
        else:
            raise UnitNotFoundError('{} is not a valid unit.'
                                    .format(energy_units))

    @property
    def mu(self):
        return self._mu
    @mu.setter
    def mu(self, value):
        if type(value) in containers:
            raise ValueError("Non-scalar chemical potential!")
        self._mu = value

    @property
    def T(self):
        return self._T
    @T.setter
    def T(self, value):
        self._T = value

    def _find_vbm_index(self, dos):
        """ Finds the index in the dos closest to the valence band maximum
        """
        return np.argwhere(dos[:, 0] <= self._vbm)[-1][0]

    def _find_cbm_index(self, dos):
        """ Finds the index in the dos closest to the conduction band minimum
        """
        return np.argwhere(dos[:, 0] >= self._cbm)[0][0]


class ConductionElectron(Carrier):
    """ Class describing a free electron """
    def _get_conduction_electron_number(self, dos):
        """ Calculate the number of conduction electrons per cell.

        Parameters
        ----------
        dos : 2D array
            the first column stores the 1-electron energy levels,
            the second column stores the corresponding DOS.

        Returns
        -------
        number_el : 1D numpy array
            the calculated number of electrons at temperatures in :attr:`T`.
            Units: [number of electrons/cell]
            shape : (len(self.T), )
        """
        imin = self._find_cbm_index(dos)
        fermi = FermiDiracDistribution(dos[imin:, 0],
                                       self.mu, self.T, self._energy_units)
        ddos = dos[imin:, 1][:, np.newaxis]
        integrand = ddos*fermi.values
        number_el = np.trapz(integrand, x=dos[imin:, 0], axis=0)

        return number_el

    def get_conduction_electron_number(self):
        """ Returns the number of electrons in the conduction band as a
        1D numpy array of length of :attr:`T`
        """
        number_el = self._get_conduction_electron_number(self._dos_up)
        if not self.spinpol:
            return number_el
        number_eld = self._get_conduction_electron_number(self._dos_down)
        return number_el + number_eld

class ValenceHole(Carrier):
    """ Class describing a free hole """
    def _get_valence_holes_number(self, dos):
        """ Calculate the number of valence holes per cell.

        Parameters
        ----------
        dos : 2D array
            the first column stores the 1-electron energy levels,
            the second column stores the corresponding DOS.

        Returns
        -------
        number_ho : 1D numpy array
            the calculated number of holes at temperatures in :attr:`self.T`.
            Units: [number of electrons/cell]
            shape : (len(self.T), )
        """
        imax = self._find_vbm_index(dos)
        fermi = FermiDiracDistribution(dos[:imax+1, 0], self.mu,
                                       self.T, self._energy_units)
        ddos = dos[:imax+1, 1][:, np.newaxis]
        integrand = ddos*(1 - fermi.values)
        number_ho = np.trapz(integrand, x=dos[:imax+1, 0], axis=0)

        return number_ho

    def get_valence_holes_number(self):
        """ Returns the number of holes in the valence band as a
        1D numpy array of length of :attr:`T`.
        """
        number_ho = self._get_valence_holes_number(self._dos_up)
        if not self.spinpol:
            return number_ho
        number_hod = self._get_valence_holes_number(self._dos_down)
        return number_ho + number_hod

class DefectConcentration:
    r"""
    Class describing defect concentrations in the dilute limit
    at the thermodynamic equilibrium:

    .. math::

        n_{eq}^d(T) = \frac{N_d g}{e^{E_f(d)/k_B T} + g}

    Or the approximated expression often used:

    .. math::

        n_{eq}^d(T) = N_d g e^{(-E_f(d)/k_BT}

    :math:`N_d` is the number of sites available for the specific defect in the
    crystal.

    Parameters
    ----------
    E_form : float
        The formation energy of the point defect

    N : float
        The number of sites available for the defect per volume unit.
        This is usually expressed in number of sites per cm^3, or
        number of sites per cell.

    T : array or float
        The temperatures (in K) to use for calculating the defect
        concentration

    g : float
        the intrinsic degeneracy of the defect

    energy_units : string
        the employed units of energy

    Attributes
    ----------
    dilute_limit_concentration : 1D numpy array of length len(T)
        the defect concentration at each temperature.
        If T was a scalar, a scalar is returned.

    dilute_limit_approx_concentration : 1D numpy array of length len(T)
        the defect concentration at each temperature, using the more
        approximative exponential formula.
        If T was a scalar, a scalar is returned.
    """
    def __init__(self, E_form, N, T, g=1, energy_units='eV'):
        if type(E_form) in containers:
            raise ValueError("The formation energy must be a scalar.")
        self.E_form = E_form
        if type(N) in containers:
            raise ValueError("N must be a scalar.")
        self.N = N
        if type(g) in containers:
            raise ValueError("g must be a scalar.")
        self.g = g

        if not isinstance(T, np.ndarray):
            self.T = np.array(T)
        else:
            self.T = T

        if energy_units in available_units:
            self.energy_units = energy_units
        else:
            raise UnitNotFoundError('{} is not a valid unit.'
                                    .format(energy_units))
        conv_factor = conversion_table['J'][self.energy_units]
        self._kb = _k*conv_factor

    @property
    def dilute_limit_concentration(self):
        return self._dilute_limit_concentration(self.E_form, self.N, self.T,
                                                self.g)

    @property
    def dilute_limit_approx_concentration(self):
        return self._dilute_limit_approx_concentration(self.E_form, self.N,
                                                       self.T, self.g)

    def _dilute_limit_concentration(self, E_form, N, T, g):
        """ The defect concentration in the dilute limit.

        Parameters
        ----------
        E_form : float
            defect formation energy

        N : float
            number of available sites per unit of volume

        T : array
            the temperature range in K

        g : float
            the intrinsic degeneracy of the defect

        Returns
        -------
        conc : 1D numpy array of length len(T)
            the defect concentration at each temperature.
            If T was a scalar, a scalar is returned.
        """
        arg = E_form/self._kb
        with np.errstate(divide='ignore', over='raise'):
            if E_form > 0:
                try:
                    ex_factor = np.where(T > 0, 1/(np.exp(arg/T) + g), 0)
                except FloatingPointError:
                    T = np.array(T, dtype=np.float128)
                    ex_factor = np.where(T > 0, 1/(np.exp(arg/T) + g), 0)
            if E_form <= 0:
                ex_factor = np.where(T > 0, 1/(np.exp(arg/T) + g), 1)
        conc = N*g*ex_factor
        return conc

    def _dilute_limit_approx_concentration(self, E_form, N, T, g):
        try:
            len(T)
        except TypeError:
            T = np.array(T)
        with np.errstate(divide='ignore', over='raise'):
            if E_form > 0:
                try:
                    ex_factor = np.where(T > 0, np.exp(-E_form/self._kb/T), 0)
                except FloatingPointError:
                    ex_factor = np.where(T > 0,
                                         np.exp(-E_form
                                                /self._kb
                                                /T.astype(np.float128)), 0)
            if E_form < 0:
                if 0 in T:
                    raise ZeroDivisionError('Temperature is equal to 0!')
                ex_factor = np.exp(-E_form/self._kb/T)
        conc = N*g*ex_factor
        return conc

class EquilibriumConcentrations:
    r"""
    Represents the defects and carriers concentrations for Fermi level
    values given by the charge neutrality condition in a
    homogeneous semiconductor:

    .. math::

        \sum_i q_i n_d(q, T) + p - n = N_d

    where :math:`q_i` is the defect charge state,
    :math:`n_d` its concentration, :math:`p` and :math:`n`
    are the concentration of free holes and electrons, respectively
    and :math:`N_d` is the effective doping level.

    Parameters
    ----------
    charge_states : dict of arrays or None
        defect_type : list of charge states for all considered defects
        If equal to None, the pristine semiconductor is considered.

        Example:

            If we consider the Si vacancy and Si interstitials in
            the charge states -2, -1, 0, 1, 2; then:

            >>> charge_states = {'Si_int':[-2, -1, 0, 1, 2],
            ...                  'Vac_Si':[-2, -1, 0, 1, 2]}

    form_energy_vbm : dict of arrays or None
        defect_type : the defect formation energy calculated
        for an electron chemical potential equal to :data:`vbm`.
        For any array, the order of the values must be the same
        as the one used in :data:`charge_states`

        If equal to None, the pristine semiconductor is considered.

        Example:

            For the defects listed above, we would type:

            >>> form_energy_vbm = {'Si_int':[val_m2, val_m1, val_0,
            ...                              val_1, val_2],
            ...                    'Vac_Si':[valv_m2, valv_m1, valv_0,
            ...                              valv_1, valv_2]}

            where ``val_m2`` is the formation energy of the Si interstitial
            in charge state -2, ``valv_m2`` is the one of the Si vacancy in
            this charge state and so on.

    vbm : float
        the value of the valence band maximum

    e_gap : float
        the value of the band gap

    site_conc : dict
        defect_type : site_concentration
        for defect_type = 'electron' and 'hole', this value
        should be the concentration for the unit cell used to calculate
        :data:`dos`.

        Example:

            For the defects listed above, we have:

            >>> site_conc = {'Si_int'  : conc_Si_int,
            ...           'Vac_Si'  : conc_Vac_Si,
            ...           'electron': conc_electrons,
            ...           'hole'    : conc_holes}

    dos : 2D array
        The first column are the energies of 1-electron level,
        the second the DOS per cell. The values of :data:`vbm`
        and :data:`e_gap` must be consistent with the dos.

    T_range : array or float
        the temperature range

    g : dict of lists or None
        defect_type : [degeneracy charge state 1,
        degeneracy charge_state 2, ...]
        each list represents the degeneracy for a given type of defect
        in each of its charge states. The order has to match that of
        *charge_states[defect_type]*.

        If None, all the degeneracy factors are taken equal to 1.
        The structure is analogous to :data:`charge_states`.

    N_eff : float
        the effective-doping concentration

    units_energy : str
        employed energy units

    dos_down : array
        the eventual dos for the spin-down electrons

    Attributes
    ----------
    defect_order : tuple
        the ordered sequence with the defect names.

    charge_states :  dict
        defect_name : sequence of charge states of the defect

    formation_energies_vbm : dict
        defect_name : sequence of the defect formation energies, for
        every charge state listed in :attr:`charge_states`, for an electron
        chemical potential equal to :attr:`vbm`

    formation_energies_equilibrium : dict
        defect_name : sequence of the defect formation energies, for
        every charge state listed in :attr:`charge_states`, for an electron
        chemical potential equal to :attr:`equilibrium_fermi_level`

    site_conc : dict
        defect_name : effective concentration for that kind of defect

    T : numpy 1D array
        the temperatures considered for calculating the defect formation
        energies

    vbm : float
        the value of the pristine system valence band maximum

    cbm : float
        the value of the pristine system conduction band minimum

    N_eff : float
        effective dopant concentration

    equilibrium_fermi_level : numpy 1D array of length len(self.T)
        the value of the electron chemical potential at the equilibrium
        for a given temperature

    equilibrium_defect_concentrations :  dict
        defect_name : {defect_charge_state : array, ...}
        where array is a numpy 1D array of length len(self.T) holding
        the calculated defect concentration for that charge state at
        at given temperature

    equilibrium_electron_concentrations : numpy 1D array of length \
        len(self.T)
        the value of the electron concentration at the equilibrium
        for a given temperature

    equilibrium_hole_concentrations : numpy 1D array of length len(self.T)
        the value of the hole concentration at the equilibrium
        for a given temperature

    equilibrium_carrier_concentrations : numpy 1D array of length \
        len(self.T)
        the value of the carrier concentration at the equilibrium
        for a given temperature. If the value is positive, holes are the
        main carriers; otherwise electrons.

    find_root_algo : string
        specifies which algorithm to use in order to find the roots of
        the charge neutrality condition. Possible values:

        - `brentq`, `newton`, `bisect`
    """
    def __init__(self, charge_states, form_energy_vbm, vbm, e_gap, site_conc,
                 dos, T_range, g=None, N_eff=0, units_energy='eV',
                 dos_down=None):
        if charge_states is not None:
            # check that the charges are integers
            for key in charge_states.keys():
                seq = charge_states[key]
                if type(seq) not in containers:
                    raise TypeError('Charge state values must be in an array.')
                for value in seq:
                    if not isinstance(value, int):
                        raise TypeError('Charge values have to '
                                        'be integers')
        if form_energy_vbm is not None:
            for key in form_energy_vbm.keys():
                defect = form_energy_vbm[key]
                if type(defect) not in containers:
                    raise TypeError('Formation energies for defect {:s} '
                                    'must be given in an array'
                                    .format(str(key)))
                for value in defect:
                    if not isinstance(value, (int, float)):
                        raise TypeError('Formation energies must be '
                                        'scalars')

        self._defect_order = [] # the order used to store defect concentrations
        self._charge_states_dict = copy.deepcopy(charge_states)
        self._formation_energies_vbm_dict = copy.deepcopy(form_energy_vbm)
        self._site_conc_dict = copy.copy(site_conc)
        # tuples instead of dictionaries, the order of the defects is contained
        # in self._defect_order
        self._charge_states = ()
        self._formation_energies_vbm = ()
        self._site_conc = () # hold site concentrations only for atomic defects
        self._Ne = self._site_conc_dict.pop('electron')
        self._Nh = self._site_conc_dict.pop('hole')
        if charge_states is None:
            self._charge_states = None
            self._formation_energies_vbm = None
            self._g = None
            self._defects = False
        else:
            if len(charge_states) != len(form_energy_vbm):
                raise ValueError('{} and {} do not contain the same defects!'.
                                 format(list(charge_states.keys()),
                                        list(form_energy_vbm.keys())))

            self._defects = True
            self._g = ()
            for key in charge_states:
                self._defect_order.append(key)
                charge_values = tuple(charge_states[key])
                form_energy_values = tuple(form_energy_vbm[key])
                if g is None:
                    g_value = [1]*len(charge_values)
                    g_value = tuple(g_value)
                else:
                    g_value = tuple(g[key])

                if len(charge_values) != len(form_energy_values):
                    raise ValueError('Different number of charge states '
                                     'and formation energies for defect {}'.
                                     format(key))
                self._charge_states += charge_values
                self._formation_energies_vbm += form_energy_values
                N_defect = [site_conc[key]]*len(charge_states[key])
                self._site_conc += tuple(N_defect)
                self._g += g_value
        self._defect_order = tuple(self._defect_order)
        self._units = units_energy
        self._vbm = vbm
        self._cbm = vbm + e_gap
        self._N_eff = N_eff
        # T has to be an array in any case, as we will loop over it
        try:
            len(T_range)
            self._T = copy.copy(T_range)
        except TypeError:
            self._T = np.array([T_range])

        self._dos = copy.copy(dos)
        if dos_down is not None:
            self._dos_down = copy.copy(dos_down)
        else:
            self._dos_down = None

        self._conduction_e = ConductionElectron(self._dos, self._vbm,
                                                self._cbm,
                                                None, None, self._dos_down,
                                                self._units)
        self._valence_h = ValenceHole(self._dos, self._vbm, self._cbm,
                                      None, None, self._dos_down,
                                      self._units)

        self._found_mu = False # becomes true once the equilibrium fermi level
                               # has been calculated
        # method to use in order to find the equilibrium chemical potential
        self._find_root_algo = 'brentq'

    @property
    def defect_order(self):
        return self._defect_order

    @property
    def charge_states(self):
        return copy.deepcopy(self._charge_states_dict)

    @property
    def formation_energies_vbm(self):
        return copy.deepcopy(self._formation_energies_vbm_dict)

    @property
    def formation_energies_equilibrium(self):
        mu_e = self.equilibrium_fermi_level[0] - self._vbm
        self._formation_energies_eq_dict = {}
        for key, values in self._formation_energies_vbm_dict.items():
            self._formation_energies_eq_dict[key] = []
            for i, value in enumerate(values):
                charge = self._charge_states_dict[key][i]
                self._formation_energies_eq_dict[key].append(value
                                                             + charge*mu_e)
        return copy.deepcopy(self._formation_energies_eq_dict)

    @property
    def site_conc(self):
        return np.copy(self._site_conc_dict)

    @property
    def T(self):
        return self._T
    @T.setter
    def T(self, value):
        try:
            len(value)
            self._T = np.copy(value)
        except TypeError:
            self._T = np.array([value])

    @property
    def vbm(self):
        return self._vbm

    @property
    def cbm(self):
        return self._cbm

    @property
    def N_eff(self):
        return self._N_eff
    @N_eff.setter
    def N_eff(self, value):
        self._N_eff = value

    @property
    def get_defects_concentrations_at_point(self):
        return self._calculate_defect_concentrations

    @property
    def get_electron_concentration_at_point(self):
        return self._calculate_electron_concentration

    @property
    def get_hole_concentration_at_point(self):
        return self._calculate_hole_concentration

    @property
    def equilibrium_fermi_level(self):
        if self._found_mu:
            return np.copy(self._equilibrium_fermi_level)
        return self.get_equilibrium_fermi_level()

    @property
    def equilibrium_defect_concentrations(self):
        if hasattr(self, '_equilibrium_defect_concentrations'):
            return self._make_eq_defects_dict()
        self.get_equilibrium_defect_concentrations()
        return self._make_eq_defects_dict()

    @property
    def equilibrium_electron_concentrations(self):
        if hasattr(self, '_equilibrium_electron_concentrations'):
            return np.copy(self._equilibrium_electron_concentrations)
        return self.get_equilibrium_electron_concentrations()

    @property
    def equilibrium_hole_concentrations(self):
        if hasattr(self, '_equilibrium_hole_concentrations'):
            return np.copy(self._equilibrium_hole_concentrations)
        return self.get_equilibrium_hole_concentrations()

    @property
    def equilibrium_carrier_concentrations(self):
        return (self.equilibrium_hole_concentrations -
                self.equilibrium_electron_concentrations)

    @property
    def find_root_algo(self):
        return self._find_root_algo
    @find_root_algo.setter
    def find_root_algo(self, value):
        self._find_root_algo = value

    @property
    def defect_concentrations_dataframe(self):
        if hasattr(self, '_def_concentrations_df'):
            return self._def_concentrations_df
        else:
            self._def_concentrations_df = self._make_defect_concentrations_df()
            return self._def_concentrations_df
    
    @property
    def carrier_concentrations_dataframe(self):
        if hasattr(self, '_carr_concentrations_df'):
            return self._carr_concentrations_df
        else:
            self._carr_concentrations_df = self._make_carrier_concentrations_df()
            return self._carr_concentrations_df

    def _make_defect_concentrations_df(self):
        data = self.get_equilibrium_defect_concentrations()
        names = []
        charges = []
        for name in self.defect_order:
            charges_ = self.charge_states[name]
            names += [name]*len(charges_)
            charges += charges_
        def_cols = pd.MultiIndex.from_arrays([names, charges])
        df = pd.DataFrame(data.T, columns=def_cols, dtype=float, index=self.T)
                          
        df.index.name = 'T (K)'
        df.sort_index(axis=1, inplace=True)
        return df
         
    def _make_carrier_concentrations_df(self):
        elec = self.get_equilibrium_electron_concentrations()
        holes = self.get_equilibrium_hole_concentrations()
        data = np.c_[elec, holes]
        df = pd.DataFrame(data, columns=['electron', 'hole'], index=self.T)
        df.index.name = 'T (K)'
        return df

    def _calculate_defect_concentrations(self, mu, T):
        """
        Parameters
        ----------
        mu : float

        T  : float

        Returns
        -------
        concentrations : 1D array of length len(self._charge_states)
        """
        if not self._defects:
            print('The system has no point defects!')
            return 0
        defects_concentrations = []
        for charge, e_form, N, g in zip(self._charge_states,
                                        self._formation_energies_vbm,
                                        self._site_conc, self._g):
            energy = e_form + charge*(mu - self.vbm)
            defect = DefectConcentration(energy, N, T, g,
                                         energy_units=self._units)
            conc = defect.dilute_limit_concentration
            defects_concentrations.append(conc)

        return np.array(defects_concentrations)

    def _calculate_electron_concentration(self, mu, T):
        self._conduction_e.mu = mu
        self._conduction_e.T = T
        no_el = self._conduction_e.get_conduction_electron_number().item(0)
        return no_el*self._Ne

    def _calculate_hole_concentration(self, mu, T):
        self._valence_h.mu = mu
        self._valence_h.T = T
        no_hol = self._valence_h.get_valence_holes_number().item(0)
        return no_hol*self._Nh

    def _charge_neutrality(self, mu, T):
        """ Obtain the charge neutrality condition
        at a given Fermi level mu.

        Parameters
        ----------
        mu : float

        T : float

        Returns
        -------
        Q : float
        """
        # negative carriers
        electrons = self.get_electron_concentration_at_point(mu, T)
        # positive carriers
        holes = self.get_hole_concentration_at_point(mu, T)
        if self._charge_states is not None:
            concs = self._calculate_defect_concentrations(mu, T)
            Q = (np.dot(self._charge_states, concs) +
                 holes - electrons - self.N_eff)
        else:
            Q = holes - electrons - self.N_eff
        return Q

    def get_equilibrium_fermi_level(self):
        """ Return the equilibrium value of the Fermi level as a function
            of the temperature.

        Returns
        -------
        equilibrium_fermi_level : 1D numpy array of length len(self.T)
            the calculated Fermi level as a function of T
        """
        self._equilibrium_fermi_level = []
        for T in self._T:
            if self._find_root_algo == 'newton':
                x0 = (self.vbm + self.cbm)/2
                x0_t = x0
                converged = False
                try:
                    value = newton(self._charge_neutrality,
                                   x0,
                                   tol=1e-10,
                                   maxiter=1000,
                                   args=tuple([T]))
                    converged = True
                except RuntimeError: # happens when the algorithm does not
                                     # converge
                    attempt_count = 0
                    while not converged and x0 > self.vbm and x0 < self.cbm:
                        if self._equilibrium_fermi_level and attempt_count < 3:
                            x0 = self._equilibrium_fermi_level[-1]
                            x0_t = x0
                        elif attempt_count%2 == 0:
                            x0 += x0_t*0.001*attempt_count
                        else:
                            x0 -= x0_t*0.001*attempt_count
                        attempt_count += 1
                        try:
                            value = newton(self._charge_neutrality,
                                           x0,
                                           tol=1e-10,
                                           maxiter=200,
                                           args=tuple([T]))
                            converged = True
                        except RuntimeError:
                            continue
            elif self._find_root_algo == 'bisect':
                try:
                    value = bisect(self._charge_neutrality,
                                   self.vbm, self.cbm,
                                   maxiter=1000,
                                   args=tuple([T]))
                except ValueError: # happens usually if the function
                    # has no opposite values at the interval extrema
                    value = bisect(self._charge_neutrality,
                                   self.vbm - abs(self.vbm)/2,
                                   self.cmb + abs(self.cbm)/2,
                                   maxiter=1000,
                                   args=tuple([T]))
            elif self._find_root_algo == 'brentq':
                try:
                    value = brentq(self._charge_neutrality,
                                   self.vbm, self.cbm,
                                   maxiter=1000, xtol=1e-15,
                                   args=tuple([T]))
                except ValueError:
                    value = brentq(self._charge_neutrality,
                                   self.vbm - abs(self.vbm)/2,
                                   self.cbm + abs(self.cbm)/2,
                                   maxiter=1000, xtol=1e-15,
                                   args=tuple([T]))
            else:
                raise ValueError('The method {} is not '
                                 'a valid one!\n'.format(self._find_root_algo))

            self._equilibrium_fermi_level.append(value)
        self._equilibrium_fermi_level = np.array(self._equilibrium_fermi_level)

        self._found_mu = True
        return self._equilibrium_fermi_level

    def get_equilibrium_defect_concentrations(self):
        """
        Return the equilibrium defect concentration as a function
        of the temperature.

        Returns
        -------
        concentrations : 2D numpy array of shape \
            (len(self._charge_states), len(self._T))
        """
        self._equilibrium_defect_concentrations = np.zeros(
            (len(self._charge_states), len(self._T)))
        for i, T in enumerate(self._T):
            mu_T = self.equilibrium_fermi_level[i]
            eq_concs = self._calculate_defect_concentrations(mu_T, T)
            self._equilibrium_defect_concentrations[:, i] = eq_concs

        return self._equilibrium_defect_concentrations

    def get_equilibrium_electron_concentrations(self):
        """
        Return the equilibrium electron concentration as a function
        of the temperature.

        Returns
        -------
        concentrations: 1D array of length len(self.T)
        """
        self._equilibrium_electron_concentrations = np.zeros(len(self._T))
        for i, T in enumerate(self._T):
            eq_concs = self.get_electron_concentration_at_point(
                self.equilibrium_fermi_level[i], T)
            self._equilibrium_electron_concentrations[i] = eq_concs
        return self._equilibrium_electron_concentrations

    def get_equilibrium_hole_concentrations(self):
        self._equilibrium_hole_concentrations = np.zeros(len(self._T))
        for i, T in enumerate(self.T):
            eq_concs = self.get_hole_concentration_at_point(
                self.equilibrium_fermi_level[i], T)
            self._equilibrium_hole_concentrations[i] = eq_concs
        return self._equilibrium_hole_concentrations

    def _make_eq_defects_dict(self):
        defects_dict = defaultdict(dict)
        count = 0
        for key in self.defect_order:
            charges = self.charge_states[key]
            for charge in charges:
                this_conc = self._equilibrium_defect_concentrations[count]
                defects_dict[key][charge] = this_conc.copy()
                count += 1
        return defects_dict

def extract_formation_energies_from_file(file_name):
    """ Read a file with the format:

    ::

        # arbitrary number of comment lines
        defect_name    defect_charge_state   defect_formation_energy

    Parameters
    ----------
    file_name : string
        the file with the data
    
    Returns
    -------
    init_args : tuple
        the tuple contains two elements: the two dictionaries to be used
        as the first two arguments for initializing a
        :class:`EquilibriumConcentrations` instance 
    """
    charge_states = {}
    form_energies = {}
    with open(file_name, 'r') as f:
        for line in f:
            if not (line.startswith('#')):
                data = line.strip().split()
                defect = data[0]
                charge = int(data[1])
                form_energy = float(data[-1])
                charge_states.setdefault(defect, [])
                charge_states[defect].append(charge)
                form_energies.setdefault(defect, [])
                form_energies[defect].append(form_energy)
    return charge_states, form_energies
