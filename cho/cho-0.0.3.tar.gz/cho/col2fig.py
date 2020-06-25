import pickle
import numpy as np
from netCDF4 import Dataset
from scipy.interpolate import griddata
from shapely.geometry import Polygon, MultiPoint
from matplotlib import pyplot as plt

def load_hcho_level2(filename):
    ds = Dataset(filename, mode = "r")
    hcho = ds["PRODUCT/formaldehyde_tropospheric_vertical_column"][:][0, :, :]
    lats = ds["PRODUCT/latitude"][:][0, :, :]
    lons = ds["PRODUCT/longitude"][:][0, :, :]
    ds.close()
    idx = np.where((np.isfinite(hcho) == True) & (lats > -40) & (lats < 40))
    # v stands for valid
    vhcho = np.array(hcho[idx])
    vlats = np.array(lats[idx].reshape(-1, 1))
    vlons = np.array(lons[idx].reshape(-1, 1))

    coors = np.hstack([vlons, vlats])
    return coors, vhcho

def load_chocho(filename):
    with open(filename, "rb") as f:
        ds = pickle.load(f)
        lons = ds["longitude"]
        lats = ds["latitude"]
        chocho = ds["chocho"]
        idx = np.where((lats > -40) & (lats < 40))
        chocho = chocho[idx].reshape(-1, 1)
        lons = lons[idx].reshape(-1, 1)
        lats = lats[idx].reshape(-1, 1)
    coors = np.hstack([lons, lats])
    return coors, chocho

def point2grid(coors, values, r = 0.075):
    poly = Polygon(coors).buffer(0)

    # # Method 1:
    xmin, ymin, xmax, ymax = poly.bounds
    # xmin = np.min(vlons)
    # ymin = np.min(vlats)
    # xmax = np.max(vlons)
    # ymax = np.max(vlats)
    x = np.arange(xmin, xmax, r)
    y = np.arange(ymin, ymax, r)
    points = MultiPoint(np.transpose([np.tile(x, len(y)), np.repeat(y, len(x))]))
    points = points.intersection(poly)

    # # Method 2:
    # grid_lon, grid_lat = np.meshgrid(
    #     np.arange(np.min(vlons), np.max(vlons), 1), 
    #     np.arange(np.min(vlats), np.max(vlats), 1)
    # )
    # points = MultiPoint(
    #     np.transpose([grid_lon.ravel(), grid_lat.ravel()])
    # )
    # points = points.intersection(poly)

    # valid grid coors
    vgcoors = np.array(
        [[pp.x, pp.y] for pp in points]
    )
    vgrid_lon = vgcoors[:, 0]
    vgrid_lat = vgcoors[:, 1]
    grid_z0 = griddata(coors, values, (vgrid_lon, vgrid_lat), method='linear')
    # ------------------------------------------------------------------------
    grid_output = np.ones([len(y), len(x)]) * np.nan
    for idx, coor in enumerate(vgcoors):
        lon = coor[0]
        lat = coor[1]
        xidx = np.where(x == lon)[0][0]
        yidx = np.where(y == lat)[0][0]
        grid_output[yidx, xidx] = grid_z0[idx]
    return grid_output, x, y
    
def grid2fig(grid, lons, lats, clabel = "formaldehyde (mol m-2)", savefile = "columns.jpg"):
    plt.figure()
    plt.pcolor(lons, lats, grid, cmap='jet')
    # plt.contourf(grid_lon,grid_lat,grid_z0,0, cmap = "jet")
    cmin = np.min(grid[np.where(np.isfinite(grid) == True)])
    cmax = np.max(grid[np.where(np.isfinite(grid) == True)])
    cbar = plt.colorbar()
    cbar.set_label(clabel)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.clim(cmin, (cmin + cmax)/2) 
    # plt.show()
    plt.savefig(savefile, format = "jpg")

# # example of drawing hcho
# filename = r"C:\workspace\cho\playground\data\S5P_OFFL_L2__HCHO___20190130T055906_20190130T074036_06723_01_010105_20190205T075428.nc"
# filename = r"C:\workspace\cho\playground\data\S5P_OFFL_L2__HCHO___20190129T061803_20190129T075934_06709_01_010105_20190204T082717.nc"
# coors, values = load_hcho_level2(filename)
# grid, lons, lats = point2grid(coors, values, r = 1)
# grid2fig(grid, lons, lats, clabel = "formaldehyde (mol m-2)")

# # example of drawing chocho
# filename = r"C:\workspace\cho\cho\data\S5P_OFFL_L1B_RA_BD4_20190101T031859_20190101T050029_06310_01_010000_20190101T064421_chocho.pkl"
# coors, values = load_chocho(filename)
# grid, lons, lats = point2grid(coors, values, r = 1)
# grid2fig(grid, lons, lats, clabel = "glyoxal (mol m-2)", savefile = "data/glyoxal.jpg")