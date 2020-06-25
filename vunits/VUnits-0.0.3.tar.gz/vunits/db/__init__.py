import os
import json

from vunits.quantity import Quantity, UnitQuantity

short_prefixes = {'Y': 1.e24, 'Z': 1.e21, 'E': 1.e18, 'P': 1.e15, 'T': 1.e12,
                  'G': 1.e9, 'M': 1.e6, 'k': 1.e3, 'h': 1.e2, 'da': 1.e1,
                  'd': 1.e-1, 'c': 1.e-2, 'm': 1.e-3, 'mu': 1.e-6, 'n': 1.e-9,
                  'p': 1.e-12, 'f': 1.e-15, 'a': 1.e-18, 'z': 1.e-21,
                  'y': 1.e-24}
"""dict: Short prefix used for unit symbols (e.g. km). See table of values
in the :ref:`prefix section <prefix_table>`"""

long_prefixes = {'yotta': 1.e24, 'zetta': 1.e21, 'exa': 1.e18, 'peta': 1.e15,
                 'tera': 1.e12, 'giga': 1.e9, 'mega': 1.e6, 'kilo': 1.e3,
                 'hecto': 1.e2, 'deca': 1.e1, 'deci': 1.e-1, 'centi': 1.e-2,
                 'milli': 1.e-3, 'micro': 1.e-6, 'nano': 1.e-9, 'pico': 1.e-12,
                 'femto': 1.e-15, 'atto': 1.e-18, 'zepto': 1.e-21,
                 'yocto': 1.e-24}
"""dict: Long prefix used for unit descriptions (e.g. kilometer). See table of
values in the :ref:`prefix section <prefix_table>`"""


def write_unit_db(filename=None, unit_db=None, json_kwargs=None):
    """Writes unit database

    Parameters
    ----------
        filename : str, optional
            Name of database. If ``filename`` not specified, saves to
            vunits/db/unit_db.json.
        unit_db : dict, optional
            Database to write. Keys should be strings of the units and the
            values are :class:`~vunits.quantity.Quantity` objects. If not
            specified, uses the default library.
        json_kwargs : dict, optional
            Arguments to write to JSON file. If ``json_kwargs`` not specified,
            uses default options.
    """
    if unit_db is None:
        unit_db = {
            # Empty string
            '': UnitQuantity(add_long_prefix=False, add_short_prefix=False),
            # Time
            's': UnitQuantity(s=1.,  add_long_prefix=False),
            'sec': UnitQuantity(s=1., add_short_prefix=False,
                                add_long_prefix=False),
            'second': UnitQuantity(s=1., add_short_prefix=False,
                                   plural_suffix='s'),
            'min': UnitQuantity(mag=60., s=1., add_short_prefix=False),
            'minute': UnitQuantity(mag=60., s=1., add_short_prefix=False,
                                   plural_suffix='s'),
            'h': UnitQuantity(mag=3600., s=1., add_short_prefix=False),
            'hr': UnitQuantity(mag=3600., s=1., add_short_prefix=False),
            'hour': UnitQuantity(mag=3600., s=1., add_short_prefix=False,
                                 plural_suffix='s'),
            'day': UnitQuantity(mag=3600.*24., s=1., add_short_prefix=False,
                                plural_suffix='s'),
            'week': UnitQuantity(mag=3600.*24.*7., s=1.,
                                 add_short_prefix=False, plural_suffix='s'),
            'yr': UnitQuantity(mag=3600.*24.*365.25, s=1.,
                               add_short_prefix=False),
            'year': UnitQuantity(mag=3600.*24.*365.25, s=1.,
                                 add_short_prefix=False, plural_suffix='s'),
            # Amount
            'mol': UnitQuantity(mol=1.),
            'mole': UnitQuantity(mol=1., plural_suffix='s'),
            'molecule': UnitQuantity(mag=1./6.02214086e23, mol=1.,
                                     add_short_prefix=False,
                                     plural_suffix='s'),
            'molec': UnitQuantity(mag=1./6.02214086e23, mol=1.,
                                  add_short_prefix=False),
            'particle': UnitQuantity(mag=1./6.02214086e23, mol=1.,
                                     add_short_prefix=False, plural_suffix='s'),
            # Mass
            'g': UnitQuantity(mag=1.e-3, kg=1.),
            'gram': UnitQuantity(mag=1.e-3, kg=1., plural_suffix='s'),
            'u': UnitQuantity(mag=1./6.022e+26, kg=1., add_short_prefix=False),
            'amu': UnitQuantity(mag=1./6.022e+26, kg=1.,
                                add_short_prefix=False),
            'Da': UnitQuantity(mag=1./6.022e+26, kg=1.),
            'dalton': UnitQuantity(mag=1./6.022e+26, kg=1.,
                                   add_short_prefix=False, plural_suffix='s'),
            'lb': UnitQuantity(mag=1./2.20462, kg=1., add_short_prefix=False,
                               plural_suffix='s'),
            'pound': UnitQuantity(mag=1./2.20462, kg=1.,
                                  add_short_prefix=False, plural_suffix='s'),
            # Length
            'm': UnitQuantity(m=1.),
            'meter': UnitQuantity(m=1., add_short_prefix=False,
                                  plural_suffix='s'),
            'in': UnitQuantity(mag=1./39.3701, m=1., add_short_prefix=False,
                               add_long_prefix=False),
            'inch': UnitQuantity(mag=1./39.3701, m=1., add_short_prefix=False,
                                 plural_suffix='es', add_long_prefix=False),
            'ft': UnitQuantity(mag=1./3.28084, m=1., add_short_prefix=False),
            'foot': UnitQuantity(mag=1./3.28084, m=1., add_short_prefix=False),
            'feet': UnitQuantity(mag=1./3.28084, m=1., add_short_prefix=False),
            'mile': UnitQuantity(mag=1609.344, m=1., add_short_prefix=False,
                                 plural_suffix='s'),
            'Ang': UnitQuantity(mag=1.e-10, m=1., add_short_prefix=False),
            # Temperature
            'K': UnitQuantity(K=1., add_short_prefix=False,
                              add_long_prefix=False),
            'oC': UnitQuantity(K=1., add_short_prefix=False,
                               add_long_prefix=False),
            'R': UnitQuantity(mag=1.8, K=1., add_short_prefix=False,
                              add_long_prefix=False),
            'oF': UnitQuantity(mag=1.8, K=1., add_short_prefix=False,
                               add_long_prefix=False),
            # Current
            'A': UnitQuantity(A=1., add_long_prefix=False),
            'ampere': UnitQuantity(A=1., add_short_prefix=False,
                                   plural_suffix='s'),
            # Intensity
            'cd': UnitQuantity(cd=1., add_long_prefix=False),
            'candela': UnitQuantity(cd=1., add_short_prefix=False,
                                    plural_suffix='s'),
            # Volume
            'L': UnitQuantity(mag=1.e-3, m=3., add_long_prefix=False),
            'liter': UnitQuantity(mag=1.e-3, m=3., add_short_prefix=False,
                                  plural_suffix='s'),
            'gal': UnitQuantity(mag=1./264.172052, m=3., add_short_prefix=False,
                                add_long_prefix=False),
            'gallon': UnitQuantity(mag=1.e-3, m=3., add_short_prefix=False,
                                   add_long_prefix=False, plural_suffix='s'),
            # Acceleration
            'g0': UnitQuantity(mag=9.80665, m=1., s=-2., 
                               add_long_prefix=False),
            # Force
            'N': UnitQuantity(kg=1., m=1., s=-2., add_long_prefix=False),
            'newton': UnitQuantity(kg=1., m=1., s=-2., add_short_prefix=False,
                                   plural_suffix='s'),
            'dyn': UnitQuantity(mag=1.e-5, kg=1., m=1., s=-2.,
                                add_long_prefix=False),
            'dyne': UnitQuantity(mag=1.e-5, kg=1., m=1., s=-2.,
                                 add_short_prefix=False),
            'lbf': UnitQuantity(mag=4.448222, kg=1., m=1., s=-2.,
                                add_short_prefix=False, add_long_prefix=False),
            # Energy
            'J': UnitQuantity(kg=1., m=2., s=-2., add_long_prefix=False),
            'joule': UnitQuantity(kg=1., m=2., s=-2., add_short_prefix=False,
                                  plural_suffix='s'),
            'cal': UnitQuantity(mag=4.184, kg=1., m=2., s=-2.,
                                add_long_prefix=False),
            'calorie': UnitQuantity(mag=4.184, kg=1., m=2., s=-2.,
                                    add_short_prefix=False, plural_suffix='s'),
            'eV': UnitQuantity(mag=1.6021766208e-19, kg=1., m=2., s=-2.,
                               add_long_prefix=False),
            'Latm': UnitQuantity(mag=101.325, kg=1., m=2., s=-2.,
                                 add_short_prefix=False, add_long_prefix=False),
            'Eh': UnitQuantity(mag=4.3597447222071e-18, kg=1., m=2., s=-2.,
                               add_long_prefix=False, ),
            'Ha': UnitQuantity(mag=4.3597447222071e-18, kg=1., m=2., s=-2.,
                               add_long_prefix=False, ),
            'hartree': UnitQuantity(mag=4.3597447222071e-18, kg=1., m=2., s=-2.,
                                    add_short_prefix=False, plural_suffix='s'),
            'BTU': UnitQuantity(mag=1055., kg=1., m=2., s=-2,
                                add_short_prefix=False, add_long_prefix=False,
                                plural_suffix='s'),
            # Pressure
            'Pa': UnitQuantity(kg=1, m=-1, s=-2, add_long_prefix=False),
            'pascal': UnitQuantity(kg=1, m=-1, s=-2, add_short_prefix=False,
                                   plural_suffix='s'),
            'atm': UnitQuantity(mag=101325., kg=1, m=-1, s=-2,
                                add_short_prefix=False, add_long_prefix=False),
            'bar': UnitQuantity(mag=1.e5, kg=1, m=-1, s=-2, plural_suffix='s'),
            'mmHg': UnitQuantity(mag=133.322, kg=1, m=-1, s=-2,
                                 add_short_prefix=False, add_long_prefix=False),
            'torr': UnitQuantity(mag=133.322, kg=1, m=-1, s=-2,
                                 plural_suffix='s'),
            'Torr': UnitQuantity(mag=133.322, kg=1, m=-1, s=-2,
                                 plural_suffix='s'),
            'psi': UnitQuantity(mag=6894.76, kg=1, m=-1, s=-2,
                                add_short_prefix=False, add_long_prefix=False),
            # Charge
            'C': UnitQuantity(A=1., s=1., add_long_prefix=False),
            'coulomb': UnitQuantity(A=1., s=1., add_short_prefix=True,
                                    plural_suffix='s'),
            # Potential difference
            'V': UnitQuantity(kg=1., m=2., s=-3., A=-1., add_long_prefix=False),
            'volt': UnitQuantity(kg=1., m=2., s=-3., A=-1.,
                                 add_short_prefix=False, plural_suffix='s'),
            # Frequency
            'Hz': UnitQuantity(s=-1, add_long_prefix=False),
            'hertz': UnitQuantity(s=-1, add_long_prefix=False),
            # Capacitance
            'F': UnitQuantity(s=4, A=2, m=-2, kg=-1, add_long_prefix=False),
            'farad': UnitQuantity(s=4, A=2, m=-2, kg=-1,
                                  add_short_prefix=False, plural_suffix='s'),
            # Electric inductance
            'H': UnitQuantity(kg=1., m=2., s=-2, A=-2, add_long_prefix=False),
            'henry': UnitQuantity(kg=1., m=2., s=-2, A=-2, add_short_prefix=False),
            'henries': UnitQuantity(kg=1., m=2., s=-2, A=-2,
                                    add_short_prefix=False),
            # Power
            'W': UnitQuantity(kg=1., m=2, s=-3, add_long_prefix=False),
            'watt': UnitQuantity(kg=1., m=2, s=-3, add_short_prefix=False,
                                 plural_suffix='s'),
            # Electric resistance
            'ohm': UnitQuantity(kg=1., m=2, s=-3, A=-2, plural_suffix='s'),
            # Magnetic flux density
            'T': UnitQuantity(kg=1., s=-2, A=-1, 
                              add_long_prefix=False),
            'tesla': UnitQuantity(kg=1., s=-2, A=-1, add_short_prefix=False,
                                  plural_suffix='s'),
            # Magnetic flux
            'Wb': UnitQuantity(kg=1., m=2, s=-2, A=-1, add_long_prefix=False),
            'weber': UnitQuantity(kg=1., m=2, s=-2, A=-1,
                                  add_short_prefix=False, plural_suffix='s'),
        }

    # Add prefix and plural entries
    unit_db = _add_prefixes(unit_db)
    unit_db = _add_plural(unit_db)

    # Convert unit database to JSON format
    json_unit_db = {}
    for key, val in unit_db.items():
        json_unit_db[key] = val.to_dict()
    # Process filename
    if filename is None:
        filename = os.path.join(os.path.dirname(__file__), 'unit_db.json')
    # Process json_kwargs
    if json_kwargs is None:
        json_kwargs = {'indent': 2}
    # Write JSON file
    with open(filename, 'w') as f_ptr:
        json.dump(json_unit_db, f_ptr, **json_kwargs)
            
def read_unit_db(filename=None, json_lib='json'):
    """Updates unit database

    Parameters
    ----------
        filename : str, optional
            Name of database. If ``filename`` not specified, saves to
            vunits/db/unit_db.json.
    Returns
    -------
        unit_db : dict
            Outputted unit database. Keys should be strings of the units and the
            values are :class:`~vunits.quantity.Quantity` objects. If not
            specified, uses the default library.
    """
    # Process filename
    if filename is None:
        filename = os.path.join(os.path.dirname(__file__), 'unit_db.json')
    with open(filename, 'r') as f_ptr:
        json_unit_db = json.load(f_ptr)
    unit_db = {}
    for key, val in json_unit_db.items():
        unit_db[key] = Quantity.from_dict(val)
    return unit_db

def _add_prefixes(qty_dict):
    """Helper method to add prefixes to dictionary
    
    Parameters
    ----------
        qty_dict : dict
            Dictionary whose keys are the quantity name and values are the
            :class:`~vunits.quantity.UnitQuantity` objects. If a
            ``UnitQuantity`` has ``add_short_prefix`` set to ``False``,
            prefixes will not be added.
    Returns
    -------
        qty_dict_out : dict
            Dictionary with the updated prefix entries.
    """
    # Add prefixes to dictionary
    _prefix_unit_db = {}
    for base_unit, qty_obj in qty_dict.items():
        try:
            add_short_prefix = qty_obj.add_short_prefix
        except AttributeError:
            pass
        else:
            # Add short prefixes
            if qty_obj.add_short_prefix:
                for prefix, factor in short_prefixes.items():
                    new_unit = '{}{}'.format(prefix, base_unit)
                    new_obj = UnitQuantity._from_qty(
                            units=qty_obj.units, mag=qty_obj.mag*factor,
                            add_short_prefix=qty_obj.add_short_prefix,
                            add_long_prefix=qty_obj.add_long_prefix,
                            plural_suffix=qty_obj.plural_suffix)
                    _prefix_unit_db[new_unit] = new_obj
        # Add long prefixes
        try:
            add_long_prefix = qty_obj.add_long_prefix
        except AttributeError:
            pass
        else:
            if qty_obj.add_long_prefix:
                for prefix, factor in long_prefixes.items():
                    new_unit = '{}{}'.format(prefix, base_unit)
                    new_obj = UnitQuantity._from_qty(
                            units=qty_obj.units, mag=qty_obj.mag*factor,
                            add_short_prefix=qty_obj.add_short_prefix,
                            add_long_prefix=qty_obj.add_long_prefix,
                            plural_suffix=qty_obj.plural_suffix)
                    _prefix_unit_db[new_unit] = new_obj

    # Add entries with prefixes
    qty_dict_out = {**qty_dict, **_prefix_unit_db}
    return qty_dict_out

def _add_plural(qty_dict):
    """Helper method to add plural units to dictionary (e.g. seconds)
    
    Parameters
    ----------
        qty_dict : dict
            Dictionary whose keys are the quantity name and values are the
            :class:`~vunits.quantity.UnitQuantity` objects. If a
            ``UnitQuantity`` has ``add_short_prefix`` set to ``False``,
            prefixes will not be added.
    Returns
    -------
        qty_dict_out : dict
            Dictionary with the updated plural entries.
    """
    # Add prefixes to dictionary
    _plural_unit_db = {}
    for base_unit, qty_obj in qty_dict.items():
        # Skip species that do not allow prefixes
        try:
            plural_suffix = qty_obj.plural_suffix
        except AttributeError:
            pass
        if plural_suffix is None:
            continue

        new_unit = '{}{}'.format(base_unit, plural_suffix)
        _plural_unit_db[new_unit] = qty_obj
    # Add entries with prefixes
    qty_dict_out = {**qty_dict, **_plural_unit_db}
    return qty_dict_out

_temp_units = ('K', 'R', 'oC', 'oF')
"""tuple: Helper tuple to identify if a unit belongs to temperature."""

symmetry_dict = {
    'C1': 1,
    'Cs': 1,
    'C2': 2,
    'C2v': 2,
    'C3v': 3,
    'Cinfv': 1,
    'D2h': 4,
    'D3h': 6,
    'D5h': 10,
    'Dinfh': 2,
    'D3d': 6,
    'Td': 12,
    'Oh': 24
}
"""dict : Keys are point groups and the values are the symmetry numbers used for
rotational modes."""

atomic_weight = {
    1: 1.008,
    2: 4.002602,
    3: 6.938,
    4: 9.0121831,
    5: 10.806,
    6: 12.0116,
    7: 14.007,
    8: 15.999,
    9: 18.99840316,
    10: 20.1797,
    11: 22.98976928,
    12: 24.305,
    13: 26.9815385,
    14: 28.085,
    15: 30.973762,
    16: 32.06,
    17: 35.45,
    18: 39.948,
    19: 39.0983,
    20: 40.078,
    21: 44.955908,
    22: 47.867,
    23: 50.9415,
    24: 51.9961,
    25: 54.938044,
    26: 55.845,
    27: 58.933194,
    28: 58.6934,
    29: 63.546,
    30: 65.38,
    31: 69.723,
    32: 72.63,
    33: 74.921595,
    34: 78.971,
    35: 79.901,
    36: 83.798,
    37: 85.4678,
    38: 87.62,
    39: 88.90584,
    40: 91.224,
    41: 92.90637,
    42: 95.95,
    43: 98.,
    44: 101.07,
    45: 102.9055,
    46: 106.42,
    47: 107.8682,
    48: 112.414,
    49: 114.818,
    50: 118.71,
    51: 121.76,
    52: 127.6,
    53: 126.90447,
    54: 131.293,
    55: 132.905452,
    56: 137.327,
    57: 138.90547,
    58: 140.116,
    59: 140.90766,
    60: 144.242,
    61: 145,
    62: 150.36,
    63: 151.964,
    64: 157.25,
    65: 158.92535,
    66: 162.5,
    67: 164.93033,
    68: 167.259,
    69: 168.93422,
    70: 173.054,
    71: 174.9668,
    72: 178.49,
    73: 180.94788,
    74: 183.84,
    75: 186.207,
    76: 190.23,
    77: 192.217,
    78: 195.084,
    79: 196.966569,
    80: 200.592,
    81: 204.382,
    82: 207.2,
    83: 208.9804,
    84: 209.,
    85: 210.,
    86: 222.,
    87: 223.,
    88: 226.,
    89: 227.,
    90: 232.0377,
    91: 231.03588,
    92: 238.02891,
    93: 237.,
    94: 244.,
    95: 243.,
    96: 247.,
    97: 247.,
    98: 251.,
    99: 252.,
    100: 257.,
    101: 258.,
    102: 259.,
    103: 262.,
    104: 267.,
    105: 268.,
    106: 271.,
    107: 272.,
    108: 270.,
    109: 276.,
    110: 281.,
    111: 280.,
    112: 285.,
    113: 284.,
    114: 289.,
    115: 288.,
    116: 293.,
    118: 294.,
    'H': 1.008,
    'He': 4.002602,
    'Li': 6.938,
    'Be': 9.0121831,
    'B': 10.806,
    'C': 12.0116,
    'N': 14.007,
    'O': 15.999,
    'F': 18.99840316,
    'Ne': 20.1797,
    'Na': 22.98976928,
    'Mg': 24.305,
    'Al': 26.9815385,
    'Si': 28.085,
    'P': 30.973762,
    'S': 32.06,
    'Cl': 35.45,
    'Ar': 39.948,
    'K': 39.0983,
    'Ca': 40.078,
    'Sc': 44.955908,
    'Ti': 47.867,
    'V': 50.9415,
    'Cr': 51.9961,
    'Mn': 54.938044,
    'Fe': 55.845,
    'Co': 58.933194,
    'Ni': 58.6934,
    'Cu': 63.546,
    'Zn': 65.38,
    'Ga': 69.723,
    'Ge': 72.63,
    'As': 74.921595,
    'Se': 78.971,
    'Br': 79.901,
    'Kr': 83.798,
    'Rb': 85.4678,
    'Sr': 87.62,
    'Y': 88.90584,
    'Zr': 91.224,
    'Nb': 92.90637,
    'Mo': 95.95,
    'Tc': 98.,
    'Ru': 101.07,
    'Rh': 102.9055,
    'Pd': 106.42,
    'Ag': 107.8682,
    'Cd': 112.414,
    'In': 114.818,
    'Sn': 118.71,
    'Sb': 121.76,
    'Te': 127.6,
    'I': 126.90447,
    'Xe': 131.293,
    'Cs': 132.905452,
    'Ba': 137.327,
    'La': 138.90547,
    'Ce': 140.116,
    'Pr': 140.90766,
    'Nd': 144.242,
    'Pm': 145.,
    'Sm': 150.36,
    'Eu': 151.964,
    'Gd': 157.25,
    'Tb': 158.92535,
    'Dy': 162.5,
    'Ho': 164.93033,
    'Er': 167.259,
    'Tm': 168.93422,
    'Yb': 173.054,
    'Lu': 174.9668,
    'Hf': 178.49,
    'Ta': 180.94788,
    'W': 183.84,
    'Re': 186.207,
    'Os': 190.23,
    'Ir': 192.217,
    'Pt': 195.084,
    'Au': 196.966569,
    'Hg': 200.592,
    'Tl': 204.382,
    'Pb': 207.2,
    'Bi': 208.9804,
    'Po': 209.,
    'At': 210.,
    'Rn': 222.,
    'Fr': 223.,
    'Ra': 226.,
    'Ac': 227.,
    'Th': 232.0377,
    'Pa': 231.03588,
    'U': 238.02891,
    'Np': 237.,
    'Pu': 244.,
    'Am': 243.,
    'Cm': 247.,
    'Bk': 247.,
    'Cf': 251.,
    'Es': 252.,
    'Fm': 257.,
    'Md': 258.,
    'No': 259.,
    'Lr': 262.,
    'Rf': 267.,
    'Db': 268.,
    'Sg': 271.,
    'Bh': 272.,
    'Hs': 270.,
    'Mt': 276.,
    'Ds': 281.,
    'Rg': 280.,
    'Cn': 285.,
    'Uut': 284.,
    'Fl': 289.,
    'Uup': 288.,
    'Lv': 293.,
    'Uuo': 294.,
}
"""dict : Atomic weight. The key can be the atomic number, the element symbol,
or the element name"""

unit_db = read_unit_db()