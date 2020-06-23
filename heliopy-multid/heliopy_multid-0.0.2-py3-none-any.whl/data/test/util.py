import warnings
import numpy as np
import astropy.units as u


def check_data_output_xr(data):
    """
    Function to check that the output of a data fetch method.
    """
    #check_units_xr(data)
    check_datetime_index_xr(data)
    assert len(data.time) > 0
    assert len(data.data_vars) > 0
    for var in data.data_vars:
        assert data[str(var)].shape[0] > 0


def check_datetime_index_xr(data):
    'Helper function to check all dataframes have a datetime index'
    for timetag in data.time.values:
        assert isinstance(timetag, np.datetime64)


def check_units_xr(data):
    if not data.attrs['Units']:
        warnings.warn("Function has no units attached", RuntimeWarning)
    else:
        for unit in data.attrs['Units'].values():
            assert isinstance(unit, (u.Unit, u.UnrecognizedUnit,
                                     u.IrreducibleUnit, u.CompositeUnit))
