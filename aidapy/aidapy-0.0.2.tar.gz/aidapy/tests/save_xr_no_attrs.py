import pytest
import numpy as np
from datetime import datetime
from aidapy import load_data


#start_time = datetime(2019, 3, 8, 13, 54, 53)
#end_time = datetime(2019, 3, 8, 13, 57, 00)


start_time = datetime(2019, 3, 8, 13, 56, 0)
end_time = datetime(2019, 3, 8, 13, 56, 30)


settings = {'prod': ['i_dist', 'dc_mag', 'sc_att', 'i_bulkv'],
	'probes': ['1'], 'coords': 'gse', 'mode': 'low_res', 'frame':'gse'}
xr_mms = load_data(mission='mms', start_time=start_time, end_time=end_time, **settings)
species = 'ion'
frame = 'B'
coordSys = 'spher'
v_max = 8.e5
resolution = 60
interp_schem = 'lin'
start_time_sub = datetime(start_time.year, start_time.month, start_time.day,
		      13, 56, 10)
end_time_sub = datetime(start_time.year, start_time.month, start_time.day,
		    13, 56, 20)

print(xr_mms)

xr_mms = xr_mms.vdf.interpolate(settings, start_time, end_time, start_time_sub, end_time_sub,
			    species=species, frame=frame, coord_sys=coordSys,
			    v_max=v_max, resolution=resolution, interp_schem=interp_schem,
			    verbose=False)

print(xr_mms['vdf_interp_time'].values)
target = np.array([1.1983741e-22, 1.3524926e-22, 1.1116379e-22, 1.1249207e-22,
		1.1723668e-22, 1.1025405e-22, 1.0375052e-22]).astype(np.float32)
result = np.nanmean(xr_mms['vdf_interp_time'].values, axis=(1,2)).astype(np.float32)

print(result)
for var_name in xr_mms.data_vars:
    local_da = xr_mms[var_name]
    local_da.attrs['pos_gse'] = 0
    local_da.attrs['Units'] = 0

xr_mms.to_netcdf('vdf.nc')
