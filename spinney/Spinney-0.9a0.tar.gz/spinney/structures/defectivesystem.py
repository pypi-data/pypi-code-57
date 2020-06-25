import numpy as np
import os
import pandas as pd
import warnings
from spinney.io.vasp import extract_potential_at_core_vasp
from spinney.io.wien2k import extract_potential_at_core_wien2k
from spinney.constants import conversion_table
from spinney.structures.pointdefect import PointDefect
from spinney import containers
from spinney.defects.diagrams import Diagram
from spinney.defects.concentration import EquilibriumConcentrations

import ase.io
from ase.calculators.vasp import VaspChargeDensity

class DefectiveSystem:
    """
    Container class describing a system with point defects.

    Parameters
    ----------
    data_path: string
        path to the folder containing the results of the point defect calculations.
        It is expected a directory tree like this:

        ::

            "data_path"
             ├── data_defects
             │   ├── "defect_name"
             │   │   ├── "charge_state"
             │   │   │   └── "files" 
             │   │   ├── "charge_state"
             │   │   │   └── "files"
             │   │   ├── "charge_state"
             │   │   │   └── "files"
             │   │   └── "charge_state"
             │   │       └── "files"
             │   ├── "defect_name"
             ...
             └── pristine
                 └── "files"

        - `defect_name` is a string describing the point defect.
        - `charge_state` must be the charge state of the considered defect.
        - `files` are the data needed for calculating defect formation energies. \
         These depends on the calculator in use:

         - VASP: at least there should be the OUTCAR file.
         - WIEN2k: at least there should be the case.struct and case.scf files.

        For all calculators a file named `position.txt` containing the fractional
        coordinates of the defective site must be present.

    calculator: string
        the code used to calculate the data

    Attributes
    ----------
    vbm: float
        the valence band maximum of the host material

    dielectric_tensor: float or 2D array
        the dielectric tensor of the host material

    chemical_potentials: dict
        a dictionary whose keys are the parent elements
        forming the defective system and whose values
        are the chemical potentials to be used in the
        calculation of the defect formation energy

    correction_scheme: str
        specifies the correction scheme for finite-size-effects
        to be used

    data: pandas DataFrame object
        collects the calculated formation energies for each
        processed point defect

    point_defects: list
        a list of ``PointDefect`` objects corresponding to the
        processed point defects

    gap_range: tuple
        a tuple containing the valence band maximum and 
        conduction band minimum of the pristine system

    extended_gap_range: tuple
        a tuple containing the valence band maximum and 
        conduction band minimum for an extetnded band gap
        of the pristine system. Used to initialize
        a Spinney Diagram object
        
    diagram: Spinney Diagram object
        an object representing the defect formation energies
        as a function of the electron chemical potential
    """
    def __init__(self, data_path, calculator):
        self._defects_path = os.path.join(data_path, 'data_defects')
        self._pristine_path = os.path.join(data_path, 'pristine')
        self._calculator = calculator.lower()

        if calculator == 'vasp':
            self._mandatory_files_base = ['OUTCAR']
        elif calculator == 'wien2k':
            self._mandatory_files_base = ['case.struct', 'case.scf']
        else:
            raise ValueError('Calculator not valid')

        self._point_defects = [] # store the last point-defect objects
        self._defects_Ecorr = {} # store type correction scheme
                                # and correction energies
        self._data_frame = None
        self._exception_status = False

    @property
    def point_defects(self):
        return self._point_defects

    @property
    def data(self):
        try:
            return self._data_frame
        except AttributeError:
            raise AttributeError('Defect formation energies need to be '
                                 'calculated before. Call: '
                                 '"calculate_energies"')

    @property
    def vbm(self):
        return self._vbm

    @vbm.setter
    def vbm(self, value):
        self._vbm = value

    @property
    def dielectric_tensor(self):
        return self._dielectric 

    @dielectric_tensor.setter
    def dielectric_tensor(self, value): 
        if value in containers:
            self._dielectric = np.array(value)
        else:
            self._dielectric = np.eye(3)*value

    @property
    def chemical_potentials(self):
        return self._chem_pots

    @chemical_potentials.setter
    def chemical_potentials(self, dictionary):
        if not isinstance(dictionary, dict):
            raise TypeError('The value must be a dictionary')
        self._chem_pots = dictionary

    @property
    def correction_scheme(self):
        return self._correction_scheme

    @correction_scheme.setter
    def correction_scheme(self, value):
        if value in ['ko', 'fnv']:
            self._correction_scheme = value
            self._defects_Ecorr[value] = {}
        else:
            raise ValueError('Not a valid correction scheme')

    @property
    def gap_range(self):
        return self._gap_range

    @gap_range.setter
    def gap_range(self, value):
        try:
            l = len(value)
            if l != 2:
                raise TypeError('The value must be a container '
                                'with two elements')
        except TypeError:
            print('The value must be a container with two elements')
        self._gap_range = value

    @property
    def extended_gap_range(self):
        return self._extended_gap_range

    @extended_gap_range.setter
    def extended_gap_range(self, value):
        try:
            l = len(value)
            if l != 2:
                raise TypeError('The value must be a container '
                                'with two elements')
        except TypeError:
            print('The value must be a container with two elements')
        self._extended_gap_range = value

    @property
    def diagram(self):
        self._prepare_diagram()
        return self._diagram

    @property
    def concentrations(self):
        self._prepare_concentrations()
        return self._eq_concentrations

    @property
    def site_concentrations(self):
        return self._site_concentrations

    @site_concentrations.setter
    def site_concentrations(self, value):
        if not isinstance(value, dict):
            raise TypeError('The value must be a dictionary')
        else:
            self._site_concentrations = value

    @property
    def temperature_range(self):
        return self._temperature_range

    @temperature_range.setter
    def temperature_range(self, value):
        if isinstance(value, (list, tuple)):
            self._temperature_range = np.array(value)
        else:
            self._temperature_range = value

    @property
    def dos(self):
        return self._dos

    @dos.setter
    def dos(self, value):
        if not isinstance(value, np.ndarray):
            raise TypeError('The density of states must be given '
                            'as a 2D numpy array')
        else:
            dos = value
            if dos.ndim != 2:
                raise TypeError('The density of states must be given '
                                'as a 2D numpy array')
        self._dos = dos

    @property
    def effective_doping(self):
        return self._effective_doping

    @effective_doping.setter
    def effective_doping(self, value):
        self._effective_doping = value

    @property
    def defects_degeneracy_numbers(self):
        """ A dictionary o 
        Represents the degeneracy for each type of defect
        in each of its charge states. The order has to match that of
        *charge_states[defect_type]*.
        """
        return self._defects_g

    @defects_degeneracy_numbers.setter
    def defects_degeneracy_numbers(self, value):
        self._defects_g = value

    def _check_defect_dir(self, path, *files, raise_exception=True):
        for file in files:
            if not os.path.isfile(os.path.join(path, file)):
                if raise_exception:
                    raise FileNotFoundError('Critical file {} missing '
                                            'in directory {}'.format(file,
                                                                     path))
                else:
                    warnings.warn('File {} not in {}'.format(file, path)) 

    def _update_mandatory_files(self):
        try:
            correction_scheme = self.correction_scheme
            self._mandatory_files.append('position.txt')
        except AttributeError:
            correction_scheme = None
        if self._calculator == 'vasp':
            if correction_scheme == 'fnv':
                self._mandatory_files.append('LOCPOT')
                self._exception_status = True
            elif correction_scheme == 'ko':
                self._exception_status = True
        if self._calculator == 'wien2k':
            if correction_scheme == 'fnv':
                raise ValueError('Method of fnv not yet implemented in Wien2k')
            elif correction_scheme == 'ko':
                self._mandatory_files.append('case.vcoul')
                self._exception_status = True

    def _process_point_defects(self, verbose):
        self._mandatory_files = self._mandatory_files_base[:]
        if self.point_defects:
            # reset list of point defect objects
            self._point_defects = []
        try:
            vbm = self.vbm
        except AttributeError:
            raise Exception('Must set the valence band value of the system')
        try:
            dielectric = self.dielectric_tensor
        except AttributeError:
            raise Exception('Must set the dielectric tensor of the system')
        try:
            chem_pots = self.chemical_potentials
        except AttributeError:
            raise Exception('Must set the values for the chemical potentials')
        try:
            correction_scheme = self.correction_scheme
        except AttributeError:
            correction_scheme = None
        Ecorrs = self._defects_Ecorr.get(correction_scheme)
        self._check_defect_dir(self._pristine_path,
                               *self._mandatory_files,
                               raise_exception=True)
        if self._calculator == 'vasp':
            out_pristine = os.path.join(self._pristine_path, 'OUTCAR')
            ase_pristine = ase.io.read(out_pristine, format='vasp-out')
            if correction_scheme == 'ko':
                pot_prist = extract_potential_at_core_vasp(out_pristine)
            elif correction_scheme == 'fnv':
                locpot_prist = os.path.join(self._pristine_path, 'LOCPOT')
                locpot_prist = VaspChargeDensity(locpot_prist)
                locpot_prist = locpot_prist.chg[-1]*ase_pristine.get_volume()*(-1)
                cell = ase_pristine.get_cell().view()
                params = np.linalg.norm(cell, axis=1)
                locpot_index = np.argsort(params)[-1]

        elif self._calculator == 'wien2k':
            struct_pristine = os.path.join(self._pristine_path, 'case.struct') 
            scf_pristine = os.path.join(self._pristine_path, 'case.scf')
            ase_pristine = prepare_ase_atoms_wien2k(struct_pristine,
                                                    scf_pristine)
            if correction_scheme == 'ko':
                vcoul_pristine = os.path.join(self._pristine_path, 'case.vcoul')
                pot_prist = extract_potential_at_core_wien2k(struct_pristine,
                                                             vcoul_pristine)
                pot_prist *= conversion_table['Ry']['eV']

        data_charge_states = []
        data_form_ene_uncorr = []
        data_form_ene_corr = []
        data_indices = []

        self._update_mandatory_files()
        for root, dirs, files in os.walk(self._defects_path):
            path = root.split(os.sep)
            skip_defect = False
            if not dirs:
                charge_state = int(path[-1])
                defect_name = path[-2]
                if verbose:
                    print('Processing defect {} and charge state {} in\n'
                          'directory: {}'.format(defect_name, charge_state, root))
                self._check_defect_dir(root, *self._mandatory_files,
                                       raise_exception=self._exception_status)
                if self._calculator == 'vasp':
                    try:
                        out_defect = os.path.join(root, 'OUTCAR')
                        ase_defect = ase.io.read(out_defect, format='vasp-out')
                    except FileNotFoundError:
                        skip_defect = True
                elif self._calculator == 'wien2k':
                    try:
                        struct_def = os.path.join(root, 'case.struct')
                        scf_def = os.path.join(root, 'case.scf')
                        ase_defect = prepare_ase_atoms_wien2k(struct_def, scf_def)
                    except FileNotFoundError:
                        skip_defect = True

                if skip_defect:
                    if verbose:
                        print('No output files found for this defect, '
                              'processing next defect')
                else: 
                    data_indices.append(defect_name)
                    data_charge_states.append(charge_state)
                    pdf = PointDefect(ase_defect)
                    pdf.set_pristine_system(ase_pristine)
                    pdf.set_chemical_potential_values(chem_pots)
                    pdf.set_vbm(vbm)
                    pdf.set_defect_charge(charge_state)
                    pdf.set_dielectric_tensor(dielectric)
                    pdf.my_name = defect_name + ' ' + str(charge_state)
                    if os.path.isfile(os.path.join(root, 'position.txt')):
                        def_position = np.genfromtxt(os.path.join(root, 'position.txt'),
                                                     dtype=float)
                        pdf.set_defect_position(def_position)
                    energy_uncorr = pdf.get_defect_formation_energy(False)
                    # prepare correction scheme data
                    if Ecorrs:
                        Ecorr_value = Ecorrs.get(pdf.my_name)
                    else:
                        Ecorr_value = None
                    if correction_scheme and Ecorr_value is None:
                        pdf.set_finite_size_correction_scheme(correction_scheme)
                        if correction_scheme == 'ko':
                            if self._calculator == 'vasp':
                                pot_def = extract_potential_at_core_vasp(out_defect)
                                corr_data = {'potential_pristine':pot_prist,
                                             'potential_defective':pot_def}
                            elif self._calculator == 'wien2k':
                                vcoul_def = os.path.join(root, 'case.vcoul')
                                pot_def = extract_potential_at_core_wien2k(struct_def,
                                                                           vcoul_def)
                                pot_def *= conversion_table['Ry']['eV']
                                corr_data = {'potential_pristine':pot_prist,
                                             'potential_defective':pot_def}
                        elif correction_scheme == 'fnv':
                            if self._calculator == 'vasp':
                                locpot_def = os.path.join(root, 'LOCPOT')
                                locpot_def = VaspChargeDensity(locpot_def)
                                locpot_def = locpot_def.chg[-1]*ase_pristine.get_volume()*(-1)
                                corr_data = {'potential_pristine':locpot_prist,
                                             'potential_defective':locpot_def,
                                             'axis':locpot_index}
                        pdf.add_correction_scheme_data(**corr_data)
                        if verbose:
                            print('Calculating defect formation energy corrected '
                                  'using "{}"'.format(correction_scheme))
                        energy = pdf.get_defect_formation_energy(True)
                        self._defects_Ecorr[correction_scheme][pdf.my_name] = pdf.E_corr
                        data_form_ene_corr.append(energy)
                        data_form_ene_uncorr.append(energy_uncorr)
                    elif correction_scheme and Ecorr_value is not None:
                        if verbose:
                            print('Calculating defect formation energy corrected '
                                  'using old value for '
                                  '"{}"'.format(correction_scheme))
                        energy = energy_uncorr + Ecorr_value
                        data_form_ene_corr.append(energy)
                        data_form_ene_uncorr.append(energy_uncorr)
                    else:
                        if verbose:
                            print('Calculating uncorrected defect formation energy')
                        data_form_ene_uncorr.append(energy_uncorr)
                        data_form_ene_corr.append(np.nan)
                
                    if verbose:
                        print('Formation energy = {:10.6} eV'.format(energy))
                        print('DONE')
                    self._point_defects.append(pdf)
                if verbose:
                    print('-'*60, '\n')
        data = np.c_[data_form_ene_uncorr, data_form_ene_corr]
        indices = pd.MultiIndex.from_arrays([data_indices,
                                             data_charge_states],
                                            names = ['Defect', 'Charge'])
        df = pd.DataFrame(data,
                          columns=['Form Ene (eV)',
                                   'Form Ene Corr. (eV)'],
                          index=indices)
        self._data_frame = df

    def calculate_energies(self, verbose=True):
        """ Calculate defect formation energies 
        Parameters
        ----------
        verbose: bool
            if True, information about the process is printed
        """
        self._process_point_defects(verbose)

    def write_formation_energies(self, out_file):
        """ Write the defect formation energies to a file in a format
        used by Spynney.

        Parameters
        ----------
        out_file: str
            name of the file used to write the energies
        """
        energy_file = open(out_file, 'w')


        format_ = '{:<8} {:>8} {:30.10f}\n'
        df = self.data
        if not df['Form Ene Corr. (eV)'].isnull().all():
            data = df['Form Ene Corr. (eV)'].values
            header = df.columns[-1]
        else:
            data = df['Form Ene (eV)'].values
            header = df.columns[-2] 

        energy_file.write('#{:<8} {:8} {:>30}\n'.format('System',
                                                'Charge',
                                                header))

        for count, value in enumerate(df.index.values):
            name, charge = value
            energy_file.write(format_.format(name, str(charge), data[count]))
        energy_file.close()

    def _prepare_diagram(self):
        try:
            band_gap = self.gap_range
        except AttributeError:
            raise Exception('Must set the band edges')
        try:
            extended_gap = self.extended_gap_range
        except AttributeError:
            extended_gap = None

        df = self.data.reset_index()
        if not df['Form Ene Corr. (eV)'].isnull().all():
            data = df['Form Ene Corr. (eV)'].values
        else:
            data = df['Form Ene (eV)'].values
        names = df['Defect']
        charges = df['Charge']
        defect_dictionary = {}
        for name, charge, value in zip(names, charges, data):
            defect_dictionary.setdefault(name, {})
            defect_dictionary[name][charge] = value
        diagram = Diagram(defect_dictionary, band_gap, extended_gap)
        self._diagram = diagram

    def _prepare_concentrations(self):
        df = self.data
        charge_states = {}
        energies_vbm = {}
        for (defect, charge) in df.index:
            def_charge = charge_states.setdefault(defect, [])
            def_charge.append(charge) 
            if not df['Form Ene Corr. (eV)'].isnull().all():
                data = df['Form Ene Corr. (eV)']
            else:
                data = df['Form Ene (eV)']
            def_ene = energies_vbm.setdefault(defect, [])
            def_ene.append(data.loc[defect][charge])
        vbm = self.vbm
        try:
            egap = self.gap_range[1] - self.gap_range[0]
        except AttributeError:
            raise AttributeError('Must set the energy gap range '
                                 '"gap_range" attribute')
        try:
            site_conc = self.site_concentrations
        except AttributeError:
            raise AttributeError('Must set the site concentrations '
                                 '"site_concentrations" attribute')
        try:
            dos = self.dos
        except AttributeError:
            raise AttributeError('Must set the density of state '
                                 '"dos" attribute')
        try:
            T = self.temperature_range
        except AttributeError:
            raise AttributeError('Must set the temperature range '
                                 '"temperature_range" attribute')
        if hasattr(self, '_effective_doping'):
            N_eff = self._effective_doping
        else:
            N_eff = 0
        concentrations = EquilibriumConcentrations(charge_states, energies_vbm,
                                                   vbm, egap, site_conc,
                                                   dos, T, N_eff=N_eff)
        self._eq_concentrations = concentrations
