from datetime import datetime
import pytest

from heliopy_multid.data.test.util import check_data_output_xr

import heliopy_multid.data.mms as mms

starttime = datetime(2016, 1, 2, 0, 0, 0)
endtime = datetime(2016, 1, 2, 1, 0, 0)
probes = ['1', '4']


# Test xarrays as outputs
@pytest.mark.parametrize("probe", probes)
def test_fgm_xr(probe):
    data = mms.fgm(probe, 'srvy', starttime, endtime, xarray=True)
    check_data_output_xr(data)


@pytest.mark.parametrize("probe", probes)
def test_fpi_dis_moms_xr(probe):
    data = mms.fpi_dis_moms(probe, 'fast', starttime, endtime, xarray=True)
    check_data_output_xr(data)


@pytest.mark.parametrize("probe", probes)
def test_fpi_des_moms_xr(probe):
    data = mms.fpi_des_moms(probe, 'fast', starttime, endtime, xarray=True)
    check_data_output_xr(data)


@pytest.mark.parametrize("probe", probes)
def test_fpi_dis_dist_xr(probe):
    data = mms.fpi_dis_dist(probe, 'fast', starttime, endtime, xarray=True)
    check_data_output_xr(data)


@pytest.mark.parametrize("probe", probes)
def test_fpi_des_dist_xr(probe):
    data = mms.fpi_des_dist(probe, 'fast', starttime, endtime, xarray=True)
    check_data_output_xr(data)
