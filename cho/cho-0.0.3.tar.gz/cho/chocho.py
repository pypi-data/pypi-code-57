# RADIANCE and IRRADIANCE

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
from pathlib import Path
import os, sys, pickle
import numpy as np
import xarray as xr
from matplotlib import pyplot as plt
from netCDF4 import Dataset
from scipy import linalg
import scipy as sp
from matplotlib import pyplot as plt
from scipy.interpolate import splev, splrep, pchip, UnivariateSpline

def fetch_s5p(date_range, roi, download_folder, producttype = 'L1B_RA_BD4', paci_rad = False):
    if download_folder == ".":
        download_folder = Path.cwd().joinpath("data")
    else:
        if not isinstance(download_folder, Path):
            download_folder = Path(download_folder)
    if not download_folder.exists(): os.makedirs(download_folder.as_posix())
    
    api = SentinelAPI(user='s5pguest', password='s5pguest', api_url='https://s5phub.copernicus.eu/dhus')
    products = api.query(
        roi,
        date = date_range,
        producttype = producttype
    )
    

    # convert to Pandas DataFrame
    products_df = api.to_dataframe(products)
    products_df.to_csv(download_folder.joinpath("meta.csv"))
    
    if paci_rad:
        # sort and limit to first sorted products
        products_df_sorted = products_df.sort_values(['summary'], ascending=[True])
        products_df = products_df_sorted.head(1)
        
    filenames = products_df["filename"].values
    # print(filenames)
    
    

    # download sorted and reduced products
    api.download_all(products_df.index,  directory_path = download_folder.as_posix())
    
    return filenames

def pacific_radiance(date_range, download_folder = "data/pacific"):
    download_folder = Path.cwd().joinpath(download_folder)
    longitude = 150
    latitude = 20
    roi = f'POINT ({longitude} {latitude})'
    
    filenames = fetch_s5p(date_range, roi, download_folder, paci_rad = True)
    
    for filename in filenames:
        filename = download_folder.joinpath(filename)
        cur_name = filename.with_suffix(".zip")
        cur_name.rename(filename)
        
        s5p_observations = xr.open_dataset(filename, group='/BAND4_RADIANCE/STANDARD_MODE/OBSERVATIONS')
        # print(s5p_observations)
        # print(s5p_observations["spectral_channel"].data)
        s5p_geo = xr.open_dataset(filename, group='/BAND4_RADIANCE/STANDARD_MODE/GEODATA')
        # print(s5p_geo)
        print("*"*40)
        # print(s5p_geo["latitude"].data.shape)



        lats = s5p_geo["latitude"].data[0, :, :]
        lons = s5p_geo["longitude"].data[0, :, :]
        radiance = s5p_observations["radiance"].data

        # print(lats.shape, lons.shape, radiance.shape)

        # 140  # 30
        idxs = np.where(
                (np.abs(lons - longitude) < 20) & \
                (np.abs(lats - latitude) < 10)
            )

        # print(idxs)
        # print(lons[idxs], lats[idxs])
        rad = np.average(radiance[0, idxs[0], idxs[1], :], axis = 0)
        # print(rad.shape)
        
        s5p_observations.close()
        s5p_geo.close()

        filename.rename(cur_name)
        
        return rad

def inversion(reflectance, wavelengths):
    fixed_band = np.arange(433, 465, step = 0.5)
    xsecs = extract_xsecs(fixed_band)

    nrow, ncol, nband = reflectance.shape
    # print(nrow, ncol)

    scd = []

    for col in range(ncol):
        bands = wavelengths[col, :]
        for row in range(nrow):
            try:
                ref = reflectance[row, col, :]
                tck = splrep(bands, ref)
                new_ref = splev(fixed_band, tck)

                fCurve3p = sp.polyfit(fixed_band, new_ref, 3)
                fCurve3 = sp.polyval(fCurve3p, fixed_band)
                dif = new_ref - fCurve3

                chocho = np.abs(linalg.lstsq(xsecs, dif)[0][0])
                # chocho = linalg.lstsq(xsecs, dif)[0][0]
                # print(chocho)
                scd.append(chocho)

                # plt.plot(bands, ref)
                # plt.plot(fixed_band, new_ref)
                # plt.show()
            except Exception as e:
                # print(e)
                scd.append(-9999.)
    return np.array(scd).reshape(nrow, ncol)

def extract_xsecs(fixed_band, xsec_path = "data/xsec.npz"):
    xsecs = []
    xsec_path = Path.cwd().joinpath(xsec_path)
    containers = np.load(xsec_path)
    for gas in containers.keys():
        # print(gas)
        bands = containers[gas][:, 0]
        ref = containers[gas][:, 1]

        tck = splrep(bands, ref)
        new_ref = splev(fixed_band, tck)

        fCurve3p = sp.polyfit(fixed_band, new_ref, 3)
        fCurve3 = sp.polyval(fCurve3p, fixed_band)
        dif = new_ref - fCurve3
    #     new_ref = interp_(bands, ref, fixed_band)
    #     dif = polfitdif(bands, new_ref)

        xsecs.append(dif)
    xsecs = np.array(xsecs).T
    return xsecs
    
def chocho_inversion(date_range, pacific, download_folder = "data/radiance"):
    download_folder = Path.cwd().joinpath(download_folder)
    roi = geojson_to_wkt(read_geojson('roi.geojson'))
    # print(roi)
    
    filenames = fetch_s5p(date_range, roi, download_folder)
    
    for count, filename in enumerate(filenames):
        filename = download_folder.joinpath(filename)
        cur_name = filename.with_suffix(".zip")
        cur_name.rename(filename)
        
        s5p_observations = xr.open_dataset(filename, group='/BAND4_RADIANCE/STANDARD_MODE/OBSERVATIONS')
        # print(s5p_observations)
        # print(s5p_observations["spectral_channel"].data)
        s5p_geo = xr.open_dataset(filename, group='/BAND4_RADIANCE/STANDARD_MODE/GEODATA')
        # print(s5p_geo)
        s5p = Dataset(filename, mode = "r")
        wavelengths = s5p['BAND4_RADIANCE/STANDARD_MODE/INSTRUMENT/nominal_wavelength'][:][0,:,:]
        # print(s5p_instru)
        print("*"*40)
        # print(s5p_geo["latitude"].data.shape)



        lats = s5p_geo["latitude"].data[0, :, :]
        lons = s5p_geo["longitude"].data[0, :, :]
        radiance = s5p_observations["radiance"].data[0, :, :]

        nrow, ncol, nband = radiance.shape
        radiance = radiance.reshape(nrow * ncol, nband)

        reflectance = np.array(
            [rad / pacific for rad in radiance]
        )
        
        reflectance = reflectance.reshape(nrow, ncol, nband)
        
        s5p_observations.close()
        s5p_geo.close()
        s5p.close()
        
        filename.rename(cur_name)
        
        chocho_columns = inversion(reflectance, wavelengths)
        
        chocho_dict = {
            "chocho": chocho_columns,
            "longitude": lons,
            "latitude": lats
        }
        
        with open(f"data/{filename.stem}_chocho.pkl", "wb") as f:
            pickle.dump(chocho_dict, f, protocol=pickle.HIGHEST_PROTOCOL)
    print("Inversion complete")

# # example:
# pacific = pacific_radiance(['20190101','20190102'], download_folder = "data/pacific")
# chocho_inversion(['20190101','20190102'], pacific, download_folder = "data/radiance")