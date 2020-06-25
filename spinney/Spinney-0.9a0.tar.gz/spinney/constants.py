"""

Define physical constants and conversion factors.

Values are taken from the Committee on Data for Science and Technology 
(CODATA). Last version available is from 2014:
    https://arxiv.org/pdf/1507.07956.pdf
The symbols used for the physical constants are those employed in the CODATA
tables.
"""
import numpy as np

class UnitNotFoundError(Exception):
    """ Exception raised when a unit is not found. """

# CODATA Physical constants: from Table I    
_c_0               = 299792458         # Speed of light in vacuum [m s^-1]
_mu_0              = np.pi*4e-7        # Magnetic constant [N A^-2]
_e_0               = 1/(_mu_0*_c_0**2) # Electric constant [F m^-1]
_G                 = 6.67408e-11       # Gravitation constant [m^3 kg^-1 s^-2]
_h                 = 6.626070040e-34   # Planck constant [J s]
_h_bar             = _h/2/np.pi
_e                 = 1.6021766208e-19  # Charge of the electron [C]
_Phi_0             = _h/2/_e           # Magnetic flux quantum [Wb]
_G_0               = 2*_e**2/_h        # Conductance quantum [S]
_m_e               = 9.10938356e-31    # Mass of the electron [kg]
_m_p               = 1.672621898e-27   # Proton mass [kg]
_N_a               = 6.022140857e23    # Avogadro constant [mol-1]
_F                 = _N_a*_e           # Faraday constant [C mol^-1]
_R                 = 8.3144598         # Molar gas constant [J mol^-1 K^-1]
_k                 = _R/_N_a           # Boltzmann constant [J K^-1]
# Npn-SI units
_eV                = _e                # electron volt [J]
_u                 = 1.660539040e-27   # atomic mass unit [kg]
# Other units (from Table II)
_mu_B              = _e*_h_bar/2/_m_e  # Bohr magneton [J T^-1]       
_a_0               = 0.52917721067e-10 # Bohr radius [m]
_Hartree           = _e**2/4/np.pi/_e_0/_a_0 # Hartree [J]

# Custom units
_kJ_mol            = 1e3/_N_a          # kJ per mol [J mol^-1]
_cal               = 4.184             # calorie [J]
_kcal_mol          = _cal*1000/_N_a    # kcal/mol [J mol^-1]
_std_atm           = 101.325*1e3       # Standard atmosphere [Pa]


# Conversion factors between common units of energy
ev_to_j           = _eV                   # eV to Joule
j_to_ev           = 1/ev_to_j             # Joule to eV
hartree_to_j      = _Hartree              # Hartree to J
j_to_hartree      = 1/hartree_to_j
hartree_to_ev     = hartree_to_j*j_to_ev  # Hartree to eV
ev_to_hartree     = 1/hartree_to_ev
ry_to_ev          = 13.6056981            # Rydberg to eV 
ev_to_ry          = 1/ry_to_ev
ry_to_j           = ry_to_ev*ev_to_j
j_to_ry           = 1/ry_to_j
kcal_mol_to_j     = _kcal_mol
j_to_kcal_mol     = 1/kcal_mol_to_j
kj_mol_to_j       = _kJ_mol
j_to_kj_mol       = 1/kj_mol_to_j
ev_to_kcal_mol    = ev_to_j*j_to_kcal_mol
kcal_mol_to_ev    = 1/ev_to_kcal_mol
ev_to_kj_mol      = ev_to_j*j_to_kj_mol
kj_mol_to_ev      = 1/ev_to_kj_mol
ry_to_hartree     = ry_to_j*j_to_hartree
hartree_to_ry     = 1/ry_to_hartree
ry_to_kcal_mol    = ry_to_j*j_to_kcal_mol
kcal_mol_to_ry    = 1/ry_to_kcal_mol
ry_to_kj_mol      = ry_to_j*j_to_kcal_mol
kj_mol_to_ry      = 1/ry_to_kj_mol
hartree_to_kcal_mol = hartree_to_j*j_to_kcal_mol
kcal_mol_to_hartree = 1/hartree_to_kcal_mol
hartree_to_kj_mol = hartree_to_j*j_to_kcal_mol
kj_mol_to_hartree = 1/hartree_to_kj_mol
kcal_mol_to_kj_mol = kcal_mol_to_j*j_to_kj_mol
kj_mol_to_kcal_mol = 1/kcal_mol_to_kj_mol

# Conversion factors between common units of length
nm_to_m           = 1e-9                  # nm to m
m_to_nm           = 1/nm_to_m
ang_to_m          = 1e-10                 # Angstrom to m
m_to_ang          = 1/ang_to_m
bohr_to_m         = _a_0                  # Bohr to m
m_to_bohr         = 1/bohr_to_m
ang_to_bohr       = ang_to_m*m_to_bohr
bohr_to_ang       = 1/ang_to_bohr
ang_to_nm         = ang_to_m*m_to_nm
nm_to_ang         = 1/ang_to_nm
bohr_to_nm        = bohr_to_m*m_to_nm
nm_to_bohr        = 1/bohr_to_nm
cm_to_m           = 1e-2
m_to_cm           = 1/cm_to_m
cm_to_ang         = cm_to_m*m_to_ang
ang_to_cm         = 1/cm_to_ang
cm_to_nm          = cm_to_m*m_to_nm
nm_to_cm          = 1/cm_to_nm
cm_to_bohr        = cm_to_m*m_to_bohr
bohr_to_cm        = 1/cm_to_bohr

# Conversion factors between common units of pressure
kpa_to_pa         = 1000
pa_to_kpa         = 1/kpa_to_pa
torr_to_pa        = _std_atm/760
pa_to_torr        = 1/torr_to_pa
torr_to_kpa       = torr_to_pa*pa_to_kpa
kpa_to_torr       = 1/torr_to_kpa
atm_to_pa         = _std_atm
pa_to_atm         = 1/atm_to_pa
atm_to_kpa        = atm_to_pa*pa_to_kpa
kpa_to_atm        = 1/atm_to_kpa
torr_to_atm       = torr_to_pa*pa_to_atm
atm_to_torr       = 1/torr_to_atm

# list of available units
available_units = ['J', 'eV', 'Ry', 'Hartree', 'kcal/mol', 'kJ/mol',
                   'm', 'Angstrom', 'Bohr', 'nm', 'cm',
                   'Pa', 'kPa', 'Atm', 'Torr']
# Possible conversions for unit: from unit to other unit
_J_conversions = {'J' : 1, 'eV' : j_to_ev, 'Ry' : j_to_ry,
                  'Hartree' : j_to_hartree, 'kcal/mol' : j_to_kcal_mol,
                  'kJ/mol' : j_to_kj_mol}
_eV_conversions = {'J' : ev_to_j, 'eV' : 1, 'Ry' : ev_to_ry, 
                   'Hartree' : ev_to_hartree, 'kcal/mol' : ev_to_kcal_mol,
                   'kJ/mol' : ev_to_kj_mol}
_Ry_conversions = {'J' : ry_to_j, 'eV' : ry_to_ev, 'Ry' : 1, 
                   'Hartree' : ry_to_hartree, 'kcal/mol' : ry_to_kcal_mol,
                   'kJ/mol' : ry_to_kj_mol}
_Hartree_conversions = {'J' : hartree_to_j, 'eV' : hartree_to_ev,
                        'Ry' : hartree_to_ry, 'Hartree' : 1,
                        'kcal/mol' : hartree_to_kcal_mol,
                        'kJ/mol' : hartree_to_kj_mol}
_kcal_mol_converstions = {'J' : kcal_mol_to_j, 'eV' : kcal_mol_to_ev,
                          'Ry' : kcal_mol_to_ry, 'Hartree' : kcal_mol_to_hartree,
                          'kcal/mol' : hartree_to_kcal_mol,
                          'kJ/mol' : kcal_mol_to_kj_mol}
_kJ_mol_conversions = {'J' : kj_mol_to_j, 'eV' : kj_mol_to_ev,
                        'Ry' : kj_mol_to_ry, 'Hartree' : kj_mol_to_hartree,
                        'kcal/mol' : kj_mol_to_kcal_mol,
                        'kJ/mol' : 1}

_m_conversions = {'m' : 1, 'Angstrom' : m_to_ang, 'Bohr' : m_to_bohr,
                  'nm' : m_to_nm, 'cm' : m_to_cm}
_Angstrom_conversions = {'m' : ang_to_m, 'Angstrom' : 1,
                         'Bohr' : ang_to_bohr, 'nm' : ang_to_nm,
                         'cm' : ang_to_cm}
_Bohr_conversions = {'m' : bohr_to_m, 'Angstrom' : bohr_to_ang,
                     'Bohr' : 1, 'nm' : bohr_to_nm, 'cm' : bohr_to_cm}
_nm_conversions = {'m' : nm_to_m, 'Angstrom' : nm_to_ang,
                   'Bohr' : nm_to_bohr, 'nm' : 1, 'cm' : nm_to_cm}
_cm_conversions = {'m' : cm_to_m, 'Angstrom' : cm_to_ang, 'Bohr' : cm_to_bohr,
                   'nm' : cm_to_nm, 'cm' : 1}

_pa_conversions = {'Pa' : 1, 'kPa' : pa_to_kpa, 'Atm' : pa_to_atm, 
                  'Torr' : pa_to_torr}
_kpa_conversions = {'Pa' : kpa_to_pa, 'kPa' : 1, 'Atm' : kpa_to_atm, 
                  'Torr' : kpa_to_torr}
_atm_conversions = {'Pa' : atm_to_pa, 'kPa' : atm_to_kpa, 'Atm' : 1, 
                  'Torr' : atm_to_torr}
_torr_conversions = {'Pa' : torr_to_pa, 'kPa' : torr_to_kpa,
                    'Atm' : torr_to_atm, 'Torr' : 1}

conversion_table = { 
                    'J'        :   _J_conversions,
                    'eV'       :   _eV_conversions,
                    'Ry'       :   _Ry_conversions,
                    'Hartree'  :   _Hartree_conversions,
                    'kcal/mol' :   _kcal_mol_converstions,
                    'kJ/mol'   :   _kJ_mol_conversions,
                    'm'        :   _m_conversions,
                    'Angstrom' :   _Angstrom_conversions,
                    'Bohr'     :   _Bohr_conversions,
                    'nm'       :   _nm_conversions,
                    'cm'       :   _cm_conversions,
                    'Pa'       :   _pa_conversions,
                    'kPa'      :   _kpa_conversions,
                    'Atm'      :   _atm_conversions,
                    'Torr'     :   _torr_conversions
                    } 

def _run_sanity_check_keys(available_units, lookup_table):
    ''' Check that the voncersion *lookup_table* has not mistyped keys '''
    print('Sanity check for the look up table in spinney.constants\n')
    print('-'*50 + '\n')
    for unit in lookup_table.keys():
        if not (unit in available_units):
            error = '{} is not present in the look-up table keys'.format(unit)
            raise UnitNotFoundError(error)
        else:
            for unit2 in lookup_table[unit].keys():
                if not (unit2 in available_units):
                    error = '{} is not present in the table of {}'.format(unit2,
                             unit)
                    raise UnitNotFoundError(error)

def run_sanity_check():
    _run_sanity_check_keys(available_units, conversion_table)        
    
    
#run_sanity_check()


### Additional constants
wang_term_O = 1.36 #eV Termo to add to the O2 molecule to correct for 
                   # LDA/GGA shortcomings for this system. See: 
                   # "L. Wang et al., PRB 73, 195107 (2006)"
# corrections from S. Grindy et al., PRB 87, 075150 (2013)
# each correction is per X2 gas molecule
grindy_term_O_pbe = 1.198
grindy_term_H_pbe = 0.284
grindy_term_N_pbe = 0.892
grindy_term_F_pbe = 0.884
grindy_term_Cl_pbe = 0.966
grindy_term_O_lda = -0.254
grindy_term_H_lda = -0.170
grindy_term_N_lda = -0.439
grindy_term_F_lda = 0.084
grindy_term_Cl_lda = 0.370
