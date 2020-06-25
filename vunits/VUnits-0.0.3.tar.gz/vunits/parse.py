import re
from vunits.quantity import Quantity
from vunits.db import unit_db, _temp_units

def _parse_unit(mag=1., units='', unit_db=None):
    """Helper method to parse units

    Parameters
    ----------
        mag : float, optional
            Magnitude of :class:`~vunits.quantity.Quantity`
        units : str, optional
            Units to parse. Different units must be sparated by a space (' ') or
            forward slash ('/'). Supports powers as numbers after units.
            e.g. 'cm/s2', 'cm s-2', or 'cm s^-2'. Default is ''.
        unit_db : dict, optional
            Unit database to use parse units. Keys should be strings of
            expected units and values are :class:`~vunits.quantity.Quantity`
            objects. If ``unit_db`` is not specified, uses the
            ``vunits.db.unit_db``.
    Returns
    -------
        quantity : :class:`~vunits.quantity.Quantity`
            New quantity object.
    """
    # Load appropriate database
    if unit_db is None:
        from vunits.db import unit_db as vunits_units_db
        unit_db = vunits_units_db
    # Check if temperature unit and parse independently
    if units in _temp_units:
        from vunits.convert import convert_temp
        mag = convert_temp(num=mag, initial=units, final='K')
        quantity_out = Quantity(mag=mag, K=1.)
    else:
        # Separate numerators
        units_list1 = units.split(' ')

        # Separate denominators
        units_list2 = []
        units_pow2 = []
        for coupled_units in units_list1:
            units_list = coupled_units.split('/')
            units_list2.extend(units_list)

            # Add powers
            units_pow = [1] + [-1]*(len(units_list)-1)
            units_pow2.extend(units_pow)

        # Remove powers if any
        units_list3 = []
        units_pow3 = []
        # Pattern detects powers given to units. e.g. J^2, m10, s-2
        power_pattern = re.compile(r'\^*-*[0-9]*\.*[0-9]+')
        for i, units2 in enumerate(units_list2):
            match = power_pattern.search(units2)
            if match is None:
                power_str = ''
                power_float = float(units_pow2[i])
            else:
                power_str = match.group(0)
                # Remove ^ character and convert to a float
                power_float = float(power_str.replace('^', ''))*units_pow2[i]
            unit = units2.replace(power_str, '')
            units_list3.append(unit)
            units_pow3.append(power_float)

        # Create Quantity object
        quantity_out = Quantity(mag=mag)
        for unit, power in zip(units_list3, units_pow3):
            try:
                quantity_out *= unit_db[unit]**power
            except KeyError:
                err_msg = ('When trying to parse "{}", encountered unit "{}", '
                           'which is not supported.'
                           ''.format(units, unit))
                raise ValueError(err_msg)
    return quantity_out
