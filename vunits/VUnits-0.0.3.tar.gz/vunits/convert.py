import numpy as np

from vunits.db import _temp_units
from vunits.quantity import Quantity, _force_get_quantity, _return_quantity
from vunits import constants as c

def convert_temp(num, initial, final):
    """Converts temperature from one unit set to another

    Parameters
    ----------
        num : float, optional
            Number to convert. I not specified, will return the appropriate
            conversion factor.
        initial : str
            Units that num is currently in. Accepted options include 'C', 'oC',
            'F', 'oF', 'R', 'K'.
        final : str
            Units you would like num to be in. Accepted options include 'C',
            'oC', 'F', 'oF', 'R', 'K'.
    Returns
    -------
        conversion_num : float
            num in the appropriate units
    Raises
    ------
        ValueError
            If unit types are not consistent or not supported
    """
    if num is None:
        num = 0.
    # Evaluating each combination
    initial_err_msg = 'Unsupported initial unit, {}.'.format(initial)
    final_err_msg = 'Unsupported final unit, {}.'.format(final)
    if initial == final:
        result = num
    elif initial == 'C' or initial == 'oC':
        if final == 'K':
            result = num + 273.15
        elif final == 'F' or final == 'oF':
            result = (num * 9./5.) + 32.
        elif final == 'R':
            result = (num + 273.15) * 1.8
        else:
            raise ValueError(final_err_msg)
    elif initial == 'K':
        if final == 'C' or final == 'oC':
            result = num - 273.15
        elif final == 'F' or final == 'oF':
            result = (num * 1.8) - 459.67
        elif final == 'R':
            result = num * 1.8
        else:
            raise ValueError(final_err_msg)
    elif initial == 'F' or initial == 'oF':
        if final == 'C' or final == 'oC':
            result = (num - 32.) * 5./9.
        elif final == 'K':
            result = (num + 459.67)/1.8
        elif final == 'R':
            result = num + 459.67
        else:
            raise ValueError(final_err_msg)
    elif initial == 'R':
        if final == 'C' or final == 'oC':
            result = num/1.8 - 273.15
        elif final == 'K':
            result = num/1.8
        elif final == 'F' or final == 'oF':
            result = num - 459.67
        else:
            raise ValueError(final_err_msg)
    else:
        raise ValueError(initial_err_msg)
    return result

def convert_unit(num=None, initial=None, final=None):
    """Converts units between two unit sets

    Parameters
    ----------
        num : float, optional
            Number to convert. If not specified, will return the appropriate
            conversion factor. Default is 0 for temperature-based units, 1
            otherwise.
        initial : str
            Units that num is currently in. Different units must be sparated by
            a ' ' or '/'. Supports powers as numbers after units. e.g. 'cm/s2',
            'cm s-2', or 'cm s^-2'.
        final : str
            Units you would like num to be in. Different units must be sparated
            by a ' ' or '/'. Supports powers as numbers after units. e.g.
            'cm/s2', 'cm s-2', or 'cm s^-2'.
    Returns
    -------
        conversion_num : float
            num in the appropriate units
    Raises
    ------
        ValueError
            If unit types are not consistent or not supported
    """
    if initial in _temp_units and final in _temp_units:
        if num is None:
            num = 0.
        return convert_temp(num=num, initial=initial, final=final)
    else:
        if num is None:
            num = 1.
        in_qty = Quantity.from_units(mag=num, units=initial)
        return in_qty(final)

def energy_to_freq(energy, units_in='J', return_quantity=False, units_out='Hz'):
    """Converts energy to frequency

    Parameters
    ----------
        energy : float or :class:`~vunits.quantity.Quantity` obj
            Energy
        units_in : str, optional
            Units corresponding to ``energy``. Default is 'J'.
        return_quantity: bool, optional
            If True, returns :class:`~vunits.quantity.Quantity`. Otherwise,
            returns float.
        units_out : str, optional
            Units corresponding to ``freq``. Default is 'Hz'.
    Returns
    -------
        freq : float or :class:`~vunits.quantity.Quantity` obj
            Frequency corresponding to ``units_out``.
    """
    energy_in = _force_get_quantity(obj=energy, units=units_in)
    qty_out = energy_in/c.h
    return _return_quantity(quantity=qty_out, return_quantity=return_quantity,
                            units_out=units_out)

def energy_to_temp(energy, units_in='J', return_quantity=False, units_out='K'):
    """Converts energy to temperature

    Parameters
    ----------
        energy : float
            Energy
        units_in : str, optional
            Units corresponding to ``energy``. Default is 'J'.
        return_quantity: bool, optional
            If True, returns :class:`~vunits.quantity.Quantity`. Otherwise,
            returns float.
        units_out : str, optional
            Units corresponding to ``temp``. Default is 'K'.
    Returns
    -------
        temp : float or :class:`~vunits.quantity.Quantity` obj
            Temperature  corresponding to ``units_out``.
    """
    energy_in = _force_get_quantity(obj=energy, units=units_in)
    qty_out = energy_in/c.kb
    return _return_quantity(quantity=qty_out, return_quantity=return_quantity,
                            units_out=units_out)

def energy_to_wavenumber(energy, units_in='J', return_quantity=False,
                         units_out='cm-1'):
    """Converts energy to wavenumber

    Parameters
    ----------
        energy : float
            Energy
        units_in : str, optional
            Units corresponding to ``energy``. Default is 'J'.
        return_quantity: bool, optional
            If True, returns :class:`~vunits.quantity.Quantity`. Otherwise,
            returns float.
        units_out : str, optional
            Units corresponding to ``wavenumber``. Default is 'cm-1'.
    Returns
    -------
        wavenumber : float or :class:`~vunits.quantity.Quantity` obj
            Wavenumber corresponding to ``units_out``.
    """
    energy_in = _force_get_quantity(obj=energy, units=units_in)
    qty_out = energy_in/c.h/c.c
    return _return_quantity(quantity=qty_out, return_quantity=return_quantity,
                            units_out=units_out)

def freq_to_energy(freq, units_in='Hz', return_quantity=False, units_out='J'):
    """Converts frequency to energy

    Parameters
    ----------
        freq : float
            Frequency
        units_in : str, optional
            Units corresponding to ``energy``. Default is 'Hz'.
        return_quantity: bool, optional
            If True, returns :class:`~vunits.quantity.Quantity`. Otherwise,
            returns float.
        units_out : str, optional
            Units corresponding to ``energy``. Default is 'J'.
    Returns
    -------
        energy : float or :class:`~vunits.quantity.Quantity` obj
            Energy corresponding to ``units_out``.
    """
    freq_in = _force_get_quantity(obj=freq, units=units_in)
    qty_out = freq_in*c.h
    return _return_quantity(quantity=qty_out, return_quantity=return_quantity,
                            units_out=units_out)

def freq_to_temp(freq, units_in='Hz', return_quantity=False, units_out='K'):
    """Converts frequency to temperature

    Parameters
    ----------
        freq : float
            Frequency
        units_in : str, optional
            Units corresponding to ``freq``. Default is 'Hz'.
        return_quantity: bool, optional
            If True, returns :class:`~vunits.quantity.Quantity`. Otherwise,
            returns float.
        units_out : str, optional
            Units corresponding to ``temp``. Default is 'K'.
    Returns
    -------
        temp : float or :class:`~vunits.quantity.Quantity` obj
            Temperature corresponding to ``units_out``.
    """
    freq_in = _force_get_quantity(obj=freq, units=units_in)
    qty_out = freq_in*c.h/c.kb
    return _return_quantity(quantity=qty_out, return_quantity=return_quantity,
                            units_out=units_out)

def freq_to_wavenumber(freq, units_in='Hz', return_quantity=False,
                       units_out='cm-1'):
    """Converts frequency to wavenumber

    Parameters
    ----------
        freq : float
            Frequency
        units_in : str, optional
            Units corresponding to ``freq``. Default is 'Hz'.
        return_quantity: bool, optional
            If True, returns :class:`~vunits.quantity.Quantity`. Otherwise,
            returns float.
        units_out : str, optional
            Units corresponding to ``wavenumber``. Default is 'cm-1'.
    Returns
    -------
        wavenumber : float or :class:`~vunits.quantity.Quantity` obj
            Wavenumber corresponding to ``units_out``.
    """
    freq_in = _force_get_quantity(obj=freq, units=units_in)
    qty_out = freq_in/c.c
    return _return_quantity(quantity=qty_out, return_quantity=return_quantity,
                            units_out=units_out)

def inertia_to_temp(inertia, units_in='kg m2', return_quantity=False,
                    units_out='K'):
    """Converts moment of inertia into rotational temperature

    Parameters
    ----------
        inertia : float
            Moment of inertia
        units_in : str, optional
            Units corresponding to ``inertia``. Default is 'kg m2'.
        return_quantity: bool, optional
            If True, returns :class:`~vunits.quantity.Quantity`. Otherwise,
            returns float.
        units_out : str, optional
            Units corresponding to ``temp``. Default is 'K'.
    Returns
    -------
        rot_temperature : float or :class:`~vunits.quantity.Quantity` obj
            Rotational temperature corresponding to ``units_out``.
    """
    inertia_in = _force_get_quantity(obj=inertia, units=units_in)
    qty_out = c.h_bar**2/2./c.kb/inertia_in
    return _return_quantity(quantity=qty_out, return_quantity=return_quantity,
                            units_out=units_out)

def temp_to_energy(temp, units_in='K', return_quantity=False, units_out='J'):
    """Converts temperature to energy

    Parameters
    ----------
        temp : float
            Temperature in K
        units_in : str, optional
            Units corresponding to ``temp``. Default is 'K'.
        return_quantity: bool, optional
            If True, returns :class:`~vunits.quantity.Quantity`. Otherwise,
            returns float.
        units_out : str, optional
            Units corresponding to ``energy``. Default is 'J'.
    Returns
    -------
        energy : float or :class:`~vunits.quantity.Quantity` obj
            Energy corresponding to ``units_out``.
    """
    temp_in = _force_get_quantity(obj=temp, units=units_in)
    qty_out = temp_in*c.kb
    return _return_quantity(quantity=qty_out, return_quantity=return_quantity,
                            units_out=units_out)

def temp_to_freq(temp, units_in='K', return_quantity=False, units_out='Hz'):
    """Converts temperature to frequency

    Parameters
    ----------
        temp : float
            Temperature in K
        units_in : str, optional
            Units corresponding to ``temp``. Default is 'K'.
        return_quantity: bool, optional
            If True, returns :class:`~vunits.quantity.Quantity`. Otherwise,
            returns float.
        units_out : str, optional
            Units corresponding to ``freq``. Default is 'Hz'.
    Returns
    -------
        freq : float or :class:`~vunits.quantity.Quantity` obj
            Frequency corresponding to ``units_out``.
    """
    temp_in = _force_get_quantity(obj=temp, units=units_in)
    qty_out = temp_in*c.kb/c.h
    return _return_quantity(quantity=qty_out, return_quantity=return_quantity,
                            units_out=units_out)

def temp_to_wavenumber(temp, units_in='K', return_quantity=False,
                       units_out='cm-1'):
    """Converts vibrational/rotational temperature to wavenumber

    Parameters
    ----------
        temp : float
            Temperature in K
        units_in : str, optional
            Units corresponding to ``temp``. Default is 'K'.
        return_quantity: bool, optional
            If True, returns :class:`~vunits.quantity.Quantity`. Otherwise,
            returns float.
        units_out : str, optional
            Units corresponding to ``wavenumber``. Default is 'cm-1'.
    Returns
    -------
        wavenumber : float or :class:`~vunits.quantity.Quantity` obj
            Wavenumber corresponding to ``units_out``.
    """
    temp_in = _force_get_quantity(obj=temp, units=units_in)
    qty_out = temp_in*c.kb/c.c/c.h
    return _return_quantity(quantity=qty_out, return_quantity=return_quantity,
                            units_out=units_out)

def wavenumber_to_energy(wavenumber, units_in='cm-1', return_quantity=False,
                         units_out='J'):
    """Converts wavenumbers to energies

    Parameters
    ----------
        wavenumber : float
            Wavenumber
        units_in : str, optional
            Units corresponding to ``wavenumber``. Default is '1/cm'.
        return_quantity: bool, optional
            If True, returns :class:`~vunits.quantity.Quantity`. Otherwise,
            returns float.
        units_out : str, optional
            Units corresponding to ``energy``. Default is 'J'.
    Returns
    -------
        energy : float or :class:`~vunits.quantity.Quantity` obj
            Energy corresponding to ``units_out``.
    """
    wavenumber_in = _force_get_quantity(obj=wavenumber, units=units_in)
    qty_out = wavenumber_in*c.c*c.h
    return _return_quantity(quantity=qty_out, return_quantity=return_quantity,
                            units_out=units_out)

def wavenumber_to_freq(wavenumber, units_in='cm-1', return_quantity=False,
                       units_out='Hz'):
    """Converts wavenumber to frequency

    Parameters
    ----------
        wavenumber : float
            Wavenumber
        units_in : str, optional
            Units corresponding to ``wavenumber``. Default is 'cm-1'.
        return_quantity: bool, optional
            If True, returns :class:`~vunits.quantity.Quantity`. Otherwise,
            returns float.
        units_out : str, optional
            Units corresponding to ``freq``. Default is 'Hz'.
    Returns
    -------
        freq : float or :class:`~vunits.quantity.Quantity` obj
            Frequency corresponding to ``units_out``.
    """
    wavenumber_in = _force_get_quantity(obj=wavenumber, units=units_in)
    qty_out = wavenumber_in*c.c
    return _return_quantity(quantity=qty_out, return_quantity=return_quantity,
                            units_out=units_out)

def wavenumber_to_inertia(wavenumber, units_in='cm-1', return_quantity=False,
                          units_out='kg m2'):
    """Converts wavenumber (1/cm) to moment of inertia

    Parameters
    ----------
        wavenumber : float
            Wavenumber
        units_in : str, optional
            Units corresponding to ``wavenumber``. Default is 'cm-1'.
        return_quantity: bool, optional
            If True, returns :class:`~vunits.quantity.Quantity`. Otherwise,
            returns float.
        units_out : str, optional
            Units corresponding to ``inertia``. Default is 'kg m2'.
    Returns
    -------
        mu : float or :class:`~vunits.quantity.Quantity` obj
            Moment of inertia corresponding to ``units_out``.
    """
    wavenumber_in = _force_get_quantity(obj=wavenumber, units=units_in)
    qty_out = c.h/(8.*np.pi**2*wavenumber_in*c.c)
    return _return_quantity(quantity=qty_out, return_quantity=return_quantity,
                            units_out=units_out)

def wavenumber_to_temp(wavenumber, units_in='cm-1', return_quantity=False,
                       units_out='K'):
    """Converts wavenumbers (1/cm) to temperatures (K)

    Parameters
    ----------
        wavenumber : float
            Wavenumber
        units_in : str, optional
            Units corresponding to ``wavenumber``. Default is 'cm-1'.
        return_quantity: bool, optional
            If True, returns :class:`~vunits.quantity.Quantity`. Otherwise,
            returns float.
        units_out : str, optional
            Units corresponding to ``temp``. Default is 'K'.
    Returns
    -------
        temperature : float or :class:`~vunits.quantity.Quantity` obj
            Temperature corresponding to ``units_out``.
    """
    wavenumber_in = _force_get_quantity(obj=wavenumber, units=units_in)
    qty_out = wavenumber_in*c.c*c.h/c.kb
    return _return_quantity(quantity=qty_out, return_quantity=return_quantity,
                            units_out=units_out)

def debye_to_einstein(debye_temperature):
    """Converts Debye temperature to Einstein temperature

    Parameters
    ----------
        debye_temperature : float
            Debye temperature in K
    Returns
    -------
        einstein_temperature : float
            Einstein temperature in K
    """
    return (np.pi/6.)**(1./3.)*debye_temperature


def einstein_to_debye(einstein_temperature):
    """Converts Einstein temperature to Debye temperature

    Parameters
    ----------
        einstein_temperature : float
            Einstein temperature in K
    Returns
    -------
        debye_temperature : float
            Debye temperature in K
    """
    return einstein_temperature/(np.pi/6.)**(1./3.)