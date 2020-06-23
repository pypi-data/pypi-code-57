import pathlib
import requests
import os
from tqdm.auto import tqdm

from heliopy.data import util
from heliopy.data.mms import _validate_instrument, _validate_probe,\
    available_files, _fpi_docstring, mms_dir, dl_url

from heliopy_multid.data.util import cdf2xr, process


def download_files(probe, instrument, data_rate, starttime, endtime,
                   product_list=None, verbose=True, product_string='',
                   warn_missing_units=True, xarray=False):
    """
    Download MMS files.

    Parameters
    ----------
    probe : int or str
        MMS probe number. Must be in 1-4 inclusive.
    instrument : str
        MMS instrument. Must be in ``['afg', 'aspoc', 'dfg', 'dsp', 'edi',
        'edp', 'fields', 'scm', 'sdp']``
    data_rate : str
        Data rate. Must be in ``['slow', 'fast', 'brst', 'srvy']``
    starttime : ~datetime.datetime
        Start time.
    endtime : ~datetime.datetime
        End time.
    verbose : bool, optional
        If ``True``, show a progress bar while downloading.
    product_string : str, optional
        If not empty, this string must be in the filename for it to be
        downloaded.
    warn_missing_units : bool, optional
        If ``True``, warnings will be shown for each variable that does not
        have associated units.

    Returns
    -------
    df : :class:`~sunpy.timeseries.GenericTimeSeries`
        Requested data.
    """
    _validate_instrument(instrument)
    probe = _validate_probe(probe)

    dirs = []
    fnames = []
    daylist = util._daysplitinterval(starttime, endtime)
    for date, stime, etime in daylist:
        files = available_files(probe, instrument, starttime, endtime,
                                data_rate, product_string)
        for file in files:
            fname = pathlib.Path(file).stem
            if product_string in fname and len(fname):
                fnames.append(fname)
                dirs.append('')

    extension = '.cdf'
    local_base_dir = mms_dir / probe / instrument / data_rate
    remote_base_url = dl_url

    def download_func(remote_base_url, local_base_dir,
                      directory, fname, remote_fname, extension):
        url = remote_base_url + '?file=' + fname + extension
        local_fname = os.path.join(local_base_dir, fname + extension)
        with requests.get(url, stream=True) as request:
            with open(local_fname, 'wb') as fd:
                for chunk in tqdm(
                        request.iter_content(chunk_size=128)):
                    fd.write(chunk)

    def processing_func(cdf):
        if xarray is True:
            return cdf2xr(cdf, index_key='Epoch', product_list=product_list)
        else:
            return util.cdf2df(cdf, index_key='Epoch')

    return process(dirs, fnames, extension, local_base_dir,
                   remote_base_url, download_func, processing_func,
                   starttime, endtime, xarray=xarray,
                   warn_missing_units=warn_missing_units)


def fpi_dis_moms(probe, mode, starttime, endtime, product_list=None,
                 xarray=False):
    return download_files(probe, 'fpi', mode, starttime, endtime,
                          product_string='dis-moms',
                          product_list=product_list, xarray=xarray)


fpi_dis_moms.__doc__ = _fpi_docstring('ion distribution moment')


def fpi_des_moms(probe, mode, starttime, endtime, product_list=None,
                 xarray=False):
    return download_files(probe, 'fpi', mode, starttime, endtime,
                          product_string='des-moms',
                          product_list=product_list, xarray=xarray)


fpi_des_moms.__doc__ = _fpi_docstring('electron distribution moment')


def fpi_dis_dist(probe, mode, starttime, endtime, product_list=None,
                 xarray=False):
    return download_files(probe, 'fpi', mode, starttime, endtime,
                          product_string='dis-dist', warn_missing_units=False,
                          product_list=product_list, xarray=xarray)


fpi_dis_dist.__doc__ = _fpi_docstring('ion distribution function')


def fpi_des_dist(probe, mode, starttime, endtime, product_list=None,
                 xarray=False):
    return download_files(probe, 'fpi', mode, starttime, endtime,
                          product_string='des-dist', warn_missing_units=False,
                          product_list=product_list, xarray=xarray)


fpi_des_dist.__doc__ = _fpi_docstring('electron distribution function')


def fgm(probe, mode, starttime, endtime, product_list=None, xarray=False):
    """
    Import fgm survey mode magnetic field data.

    Parameters
    ----------
    probe : string
        Probe number, must be 1, 2, 3, or 4
    mode : str
        Data rate.
    starttime : datetime
        Interval start time.
    endtime : datetime
        Interval end time.

    Returns
    -------
    data : :class:`~sunpy.timeseries.TimeSeries`
        Imported data.
    """
    return download_files(probe, 'fgm', mode, starttime, endtime,
                          product_list=product_list, xarray=xarray)
