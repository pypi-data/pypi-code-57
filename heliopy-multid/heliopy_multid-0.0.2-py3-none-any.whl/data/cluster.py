from datetime import datetime, time

from heliopy.data import util
from heliopy.data.cluster import cluster_dir, csa_url, _download

from heliopy_multid.data.util import cdf2xr, process


def _load(probe, starttime, endtime, instrument, product_id,
          try_download, product_list=None, xarray=False):
    dirs = []
    fnames = []
    download_info = []
    for day in util._daysplitinterval(starttime, endtime):
        date = day[0]
        year = str(date.year)
        month = str(date.month).zfill(2)
        day = str(date.day).zfill(2)

        dirs.append(year)
        local_fname = 'C' + probe + '_' + product_id + '__' +\
            year + month + day
        fnames.append(local_fname)
        thisstart = datetime.combine(date, time.min)
        thisend = datetime.combine(date, time.max)
        download_info.append((thisstart, thisend))

    extension = '.cdf'
    local_base_dir = cluster_dir / ('c' + probe) / instrument
    remote_base_url = csa_url

    def download_func(remote_base_url, local_base_dir,
                      directory, fname, remote_fname, extension,
                      download_info):
        starttime, endtime = download_info
        _download(probe, starttime, endtime, instrument, product_id)

    def processing_func(file):
        for non_empty_var in list(file.cdf_info().keys()):
            if 'variable' in non_empty_var.lower():
                if len(file.cdf_info()[non_empty_var]) > 0:
                    var_list = non_empty_var
                    break

        for key in file.cdf_info()[var_list]:
            if 'CDF_EPOCH' in file.varget(key, expand=True).values():
                index_key = key
                break

        if xarray is True:
            return cdf2xr(file, index_key, product_list=product_list)
        else:
            return util.cdf2df(file, index_key)

    return process(dirs, fnames, extension, local_base_dir,
                   remote_base_url, download_func, processing_func,
                   starttime, endtime, try_download=try_download,
                   units=None, xarray=xarray,
                   download_info=download_info)


def fgm(probe, starttime, endtime, try_download=True, xarray=False):
    """
    Download fluxgate magnetometer data.

    See https://caa.estec.esa.int/documents/UG/CAA_EST_UG_FGM_v60.pdf for more
    information on the FGM data.

    Parameters
    ----------
        probe : string
            Probe number. Must be '1', '2', '3', or '4'.
        starttime : datetime
            Interval start.
        endtime : datetime
            Interval end.
        try_download : bool
            Download file.
        want_xr : bool
            If want xarray.

    Returns
    -------
        data : :class:`~sunpy.timeseries.TimeSeries`
            Requested data.
    """
    return _load(probe, starttime, endtime, 'fgm', 'CP_FGM_FULL',
                 try_download=try_download, xarray=xarray)


def cis_codif_h1_moms(probe, starttime, endtime, sensitivity='high',
                      try_download=True, xarray=False):
    """
    Load H+ moments from CIS instrument.

    See https://caa.estec.esa.int/documents/UG/CAA_EST_UG_CIS_v35.pdf for more
    information on the CIS data.

    Parameters
    ----------
    probe : string
        Probe number. Must be '1', '2', '3', or '4'.
    starttime : datetime
        Interval start.
    endtime : datetime
        Interval end.import pathlib as path
    sensitivity : string, 'high' or 'low', default: 'low'
        Load high or low sensitivity

    Returns
    -------
    data : DataFrame
        Requested data.
    """
    sensitivitydict = {'high': 'HS', 'low': 'LS'}
    sensitivity = sensitivitydict[sensitivity]
    endstr = '_CP_CIS-CODIF_' + sensitivity + '_H1_MOMENTS'
    return _load(probe, starttime, endtime, 'peace', endstr[1:],
                 try_download=try_download, xarray=xarray)


def peace_moments(probe, starttime, endtime, try_download=True, xarray=False):
    """
    Download electron moments from the PEACE instrument.

    See https://caa.estec.esa.int/documents/UG/CAA_EST_UG_PEA_v25.pdf for more
    information on the PEACE data.

    Parameters
    ----------
        probe : string
            Probe number. Must be '1', '2', '3', or '4'.
        starttime : datetime
            Interval start.
        endtime : datetime
            Interval end.
        try_download : bool
            Download file.
        want_xr : bool
            If want xarray.

    Returns
    -------
        data : DataFrame
            Requested data.
    """
    return _load(probe, starttime, endtime, 'peace', 'CP_PEA_MOMENTS',
                 try_download=try_download, xarray=xarray)


def cis_hia_onboard_moms(probe, starttime, endtime, try_download=True,
                         xarray=False):
    """
    Download onboard ion moments from the CIS instrument.

    See https://caa.estec.esa.int/documents/UG/CAA_EST_UG_CIS_v35.pdf for more
    information on the CIS data.

    Parameters
    ----------
        probe : string
            Probe number. Must be '1' or '3'
        starttime : datetime
            Interval start.
        endtime : datetime
            Interval end.
        try_download : bool
            Download file.
        want_xr : bool
            If want xarray.

    Returns
    -------
        data : DataFrame
            Requested data.
    """
    if probe in ['2', '4']:
        raise ValueError('Onboard ion moment data is not available for '
                         'cluster probes 2 or 4')
    data = _load(probe, starttime, endtime, 'cis',
                 'CP_CIS-HIA_ONBOARD_MOMENTS',
                 try_download=try_download, xarray=xarray)
    return data
