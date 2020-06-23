import warnings
import pathlib as path
import shutil
import cdflib

import numpy as np
import pandas as pd
import xarray as xr
import astropy.units as u

from heliopy.data.util import _file_match, _load_raw_file, _checkdir,\
    timefilter, cdf_units, units_attach, _load_local, logger, NoDataError


def process(dirs, fnames, extension, local_base_dir, remote_base_url,
            download_func, processing_func, starttime, endtime,
            try_download=True, units=None,
            processing_kwargs={}, download_info=[], remote_fnames=None,
            xarray=False, warn_missing_units=True):
    """
    The main utility method for systematically loading, downloading, and saving
    data.

    Parameters
    ----------
    dirs : list
        A list of directories relative to *local_base_dir*.
    fnames : list or str or regex
        A list of filenames **without** their extension. These are the
        filenames that will be downloaded from the remote source. Must be the
        same length as *dirs*. Each filename is saved in it's respective entry
        in *dirs*. Can also be a regular expression that is used to match
        the filename (e.g. for version numbers)
    extension : str
        File extension of the raw files. **Must include leading dot**.
    local_base_dir : str
        Local base directory. ``fname[i]`` will be stored in
        ``local_base_dir / dirs[i] / fname[i] + extension``.
    remote_base_url : str
        Remote base URL. ``fname[i]`` will be downloaded from
        ``Remote / dirs[i] / fname[i] + extension``.
    download_func
        Function that takes

        - The remote base url
        - The local base directory
        - The relative directory (relative to the base url)
        - The local filename to download to
        - The remote filename
        - A file extension

        and downloads the remote file. The signature must be::

            def download_func(remote_base_url, local_base_dir,
                              directory, fname, remote_fname, extension)

        The function can also return the path of the file it downloaded,
        if this is different to the filename it is given. *download_func*
        can either silently do nothing if a given file is not available, or
        raise a `NoDataError` with a descriptive error message that will be
        printed.

    processing_func
        Function that takes an open CDF file or open plain text file,
        and returns a pandas DataFrame. The signature must be::

            def processing_func(file, **processing_kwargs)

    starttime : ~datetime.datetime
        Start of requested interval.
    endtime : ~datetime.datetime
        End of requested interval.
    try_download : bool, optional
        If ``True``, try to download data. If ``False`` don't.
        Default is ``True``.

    units : ~collections.OrderedDict, optional
        Manually defined units to be attached to the data that will be
        returned.

        Must map column headers (strings) to :class:`~astropy.units.Quantity`
        objects. If units are present, then a TimeSeries object is returned,
        else a Pandas DataFrame.

    processing_kwargs : dict, optional
        Extra keyword arguments to be passed to the processing funciton.

    download_info : list, optional
        A list with the same length as *fnames*, which contains extra info
        that is handed to *download_func* for each file individually.
    remote_fnames : list of str, optional
        If the remote filenames are different from the desired downloaded
        filenames, this should be a list of length ``len(fnames)`` with the
        files to be downloaded. The ordering must be the same as *fnames*.
    warn_missing_units : bool, optional
        If ``True``, warnings will be shown for each variable that does not
        have associated units.

    Returns
    -------
    :class:`~pandas.DataFrame` or :class:`~sunpy.timeseries.TimeSeries`
        Requested data.
    """
    local_base_dir = path.Path(local_base_dir)
    data = []
    if download_info == []:
        download_info = [None] * len(dirs)
    if remote_fnames is None:
        remote_fnames = fnames.copy()

    if len(dirs) != len(fnames):
        raise ValueError(
            'Must have the same number of directories as filenames')
    if len(fnames) != len(remote_fnames):
        raise ValueError(
            'Must have the same number of remote filenames as filenames')

    zips = zip(dirs, fnames, remote_fnames, download_info)
    for directory, fname, remote_fname, dl_info in zips:
        local_dir = local_base_dir / directory
        local_file = local_dir / fname

        # Try to load hdf file
        hdf_fname = _file_match(local_dir, fname + '.hdf')
        if hdf_fname is not None:
            hdf_file_path = local_dir / hdf_fname
            raw_file_path = hdf_file_path.with_suffix(extension)
            logger.info('Loading {}'.format(hdf_file_path))
            data.append(pd.read_hdf(hdf_file_path))
            continue

        # Try to load raw file
        raw_fname = _file_match(local_dir, fname + extension)
        if raw_fname is not None:
            raw_file_path = local_dir / raw_fname
            logger.info('Loading {}'.format(raw_file_path))
            df = _load_raw_file(raw_file_path,
                                processing_func, processing_kwargs)
            if df is not None:
                data.append(df)
                continue

        # If we can't find local file, try downloading
        if try_download:
            _checkdir(local_dir)
            args = ()
            if dl_info is not None:
                args = (dl_info,)
            try:
                new_path = download_func(remote_base_url, local_base_dir,
                                         directory, fname, remote_fname,
                                         extension, *args)
            except NoDataError as e:
                print(str(e))
                continue
            if new_path is not None:
                shutil.copy(new_path, local_file.with_suffix(extension))

            raw_fname = _file_match(local_dir, fname + extension)
            # Print a message if file hasn't been downloaded
            if raw_fname is not None:
                raw_file_path = local_dir / raw_fname
                df = _load_raw_file(raw_file_path,
                                    processing_func, processing_kwargs)
                if df is not None:
                    data.append(df)
                continue
            else:
                logger.info('File {}{}/{}{} not available remotely\n'.format(
                            remote_base_url, directory, fname, extension))
                continue
        else:
            msg = ('File {a}/{b}{c} not available locally,\n'
                   'and "try_download" set to False')
            logger.info(msg.format(a=local_dir, b=fname, c=extension))

    # Loaded all the data, now filter between times
    if xarray is True:
        data = xr_timefilter(data, starttime, endtime)
    else:
        data = timefilter(data, starttime, endtime)
        data = data.sort_index()

    # Attach units
    if extension == '.cdf':
        cdf = _load_local(raw_file_path)
        units = cdf_units(cdf, manual_units=units)

    if xarray is True:
        return units_xarray(data, units, warn_missing_units=warn_missing_units)
    else:
        return units_attach(data, units, warn_missing_units=warn_missing_units)


def cdf2xr(cdf, index_key, dtimeindex=True, badvalues=None, ignore=None,
           include=None, product_list=None):
    """
    Converts cdf file of spacecraft timeseries data to an xarray (DataArray or
    Dataset) object. xarray package is used as particle distribution functions
    are usually multidimensional (3/4D) datasets *f(time, energy, theta, phi)*.
    See http://xarray.pydata.org/en/stable/index.html for more information.
    Products to be loaded from the file must be passed as their corresponding
    key in the file. If not key is provided, all data from the file is loaded
    into a xarray.Dataset (with each key corresponding to a DataArray object).
    Keys must be provided as a dictionary. If the dictionary contains only one
    key, then 1D/2D dataset is assumed and loaded in a xarray.DataArray. If the
    dictionary contains more than 1 key, a 3D or 4D distribution function is
    assumed and an OrderedDict is required to load it with the following keys:
    {'dist','energy','theta'} or {'dist','energy','theta','phi'}, respectively.
    Parameters
    ----------
    cdf : cdf
        Opened cdf file.
    starttime : datetime.datetime object
        Start of desired time interval.
    endtime : datetime.datetime object
        End of desired time interval.
    index_key : string
        Time key of the opened cdf file.
    list_keys : dict, optional
        Dictionary of one or more keys corresponding to the desired products in
        the CDF file. If more than one key, and OrderedDict is required in the
        form: {'dist', 'energy', 'theta'} or {'dist', 'energy', 'theta', 'phi'}
        depending on the dimension of the dataset, to construct multidimension
        distribution function.
    Returns
    -------
    out : :class:`xarray.DataArray` or `xarray.Dataset`
        xarray object containing data from the open CDF file.
    """
    vars, keys, index = generate_vars_keys_index(
        cdf, index_key, dtimeindex=True, badvalues=None, ignore=None,
        include=None)
    ind = np.intersect1d(index, index, return_indices=True)[1]

    # If none of the required data in current CDF file, move on to the next one
    if len(index) == 0:
        return

    # If no product_list (cdf keys) is passed, load all data in xarray.Dataset
    if not product_list:
        data = xr.Dataset({})

        # Loop through each key and put data into the dataset
        for cdf_key in vars:
            df_key = keys[cdf_key]

            if isinstance(df_key, list):
                for i, subkey in enumerate(df_key):

                    try:
                        data_temp = xr.DataArray(
                            cdf.varget(cdf_key, None)[...][:, i])
                    except:
                        data_temp = xr.DataArray(
                            cdf.varget(cdf_key)[ind][:, i])

                    data[subkey] = data_temp
            else:
                try:
                    key_shape = cdf.varget(cdf_key,
                                           None)[...].shape
                except:
                    key_shape = cdf.varget(cdf_key)[ind].shape

                data_coords = []
                # Define coords in dataarray
                for i in np.arange(len(key_shape)):
                    data_coords += [np.arange(key_shape[i])]
                    data_coords[0] = index
                # Define dims in dataarray
                data_dims = np.arange(len(key_shape) - 1).tolist()
                # Convert to strings
                data_dims = ['dim_' + str(x) for x in data_dims]
                data_dims = ['time'] + data_dims
                try:
                    data_temp = xr.DataArray(cdf.varget(
                        cdf_key, None)[...],
                                             coords=data_coords,
                                             dims=data_dims)
                except:
                    data_temp = xr.DataArray(cdf.varget(cdf_key)[ind],
                                             coords=data_coords,
                                             dims=data_dims)
                data[df_key] = data_temp

    # If only one cdf key, put associated data in xarray.DataArray
    elif product_list and len(product_list) == 1:
        for cdf_key in product_list.values():
            data = cdf.varget(cdf_key, None, None, None)[...]

            if len(data.shape) == 0:
                raise ValueError('Loaded data is empty')

            elif len(data.shape) == 1:
                # Assumes time series
                data = xr.DataArray(data, coords=[index], dims=['time'])

            elif len(data.shape) == 2 and data.shape[1] <= 4:
                # Assumes 2D data with cartesian vector components
                data_coords = ['x', 'y', 'z', 'tot']
                data = xr.DataArray(
                    data, coords=[index, data_coords[:data.shape[1]]],
                    dims=['time', cdf_key])

            elif len(data.shape) == 2 and data.shape[1] > 4:
                # 2D data with undetermined components
                data_coords = np.arange(data.shape[1])
                data = xr.DataArray(
                    data, coords=[index, data_coords[:data.shape[1]]],
                    dims=['time', cdf_key])

            elif len(data.shape) == 3 and data.shape[1] <= 4:
                # Assumes 3D data with cartesian vector components
                # (e.g., pressure or temperature tensor)
                data_coords1 = ['x1', 'y1', 'z1']
                data_coords2 = ['x2', 'y2', 'z2']
                data = xr.DataArray(
                    data, coords=[index, data_coords1,
                                  data_coords2],
                    dims=['time', cdf_key + '1', cdf_key + '2'])

            else:
                raise ValueError('Data type not recognized')

            data.name = cdf_key

    # If more than 1 key, assumes distribution function (3D or more data)
    elif product_list and len(product_list) > 1:
        # Load coordinates and dimensions to match 'dist' shape
        coords = []
        dims = []
        keys = list(product_list.keys())
        for i, key in enumerate(keys):
            coords.append(cdf.varget(product_list[key], None, None, None)[...])
            dims.append(product_list[key])

            # If key is 2D, just take first dimension
            # (all coords are assumed constant)
            if len(coords[i].shape) == 2:
                coords[i] = coords[i][0, :]

        data = coords[0]
        coords[0] = index
        dims[0] = 'time'
        # Create the xarray.DataArray
        data = xr.DataArray(data, coords, dims)

        data.name = product_list['dist']
        data_units = cdf.varattsget(data.name)['UNITS']
        data.attrs[data.name] = data_units

    else:
        raise ValueError(
                'Unknown CDF key input: must be either empty or of dict type')

    return data


def xr_timefilter(data, starttime, endtime):
    """
    Concatenates a list of xarray.DataArray or xarray.Dataset along the 'time'
    dimension, and filters the resulting object between times.
    Parameters
    ----------
    data : :class: list
        Input data from different CDF files.
    starttime : datetime
        Start of interval.
    endtime : datetime
        End of interval.
    Returns
    -------
    out : :class:`xarray.DataArray` or `xarray.Dataset`
        Filtered data.
    """
    if len(data) == 0:
        raise RuntimeError(
            'No data available between {} and {}'.format(starttime, endtime))

    if isinstance(data, list) and 'time' in data[0].dims:
        # Make sure that the dataarrays indices do not overlap
        for i in np.arange(len(data) - 1):
            data[i] = data[i].sel(
                time=slice(data[i].time[0], data[i + 1].time[0]))

        # Concatenate the list along time
        data = xr.concat(data, dim='time')

    else:
        raise KeyError('The label "time" was not found in '
                       'the xarray coordinates')

    # Time filter the xarray
    data = data.sel(time=slice(starttime, endtime))

    return data


def units_xarray(data, units, warn_missing_units=True):
    """
    Takes the units defined by the user and attaches them to the xarray object.
    Units are attached as attributes to the xarray object and are accessible
    through the xarray attribute 'attrs'.
    Parameters
    ----------
    data : :class:`xarray.DataArray` or `xarray.Dataset`
        Input data. Object which needs to have units attached.
    units : :class:`collections.OrderedDict`
        The units manually defined by the user.
    Returns
    -------
    out : :class:`xarray.DataArray` or `xarray.Dataset`
        xarray object with units attached as attributes.
    """
    missing_msg = ('If you are trying to automatically download data '
                   'with HelioPy this is a bug, please report it at '
                   'https://github.com/heliopython/heliopy/issues')
    unit_key = list(units.keys())
    data_units = {}

    # If data is a xarray.DataArray
    if isinstance(data, xr.core.dataarray.DataArray) and data.name:
        if data.name not in unit_key:
            units[data.name] = u.dimensionless_unscaled
            if warn_missing_units:
                message = (f"{data.name} column has missing units."
                           f"\n{missing_msg}")
                warnings.warn(message, Warning)

        data_units[data.name] = units[data.name]

        for dim in data.dims:
            if dim == 'time':
                continue
            elif dim not in unit_key:
                units[dim] = u.dimensionless_unscaled
                if warn_missing_units:
                    message = (f"{dim} column has missing units."
                               f"\n{missing_msg}")
                    warnings.warn(message, Warning)
                data_units[dim] = units[dim]
            else:
                data_units[dim] = units[dim]

        data.attrs['Units'] = convert_units_to_str(data_units)

    # If data is a xarray.Dataset
    if isinstance(data, xr.core.dataset.Dataset):
        for data_var in data.data_vars:
            if data_var not in unit_key:
                units[data_var] = u.dimensionless_unscaled
                if warn_missing_units:
                    message = (f"{data[data_var]} column has missing units."
                               f"\n{missing_msg}")
                    warnings.warn(message, Warning)
                data_units[data_var] = units[data_var]
            else:
                data_units[data_var] = units[data_var]

        data.attrs['Units'] = convert_units_to_str(data_units)

    with warnings.catch_warnings():
        warnings.simplefilter(
            'ignore', 'Discarding nonzero nanoseconds in conversion')

    return data


def generate_vars_keys_index(cdf, index_key, dtimeindex=True, badvalues=None,
           ignore=None, include=None):
    if badvalues is not None:
        warnings.warn('The badvalues argument is decprecated, as bad values '
                      'are now automatically recognised using the FILLVAL CDF '
                      'attribute.', DeprecationWarning)
    if include is not None:
        if ignore is not None:
            raise ValueError('ignore and include are incompatible keywords')
        if isinstance(include, str):
            include = [include]
        if index_key not in include:
            include.append(index_key)

    # Extract index values
    index = cdf.varget(index_key)
    try:
        # If there are multiple indexes, take the first one
        # TODO: this is just plain wrong, there should be a way to get all
        # the indexes out
        index = index[...][:, 0]
    except IndexError:
        pass

    if dtimeindex:
        index = cdflib.epochs.CDFepoch.breakdown(index, to_np=True)
        index_df = pd.DataFrame({'year': index[:, 0],
                                 'month': index[:, 1],
                                 'day': index[:, 2],
                                 'hour': index[:, 3],
                                 'minute': index[:, 4],
                                 'second': index[:, 5],
                                 'ms': index[:, 6],
                                 })
        # Not all CDFs store pass milliseconds
        try:
            index_df['us'] = index[:, 7]
            index_df['ns'] = index[:, 8]
        except IndexError:
            pass
        index = pd.DatetimeIndex(pd.to_datetime(index_df), name='Time')
    npoints = index.shape[0]

    var_list = _get_cdf_vars(cdf)
    keys = {}
    # Get mapping from each attr to sub-variables
    for cdf_key in var_list:
        if ignore:
            if cdf_key in ignore:
                continue
        elif include:
            if cdf_key not in include:
                continue
        if cdf_key == 'Epoch':
            keys[cdf_key] = 'Time'
        else:
            keys[cdf_key] = cdf_key
    # Remove index key, as we have already used it to create the index
    keys.pop(index_key)
    # Remove keys for data that doesn't have the right shape to load in CDF
    # Mapping of keys to variable data
    vars = {cdf_key: cdf.varget(cdf_key) for cdf_key in keys.copy()}
    for cdf_key in keys:
        var = vars[cdf_key]
        if type(var) is np.ndarray:
            key_shape = var.shape
            if len(key_shape) == 0 or key_shape[0] != npoints:
                vars.pop(cdf_key)
        else:
            vars.pop(cdf_key)
    return vars, keys, index


def _get_cdf_vars(cdf):
    # Get list of all the variables in an open CDF file
    var_list = []
    cdf_info = cdf.cdf_info()
    for attr in list(cdf_info.keys()):
        if 'variable' in attr.lower() and len(cdf_info[attr]) > 0:
            for var in cdf_info[attr]:
                var_list += [var]

    return var_list


def convert_units_to_str(dict_input):
    dict_out = {}
    for k, v in dict_input.items():
        if isinstance(v, (u.Unit, u.UnrecognizedUnit, u.IrreducibleUnit,
                          u.CompositeUnit)):
            dict_out[k] = v.to_string()
        elif isinstance(v, u.Quantity):
            dict_out[k] = v.unit.to_string()
        else:
            raise ValueError('Problem to convert the units. There are not'
                             'astropy units or quantity')
    return dict_out
