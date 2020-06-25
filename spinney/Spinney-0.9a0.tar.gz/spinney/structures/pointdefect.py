#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Module implementing a :class:`PointDefect` class
to store and process information
concerning a system with point defects.
"""
import copy
import numpy as np
import ase.atoms
from ase.calculators.calculator import PropertyNotImplementedError, Calculator
from spinney import containers
from spinney.tools.reactions import calculate_defect_formation_energy
from spinney.tools.formulas import get_formula_unit
import spinney.defects.fnv as fnv

class DummyAseCalculator(Calculator):
    """
    Dummy calculator to be used when the calculations are done with a
    code not supported by ase.
    Use this dummy calculator only to pass custom Atoms objects to the
    :class:`PointDefect` class. Any other use of ought to be avoided.

    Parameters
    ----------
    atoms : :class:`ase.Atoms`
        the Atoms instance to be used with a :class:`PointDefect` instance
    """
    implemented_properties = ['energy']

    def __init__(self, atoms):
        Calculator.__init__(self, atoms=None, restart=None,
                            ignore_bad_restart_file=False, label=None)
        self.atoms = atoms

    def set_total_energy(self, value):
        self.results['energy'] = value

    def get_potential_energy(self, atoms=None):
        if atoms is not None:
            atoms = None
        energy = self.get_property('energy', None)
        return energy

class PointDefect(ase.atoms.Atoms):
    """
    PointDefect class.

    It represents a 3D-periodic system containing one or more point defects.

    Parameters
    ----------
    ase_atoms : instance of :class:`ase.Atoms`
        the Atoms object created from a completed point defect
        calculation.

        Note:
            it is assumed that all the Atoms object have units of Angstrom
            for lengths and eV for energies. This is the default in :mod:`ase`.

    Attributes
    ----------
    my_name : string, optional
        an alphanumeric label for the instance

    defect_position : 1D numpy array
        the scaled positions of the defect in the supercell

    defect_charge : float
        the charge state of the defect

    pristine_system : :class:`ase.Atoms` instance
        the :class:`ase.Atoms` describing the pristine system

    parent_compounds : dict
        the keys are: ``pristine``, ``chemical_formula1``, ...
        the value associated to ``pristine`` is the :class:`ase.Atoms` instance
        representing the pristine system. ``chemical_formula1`` etc. are the
        chemical formulas of the other compounds involved in the creation
        of the point defect. These are added using
        :func:`set_parent_elements`.
        Their values are the :class:`ase.Atoms` instances representing
        these compounds.

        Excluding the pristine system, these data are not necessary, but can
        be used to test the chemical potential values to be used in the
        calculation of the defect formation energy.

        For example, for an Oxygen vacancy in MgO, the keys of
        :attr:`parent_compounds`
        would be: 'pristine', 'O2', 'Mg2', which means the ase Atoms object
        for 'Mg2' contains 2 Mg atoms; i.e. it is the primitive HCP cell.

    parent_elements : dict, optional
        each element is an instance of an :class:`ase.Atoms` object
        representing the compound describing the standard state
        of the elements involved in the defective system.

        For example, for an Oxygen vacancy in MgO, these would be the
        :class:`ase.Atoms` instances for  'O2' and 'Mg2'

    Examples
    --------
    To initialize a :class:`PointDefect` instance, it is only necessary to
    have an initialized :class:`ase.Atoms` object with attached a
    calculator that supports the :func:`Atoms.get_total_energy` method.

    Suppose that the output, obtained by a first-principle code, describing
    a defective system is saved in the file
    ``output.fmt``. And that format ``fmt`` can be read by :func:`ase.io.read`.
    Then the following snippet can be used to initialize a :class:`PointDefect`
    object representing the defective system.

    >>> import ase.io
    >>> defect = ase.io.read('output.fmt')
    >>> pdf = PointDefect(defect)

    """
    def __init__(self, ase_atoms):
        self._keys = ['symbols', 'positions', 'numbers', 'tags', 'momenta',
                      'masses', 'magnetic_moments', 'charges',
                      'scaled_positions', 'cell', 'pbc', 'celldisp',
                      'constraint', 'calculator', 'info']
        init = {}
        for key in self._keys:
            try:
                if hasattr(ase_atoms, key):
                    init[key] = getattr(ase_atoms, key)
                elif hasattr(ase_atoms, 'get_' + key):
                    init[key] = getattr(ase_atoms, 'get_' + key)()
                else:
                    init[key] = None
            except PropertyNotImplementedError:
                init[key] = None
        if not init['calculator']:
            raise ValueError('Error! A calculator must be present!')
        if (init['symbols'] is not None) and (init['numbers'] is not None):
            init['numbers'] = None
        if (init['positions'] is not None) and (init['scaled_positions'] is
                                                not None):
            init['scaled_positions'] = None
        energy = ase_atoms.get_total_energy()
        calculator = DummyAseCalculator(ase_atoms.copy())
        ase.atoms.Atoms.__init__(self, symbols=init['symbols'],
                                 positions=init['positions'],
                                 numbers=init['numbers'], tags=init['tags'],
                                 momenta=init['momenta'],
                                 masses=init['masses'],
                                 magmoms=init['magnetic_moments'],
                                 charges=init['charges'],
                                 scaled_positions=init['scaled_positions'],
                                 cell=init['cell'].view(), pbc=init['pbc'],
                                 celldisp=init['celldisp'],
                                 constraint=init['constraint'],
                                 calculator=None,
                                 info=init['info'])
        # avoid some problems and just use the dummy calculator
        self.set_calculator(calculator)
        self.calc.set_total_energy(energy)
        tmp_flag = (self.pbc == True).all()
        if not tmp_flag:
            raise ValueError('The system must be periodic in all 3 '
                             'dimensions!')

        # scaled position of thr defect in the supercell
        self._defect_position = None
        # the formal charge of the point defect
        self._defect_charge = None
        # ase.atoms.Atoms objects representing the compounds involved in
        # the defective system
        self._parent_compounds = {}
        # the Atoms objects for the elementary compounds of the elements
        # involved in the defect creation
        self._parent_elements = {}
        # valence band maximum and electronic band gap
        self._vbm = None
        self._eg = None

        # available correction schemes
        self._available_correction_schemes = ('ko', 'fnv')
        self._correction_scheme = None
        self._correction_scheme_dict = {}
        self._ecorr = None
        # dielectric tensor
        self._er = np.eye(3)
        # allow to use other values for the element chemical potentials
        self._mu_ranges = None # will be a sequence of tuples
                             # one 2-ple for each element
        self._input_mu_values = None
        # actual value chemical potential to use in the calculations
        self._mu_values = None
        # position fermi level wrt valence band maximum
        self._fermi_level = 0
        # label identifying the instance
        self._name = None

    @property
    def my_name(self):
        return self._name
    @my_name.setter
    def my_name(self, value):
        if not isinstance(value, str):
            raise TypeError('The instance name must be a string')
        self._name = value

    @property
    def defect_position(self):
        return self._defect_position

    def set_defect_position(self, position):
        """ Set the fractional coordinates of the point defects in the
        system.

        Parameters
        ----------
        position : 1D array
            the scaled position of the point defect with respect to
            :func:`self.get_cell`
        """
        if type(position) not in containers:
            raise ValueError('Positions must be a 1D array')

        if not isinstance(position, np.ndarray):
            position = np.array(position)
        if position.ndim != 1:
            raise ValueError('Positions must be a 1D array')

        self._defect_position = position

    @property
    def defect_charge(self):
        return self._defect_charge

    def set_defect_charge(self, charge):
        """
        Parameters
        ----------
        charge : float
            The formal charge assigned to the point defect.
            It is assumed that only one localized charge is present in the
            supercell.
        """
        # the correction schemes expect an array
        charge = [charge]
        if not isinstance(charge, np.ndarray):
            charge = np.array(charge)
        self._defect_charge = charge

    @property
    def parent_compounds(self):
        return self._parent_compounds

    @property
    def parent_elements(self):
        return copy.copy(self._parent_elements)

    def set_pristine_system(self, ase_pristine):
        """
        Parameters
        ----------
        ase_pristine : :class:`ase.Atoms`
            The :class:`ase.Atoms` object representing the pristine system.
        """
        if ase_pristine.get_calculator() is None:
            raise ValueError('Error! A calculator must be present!')
        if not np.allclose(ase_pristine.get_cell().view(), self.get_cell().view(), 1e-3):
            raise ValueError('Defective and pristine system must have the '
                             'same cell!')
        self._parent_compounds['pristine'] = ase_pristine

    @property
    def pristine_system(self):
        try:
            return self._parent_compounds['pristine']
        except KeyError:
            raise RuntimeError('Pristine system not found. '
                               'Use "set_pristine_system(...)"')

    def set_parent_elements(self, elements):
        """
        Set the :class:`ase.Atoms` objects representing the compounds, in their
        reference state, for the elements involved in the formation
        of the point defects.

        Parameters
        ----------
        elements : list or tuple
            each element of the sequence is an Atoms object.
            For example, if the defective system consists of
            the C vacancy- N_C complex in diamond, then:
            elements = (:class:`ase.Atoms` for C (e.g. C diamond),
            :class:`ase.Atoms` for N2)
        """
        for elm in elements:
            if elm is not None:
                if elm.get_calculator() is None:
                    raise ValueError('Error! A calculator must be present!')
                formula = elm.get_chemical_formula()
                label = get_formula_unit(formula)
                self._parent_compounds[formula] = elm
                self._parent_elements[label] = elm

    @property
    def vbm(self):
        return self._vbm

    def set_vbm(self, value):
        """
        Parameters
        ----------
        value : float
            The system valence band maximum, which determines the
            minimum value of the electron chemical potential.
        """
        self._vbm = value

    @property
    def Eg(self):
        return self._eg

    def set_Eg(self, value):
        """
        Parameters
        ----------
        value : float
            The system band gap value.
        """
        self._eg = value

    @property
    def available_correction_schemes(self):
        return self._available_correction_schemes

    @property
    def correction_scheme(self):
        return self._correction_scheme
    @correction_scheme.setter
    def correction_scheme(self, scheme):
        if scheme not in self.available_correction_schemes:
            raise ValueError('{:s} is not an implemented scheme'
                             .format(scheme))
        self._correction_scheme = scheme

    def set_finite_size_correction_scheme(self, scheme):
        """ Set the correction scheme for finite-size effects in point
        defect calculations.

        Parameters
        ----------
        scheme : string
            The correction scheme to use.
            Possible values:

            - 'ko' : Kumagai and Oba, PRB 89, 195205 (2014)
            - 'fnv': Freysoldt, Neugebauer, and Van de Walle, Phys.
              Rev. Lett. 102, 016402 (2009)
        """
        self.correction_scheme = scheme

    def add_correction_scheme_data(self, **kwargs):
        r""" Add the extra data needed in order to calculate the defect
        formation energy with the choosen scheme

        Parameters
        ----------
        kwargs : dict

            - For the correction schemes 'ko' and 'fnv':

              keys: ``potential_pristine``, ``potential_defective``

              the values are :mod:`numpy` arrays.

              - for 'ko':

                the arrays have to contain the value of the electrostatic
                potential at the ionic sites. The order has to be the same
                of the one used in the :class:`ase.Atoms` objects employed
                in the initialization of the :class:`PointDefect`
                instance and employed in :func:`set_pristine_system`

              - for 'fnv':

                the arrays have to contain the electrostatic potential on a
                3D grid. The file has to match the supercell used to
                initialize the :class:`PointDefect` instance.

            - For 'fnv':

              ``axis``
              the unit cell axis along which the electrostatic potential
              will be averaged.

              ``defect_density`` (optional)
              a 3D array with the charge density that can be used to
              model the defect-induced one.
              This will be used to fit the model charge to the defect-induced
              charge density.

              ``x_comb`` (optional)
              a float between 0 and 1. Weight of the exponential function with
              respect to the Gaussian function in modeling the defect-induced
              charge density. Default ``x_comb = 0``: the charge density is a
              pure Gaussian.

              ``gamma`` (optional)
              a float. The parameter of the exponential function. Default
              value is 1.

              ``beta`` (optional)
              a float. The parameter of the Gaussian function. Default value
              is 1.
     
              ``shift_tol`` (optional)
              a float representing the tolerance to be used in order to locate
              the defect position along ``axis``. Default value:
              :math:`1e-5 \times \mathrm{length cell parameter of axis}`

              ``e_tol`` (optional)
              a float, break condition for the iterative calculation of the
              correction energy. Value in Hartree. Default: 1e-6 Ha.

            - For `ko`:

              ``distance_tol`` (optional)
              rounding tolerance for comparing distances, in units of
              Angstrom. Default value is 5e-2 Angstroms.

              ``e_tol`` (optional)
              a float, break condition for the iterative calculation of the
              correction energy. Value in eV. Default: 1e-6 eV.
        """
        if self._correction_scheme is None:
            raise ValueError('No correction scheme has been chosen. '
                             'Use "set_finite_size_correction_scheme(...)"')
        try:
            potential_pris = kwargs['potential_pristine']
        except KeyError:
            raise RuntimeError('The potential of the pristine system '
                               'is required by {:s}'
                               .format(self._correction_scheme))
        try:
            potential_def = kwargs['potential_defective']
        except KeyError:
            raise RuntimeError('The potential of the defective system '
                               'is required by {:s}'
                               .format(self._correction_scheme))

        if self._correction_scheme == 'fnv':
            try:
                axis_dir = kwargs['axis']
                self._correction_scheme_dict['axis_dir'] = axis_dir
            except KeyError:
                raise RuntimeError('For the fnv scheme, "axis" has to be '
                                   'specified')
        defect_density = kwargs.get('defect_density', None)
        distance_tol = kwargs.get('distance_tol', 1e-2)
        e_tol = kwargs.get('e_tol', 1e-6)
        shift_tol = kwargs.get('shift_tol', 1e-5)
        x_comb = kwargs.get('x_comb', 0)
        p_gamma = kwargs.get('gamma', 1)
        p_beta = kwargs.get('beta', 1)

        self._correction_scheme_dict['potential_pristine'] = potential_pris
        self._correction_scheme_dict['potential_defective'] = potential_def
        self._correction_scheme_dict['defect_density'] = defect_density
        self._correction_scheme_dict['distance_tol'] = distance_tol
        self._correction_scheme_dict['e_tol'] = e_tol
        self._correction_scheme_dict['shift_tol'] = shift_tol
        self._correction_scheme_dict['x_comb'] = x_comb
        self._correction_scheme_dict['p_gamma'] = p_gamma
        self._correction_scheme_dict['p_beta'] = p_beta

    @property
    def dielectric_tensor(self):
        return self._er

    def set_dielectric_tensor(self, value):
        """
        Parameters
        ----------
        value : 2D array or float
            The value of the system dielectric tensor (or constant).
        """
        if type(value) not in containers:
            er = value
            self._er = np.eye(3)*value
        else:
            if not isinstance(value, np.ndarray):
                er = np.array(value)
            else:
                er = value
            self._er = er

    @property
    def chemical_potential_ranges(self):
        return self._mu_ranges

    def set_chemical_potential_ranges(self, ranges):
        """ For each element involved in the creation of the defective
        system, specify the minimum and maximum value that the chemical
        potential can have.

        If :func:`set_parent_elements` was used, it will be checked that
        the input elements are the same.

        Parameters
        ----------
        ranges : dictionary of 2-ples
            For each element involved in the creation of the point defect,
            an element of :data:`ranges[element]` is the 2-ple:

            (minimum value atomic chemical potential,
            maximum value atomic chemical potential)

            With 'atomic chemical potential' it is intended that the values
            are referred to a single atom, and not to the formula unit of
            the corresponding element used in :attr:`parent_elements`
        """
        if len(self._parent_elements) != 0:
            if len(self._parent_elements) != len(ranges):
                raise ValueError('A different number of elements than '
                                 'expected was entered: {:d} != {:d}'
                                 .format(len(ranges),
                                         len(self._parent_elements)))
            for key in ranges.keys():
                if key not in self._parent_elements.keys():
                    raise ValueError('Element {} does not appear in '
                                     '"self.parent_elements"')
        else:
            self._mu_ranges = copy.copy(ranges)

    @property
    def chemical_potential_values(self):
        if self._mu_values is not None:
            for key in self._mu_values.keys(): # check for updated values
                if self._mu_values[key] != self._input_mu_values[key]:
                    self._get_chemical_potential_values()
                    break
            return self._mu_values
        self._get_chemical_potential_values()
        return self._mu_values

    def set_chemical_potential_values(self, chem_pots, force=False):
        """ Set the chemical potential values, for each species involved in
        forming the defective system, to be used in the calculation
        of the defect formation energy.

        If these are not set, an exception will be raised.
        If :attr:`chemical_potential_ranges` is not ``None``,
        it will be checked if the given chemical potentials are within
        these ranges; if not, an exception will be raised.
        In any case, the given chemical potential values will be tested againts
        the parent elements chemical potentials, if these are given.
        Use :data:`force=True` to bypass these checks.

        Parameters
        ----------
        chem_pots : dict of floats
                each element is the chemical potential of one element (value
                give per atom)
                The keys must be the same used in *self.parent_elements*, if
                the parent elements were set.

        force : bool
                If True, the inserted values will be used for the calculations,
                even tough they are not physical valid values
        """
        if force:
            self._mu_values = copy.copy(chem_pots)

        elif len(self._parent_elements) != 0:
            if len(self._parent_elements) != len(chem_pots):
                raise ValueError('A different number of elements than '
                                 'expected was entered: {:d} != {:d}'
                                 .format(len(chem_pots),
                                         len(self._parent_elements)))
            for key in chem_pots.keys():
                if key not in self._parent_elements.keys():
                    raise ValueError('Element {} does not appear in '
                                     '"self.parent_elements"')

        self._input_mu_values = copy.copy(chem_pots)

    @property
    def fermi_level_value_from_vbm(self):
        return self._fermi_level

    def set_fermi_level_value_from_vbm(self, value):
        """ Set the value of the Fermi level with respect to the system
        valence band maximum.

        This value will be used to calculate the defect formation energy
        of charged defects.

        Parameters
        ----------
        value : float
        """
        self._fermi_level = value

    def _get_chemical_potential_values(self):
        """ Returns the values of the chemical potentials to be used in
        calculating the defect formation energies.
        """
        # if user has given some values
        if self._input_mu_values is not None:
            # if user has given the allowed ranges
            if self._mu_ranges is not None:
                for key, mu in self._input_mu_values.items():
                    mumin, mumax = self._mu_ranges[key]
                    if not mumin <= mu <= mumax:
                        raise ValueError('Chemical potential of {} is not '
                                         'in the valid range!'.format(key))
            # no ranges given
            elif len(self.parent_elements) != 0:
                for key, mu in self._input_mu_values.items():
                    parent = self._parent_elements[key]
                    mumax = (parent.get_total_energy()/
                             len(parent))
                    if mu > mumax:
                        raise ValueError('Chemical potential of {} is above '
                                         'the valid upper bound'.format(key))
        # user gave no values
        else:
            raise ValueError('No values set for the chemical potentials!')

        self._mu_values = copy.copy(self._input_mu_values)

    @property
    def E_corr(self):
        if self._ecorr:
            ecorr = self._ecorr
        else:
            ecorr = self.calculate_finite_size_correction()
        return ecorr

    def calculate_finite_size_correction(self, verbose=False):
        """ Calculate the energy correction for finite-size effects employing
        the method chosen with *set_finite_size_correction_scheme*.

        Parameters
        ----------
        verbose : bool
                If True, several details are returned as a dictionary.
                If False, only the correction energy is returned.
                This has to be added to the energy of the defective system.
        """
        pristine = self.pristine_system
        pristine_pot = self._correction_scheme_dict['potential_pristine']
        defective_pot = self._correction_scheme_dict['potential_defective']
        tol_dist = self._correction_scheme_dict['distance_tol']
        e_tol = self._correction_scheme_dict['e_tol']
        shift_tol = self._correction_scheme_dict['shift_tol']
        if not self._correction_scheme:
            self._ecorr = 0
            if verbose:
                return (0, {'E_corr': 0, 'Details':'No correction scheme '
                                                   'was set'})
            return 0
        if self._correction_scheme == 'ko':
            from spinney.defects.kumagai import KumagaiCorr
            kuma = KumagaiCorr(self.get_cell().view(),
                               self.get_scaled_positions(),
                               pristine.get_scaled_positions(),
                               self.defect_position, self.defect_charge,
                               self.dielectric_tensor,
                               defective_pot, pristine_pot,
                               tol_dist=tol_dist, tol_en=e_tol)
            ecorr = kuma.get_net_correction_energy()
            self._ecorr = ecorr
            if verbose:
                dd = {}
                dd['E corr'] = ecorr
                dd['PC term'] = kuma.pc_term
                dd['Alignment term'] = kuma.alignment_term
                dis, pot = kuma.alignment_potential_vs_distance_sampling_region
                dd['Distances from defect sampled points'] = dis
                dd['Std deviation potential alignment'] = np.std(pot)
                dd['Corr object'] = kuma
                return ecorr, dd
            return ecorr
        if self._correction_scheme == 'fnv':
            x_comb = self._correction_scheme_dict['x_comb']
            beta = self._correction_scheme_dict['p_beta']
            gamma = self._correction_scheme_dict['p_gamma']
            density_model = fnv.FChargeDistribution(x=x_comb,
                                                    gamma=gamma,
                                                    beta=beta)
            er_av = np.mean(np.linalg.eig(self.dielectric_tensor)[0])
            dielectric_constant = er_av
            axis_average = self._correction_scheme_dict['axis_dir']
            axis_param = np.linalg.norm(self.get_cell().view(), axis=1)[axis_average]
            grid = pristine_pot.shape
            rang = range(grid[axis_average])
            axis_grid = [x/grid[axis_average] for x in rang]
            axis_grid = np.array(axis_grid)*axis_param
            if self._correction_scheme_dict['defect_density'] is None:
                FCorr = fnv.FCorrection(self.get_cell().view(), self.defect_charge[0],
                                        density_model, pristine_pot,
                                        defective_pot, dielectric_constant,
                                        self.defect_position, axis_average,
                                        tolerance=e_tol, shift_tol=shift_tol)
            else:
                charge_density = self._correction_scheme_dict['defect_density']
                fitter = fnv.FFitChargeDensity(self.get_cell().view(),
                                               fnv.FChargeDistribution,
                                               charge_density,
                                               self.defect_position,
                                               axis_average, 1e-5)
                popt = fitter.fit_model()[0]
                new_model = fnv.FChargeDistribution(*popt)
                FCorr = fnv.FCorrection(self.get_cell().view(), self.defect_charge[0],
                                        new_model, pristine_pot, defective_pot,
                                        dielectric_constant,
                                        self.defect_position, axis_average,
                                        tolerance=e_tol, shift_tol=shift_tol)
            ecorr = FCorr.get_correction_energy()
            self._ecorr = ecorr
            if verbose:
                dd = {}
                dd['E corr'] = ecorr
                dd['E lat'] = FCorr.eper - FCorr.eself
                dd['Alignment term'] = FCorr.v_alignment
                dd['Potential grid'] = axis_grid
                dd['DFT potential'] = FCorr.av_locpot
                dd['Model potential'] = FCorr.av_long_range_potential
                dd['Alignment potential'] = FCorr.av_short_range_potential
                if self._correction_scheme_dict['defect_density'] is not None:
                    dd['CDistribution parameters'] = popt
                dd['Corr object'] = FCorr
                return ecorr, dd
            return ecorr

    def get_defect_formation_energy(self, include_corr=False):
        """ Returns the formation energy of the defective system.

        Parameters
        ----------
        include_corr : bool
                If True, the formation energy is already corrected for
                finite-size effects.

        Returns
        -------
        energy : float
            the defect formation energy
        """
        if include_corr:
            ecorr = self.E_corr
        else:
            ecorr = 0

        e_defect = {self.get_chemical_formula() : self.get_total_energy()}
        e_pristine = {self.pristine_system.get_chemical_formula() :
                      self.pristine_system.get_total_energy()}
        mu_dict = copy.copy(self.chemical_potential_values)
        mu_dict['electron'] = self.vbm + self.fermi_level_value_from_vbm
        charge_state = self.defect_charge[0]
        return calculate_defect_formation_energy(e_defect, e_pristine,
                                                 mu_dict, charge_state, ecorr)

