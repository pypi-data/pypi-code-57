"""
Test for mms_vdf methods.
"""
import pytest
import numpy as np
import xarray as xr
from aidapy import aidaxr
from datetime import datetime

def test_vdf_mms():
    start_time = datetime(2019, 3, 8, 13, 54, 53)
    end_time = datetime(2019, 3, 8, 13, 57, 00)
    species = 'ion'
    frame = 'B'
    coordSys = 'spher'
    v_max = 8.e5
    resolution = 60
    interp_schem = 'lin'
    start_time_sub = datetime(start_time.year, start_time.month, start_time.day,
                              13, 56, 23, 160000)
    end_time_sub = datetime(start_time.year, start_time.month, start_time.day,
                            13, 56, 24, 225000)
    settings = {'prod': ['i_dist', 'dc_mag', 'sc_att', 'i_bulkv'],
                'probes': ['1'], 'coords': 'gse', 'mode': 'high_res', 'frame':'gse'}   
 
    xr_mms = xr.open_dataset('vdf.nc')

    xr_mms = xr_mms.vdf.interpolate(settings, start_time, end_time, start_time_sub, end_time_sub,
                                    species=species, frame=frame, coord_sys=coordSys,
                                    v_max=v_max, resolution=resolution, interp_schem=interp_schem,
                                    verbose=False)
    target = np.array([1.1983741e-22, 1.3524926e-22, 1.1116379e-22, 1.1249207e-22,
                        1.1723668e-22, 1.1025405e-22, 1.0375052e-22]).astype(np.float32)
    result = np.nanmean(xr_mms['vdf_interp_time'].values, axis=(1,2)).astype(np.float32)
    # This test will potentially fail if MMS data are updated...
    assert np.allclose(target, result, atol=1.e-24)
