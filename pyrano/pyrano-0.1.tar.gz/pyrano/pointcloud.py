"""
This module contains functions related to manipulating LiDAR point clouds
to use them for calculating shading for hourly annual solar irradiance
simulations.
Some of the functions are from the USM_LiDAR project:
https://gitlab.tue.nl/bp-tue/usm_lidar_dev
and the Daypym project:
https://gitlab.tue.nl/bp-tue/daypym
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from mpl_toolkits.axes_grid1 import make_axes_locatable
from PIL import Image
from geomeppy.geom.polygons import (Polygon2D, Vector2D)
from pyrano.geometry import point_in_poly
import rtree


def sph2cart(az_deg, el_deg, r):
    """Function to convert spherical coordinates to cartesian coordinates.
    It expects numpy arrays in degrees as input with the same length or length
    of 1"""
    # convert to radians
    az_rad = np.deg2rad(az_deg)
    el_rad = np.deg2rad(el_deg)
    # do the maths
    rcos_theta = r * np.cos(el_rad)
    x = rcos_theta * np.cos(az_rad)
    y = rcos_theta * np.sin(az_rad)
    z = r * np.sin(el_rad)
    # put the result into a DataFrame
    cart = pd.DataFrame({'x': x, 'y': y, 'z': z})
    return cart


def cart2sph(x, y, z):
    """Function to convert cartesian coordinates to spherical coordinates.
    It expects numpy arrays as input with the same length or length of 1"""
    # do the maths
    hxy = np.hypot(x, y)
    r = np.hypot(hxy, z)
    el_rad = np.arccos(z/r)
    az_rad = np.arctan2(y, x)
    # convert to degrees and rotate 90 degrees to have North be 0 degrees
    el_deg = 90 - np.rad2deg(el_rad)  # 90-x to get elevation instead of zenith
    az_deg = -np.rad2deg(az_rad) + 90
    # wrap around the parts above 360 due to rotate
    az_deg[az_deg < 0] = az_deg[az_deg < 0] + 360
    # put the result into a DataFrame
    sph = pd.DataFrame({'azimuth': az_deg, 'elevation': el_deg, 'r': r})
    return sph


def supress_points(xyz, vertices, zmax, apothem):
    """Limits an xyz point cloud's z coordinates to zmax within the boundaries
    of a polygon. xyz: a DataFrame with x-y-z columns made by teh tiff2xyz()
    function; vertices: vertices of the polygon; zmax: max height of points
    within the polygon; aphotem: aphotem used in the tiff2xyz function()."""
    vert_vects = [Vector2D(v[0]-apothem, v[1]-apothem) for v in vertices]
    poly = Polygon2D(vert_vects)
    x_min = min(poly.xs)
    x_max = max(poly.xs)
    y_min = min(poly.ys)
    y_max = max(poly.ys)
    # sorting from high z to low to speed things up
    for i in xyz.sort_values(by='z', ascending=False).index:
        if ((xyz.loc[i, 'x'] > x_min and xyz.loc[i, 'x'] < x_max) and
           (xyz.loc[i, 'y'] > y_min and xyz.loc[i, 'y'] < y_max)):
           point = Vector2D(xyz.loc[i, 'x'], xyz.loc[i, 'y'])
           if point_in_poly(point, poly):
               xyz.loc[i, 'z'] = zmax
        if xyz.loc[i, 'z'] < zmax:
            break
    return xyz


def shift_cart_coords(xyz, p_xyz_ref, p_xyz_to_shift):
    """Shifts xyz coordinates to a new reference. Inputs: xyz = the input xyz
    DataFrame to be shifted, p_xyz_ref = xyz coordinates dict of a reference
    point in the ref_xyz e.g. {'x':0, 'y':0, 'z':0}, p_xyz_shfted = xyz coords
    of the same reference point in the to be shifted xyz. It returns a new xyz
    that is shifted to the reference system."""
    p_delta = {'x':p_xyz_to_shift['x'] - p_xyz_ref['x'],
               'y':p_xyz_to_shift['y'] - p_xyz_ref['y'],
               'z':p_xyz_to_shift['z'] - p_xyz_ref['z']}
    for c in ['x', 'y', 'z']:
        xyz[c] -= p_delta[c]
    return xyz


def lidar_to_ep_coords(lidar_xyz, ref_point_ep, ref_point_lidar):
    '''Rerurns the xyz DataFrame of the LiDAR point cloud in the coordinate
    system of the energy plus model. lidar_xyz = xyz DataFrame of the LiDAR
    point cloud. ref_point_ep = list of x, y, z coordinates of a reference
    point in the EnergyPlus model, ref_point_lidar = list of x, y, z
    coordinates of the same reference point in the LiDAR point cloud.'''
    apothem = -lidar_xyz['y'].min()
    p_xyz_ref = {'x':ref_point_ep[0], 'y':ref_point_ep[1], 'z':ref_point_ep[2]}
    p_xyz_to_shift = {'x':ref_point_lidar[0], 'y':ref_point_lidar[1],
                      'z':ref_point_lidar[2]}
    xyz_ep = shift_cart_coords(lidar_xyz, p_xyz_ref, p_xyz_to_shift)
    xyz_ep['x'] += apothem
    xyz_ep['y'] += apothem
    return xyz_ep


def tiff2array(tiffloc):
    """function to read tiff file and put it into an array"""
    # set maximum number of pixels higher to prevent DOS errors
    Image.MAX_IMAGE_PIXELS = 125000000
    # open tiff file and convert it to an array
    array = np.array(Image.open(tiffloc))
    # get the maximum value of the whole array
    nanpoint = np.amax(array)
    # set the maximum value to be nan
    array[array == nanpoint] = np.nan
    # flip array around the x-axis
    array = np.flip(array, axis=0)
    return array


def lidarzoom(array, x, y, apothem=200, resolution=0.5):
    """function that 'zooms in' to a test point (x, y) of the LiDAR array
        and removes all unnecessary points outside of the apothem (square
        radius)
    array = the LiDAR array to 'zoom in' to
    x = x coordinate of the test point in the LiDAR array
    y = y coordinate of the test point in the LiDAR array
    apothem = apothem ('square radius') of LiDAR points that need to be kept
    resolution = resolution of the tiff file (0.5 for pdok.nl files)"""
    # multiply x, y and apothem by 1/resolution to get distance in meters
    x = int(x * (1/resolution))
    y = int(y * (1/resolution))
    apothem = int(apothem * (1/resolution))
    xrangeleft = x - apothem
    xrangeright = x + apothem
    yrangebottom = y - apothem
    yrangetop = y + apothem
    height, width = array.shape
    array = np.delete(array, np.r_[0:xrangeleft, xrangeright:width], axis=1)
    array = np.delete(array, np.r_[0:yrangebottom, yrangetop:height], axis=0)
    return array


def array2xyz_depr1(array, savename='pointcloud', save=False, resolution=0.5):
    """function to make the LiDAR array into an XYZ array and save an XYZ
    file"""
    # make array into xyz array
    height, width = array.shape
    ys, xs = np.mgrid[:height/2:resolution, :width/2:resolution]
    xyz = np.column_stack((xs.ravel() - round(width/2/(1/resolution)),
                           ys.ravel() - round(height/2/(1/resolution)),
                           array.ravel()))
    # remove rows with NaNs
    xyz = xyz[~np.isnan(xyz).any(axis=1)]
    # convert array to DataFrame for easier use
    xyz = pd.DataFrame({'x': xyz[:, 0], 'y': xyz[:, 1], 'z': xyz[:, 2]})
    # save the XYZ file
    if save:
        save_df(xyz, filename=savename, filetype='xyz', folder='Pointclouds',
                header=False, sep=' ')
    return xyz


def array2xyz(array, savename='pointcloud', save=False, resolution=0.5):
    """function to make the LiDAR array into an XYZ array and save an XYZ
    file"""
    # make array into xyz array
    height, width = array.shape
    ys, xs = np.mgrid[:height*resolution:resolution, :width*resolution:resolution]
    xyz = np.column_stack((xs.ravel() - round(width/2/(1/resolution)),
                           ys.ravel() - round(height/2/(1/resolution)),
                           array.ravel()))
    # remove rows with NaNs
    xyz = xyz[~np.isnan(xyz).any(axis=1)]
    # convert array to DataFrame for easier use
    xyz = pd.DataFrame({'x': xyz[:, 0], 'y': xyz[:, 1], 'z': xyz[:, 2]})
    # save the XYZ file
    if save:
        save_df(xyz, filename=savename, filetype='xyz', folder='Pointclouds',
                header=False, sep=' ')
    return xyz


def lidarplot(array, figure_name=None, resolution=0.5):
    """function to plot lidar maps based on the LiDAR array
    save = boolean whether to save the plot
    resolution = resolution of the tiff file (0.5 for pdok.nl files)"""
    # initialize figure
    fig, ax = plt.subplots()
    fig.tight_layout()
    fig.set_size_inches(5, 5)
    # set title and axes labels
    ax.set_title('DSM')
    ax.set_xlabel('X-axis [m]')
    ax.set_ylabel('Y-axis [m]')
    ax.minorticks_on()
    # get shape to put into imshow extent
    m, n = array.shape
    # create figure
    # extend is divided by 1/resolution to go to meters on the axes
    im = plt.imshow(array, cmap='plasma', origin='lower', interpolation='none',
                    extent=[0, n/(1/resolution), 0, m/(1/resolution)],
                    aspect='equal')
    # add color bar to figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size=0.2, pad=0.1)
    cbar = plt.colorbar(im, cax=cax, extend='both')
    cbar.minorticks_on()
    cbar.set_label(label='Height above Amsterdam Ordnance Datum [m]')
    plt.show(block=False)
    if figure_name is not None:
        plt.save_figure(fig, figure_name, filetype='png')


def tiff2xyz(tiffloc, x=None, y=None, apothem=200, save_xyz_filename=None,
             plot_tiff=False, plot_croppedtiff=False, resolution=0.5):
    """Function to go from the tiff file, with an x and y in that file around
    the testpoint to an xyz-file with the ability to plot it and return the
    x, y, z array
    tiffloc = relative or full file location of the tiff file (e.g. downloaded
        from pdok.nl)
    x = x coordinate of the test point in the full tiff file
    y = y coordinate of the test point in the full tiff file
    apothem = 'square radius' you want to take into account in the cropped
        tiff version
    savexyz = boolean whether to save the .xyz-file
    plot_tiff = boolean whether to plot the full tiff file
    plot_croppedtiff = boolean whether to plot the cropped tiff version
    resolution = resolution of the tiff file (0.5 for pdok.nl files)."""
    # load tiff file in an array
    array = tiff2array(tiffloc)
    # plot full tiff file
    if plot_tiff:
        lidarplot(array, figure_name=None, resolution=resolution)
    # crop array around x, y with a radius
    if x and y and apothem is not None:
        array = lidarzoom(array, x, y, apothem, resolution=resolution)
    # plot cropped array
    if plot_croppedtiff:
        lidarplot(array, figure_name=None, resolution=resolution)
    # convert array to x, y and z DataFrame
    xyz = array2xyz(array, savename=None, save=False, resolution=resolution)
    if save_xyz_filename is not None:
        xyz.to_csv(save_xyz_filename, sep=' ', header=False, index=False)
    return xyz


def dist2D(p, q):
    """Return the Euclidean distance between 2D points p and q."""
    return np.hypot(p[0] - q[0], p[1] - q[1])


def remove_neighbors(points, tol):
    """Function to remove nearest neighbors of 2D points collection DataFrame
        within tolerance and returns 'culled' DataFrame"""
    # create an empty list so we can fill it
    result = []
    # create the R-tree
    index = rtree.index.Index()
    # get the column names of the points DataFrame
    columns = points.columns.values.tolist()
    # put the points in a list
    points = points.values.tolist()
    # iterate over points and put points that comply with conditions in the
    # result list
    for i, p in enumerate(points):
        # get x and y value of the points
        x, y = p
        # get the proximity of the point to the others
        nearby = index.intersection((x - tol, y - tol, x + tol, y + tol))
        # keep the points that are above the tolerance in the proximity set
        if all(dist2D(p, points[j]) >= tol for j in nearby):
            # append the point to the result list
            result.append(p)
            # insert the point in the index
            index.insert(i, (x, y, x, y))
    # create a dataframe of the result list with the original column names
    result = pd.DataFrame(result, columns=columns)
    return result


def plotprojected(projected, save=False, radius=10):
    """Plot DataFrame with x, y and z column in 3D"""
    # set up plot
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_xlim3d(-radius, radius)
    ax.set_ylim3d(-radius, radius)
    # plot x, y and z of the DataFrame
    ax.scatter3D(projected['x'], projected['y'], projected['z'])
    # save figure
    if save:
        save_figure(fig, figurename='projected')


def cyl2cart(az_deg, z, rho):
    """function to convert cylindrical coordinates to cartesional coordinates.
    It expects numpy arrays as input with the same length or length of 1"""
    # convert to radians
    az_rad = np.deg2rad(az_deg)
    # do the maths
    x = rho * np.cos(az_rad)
    y = rho * np.sin(az_rad)
    # put the result into a DataFrame
    cart = pd.DataFrame({'x': x, 'y': y, 'z': z})
    return cart


def cart2cyl(x, y, z):
    """function to convert cartesian coordinates to cylindrical coordinates.
    It expects numpy arrays as input with the same lenght or lenght of 1"""
    # do the maths
    rho = np.hypot(x, y)
    az_rad = np.arctan2(x, y)
    # convert to degrees and rotate 90 degrees to have North be 90 degrees
    az_deg = -np.rad2deg(az_rad) + 90
    # wrap around the parts above 360 due to rotate
    az_deg[az_deg < 0] = az_deg[az_deg < 0] + 360
    # put the result into a DataFrame
    cyl = pd.DataFrame({'azimuth': az_deg, 'z': z, 'rho': rho})
    return cyl


def xyz_coords_from_sps(sps):
    """Takes sps dict as input. Extracts x, y, z coords from an sps dict made
    with the create_sensor_points() or the pointgrid_over_surface() function"""
    x, y, z = ([] for i in list(range(3)))
    for p in sps:
        x += [c[0] for c in p['sensor_points']]
        y += [c[1] for c in p['sensor_points']]
        z += [c[2] for c in p['sensor_points']]
    return pd.DataFrame(data={'x':x, 'y':y, 'z':z})


def xyz2proj(xyz, testpoint_height, cull_tol=1.5, plot_proj=False,
             save_projplot=False, save_proj=False, proj_name='proj', cyl=False,
             radius=1):
    """Function to go from an xyz pointcloud file around the testpoint,
    to a projected sphere in 3D with the ability to plot it and
    return the x, y, z DataFrame and the azimuth, z, rho DataFrame (in case of
    cyl = True) or the azimuth, elevation, radius DataFrame (in case of
    cyl = False).
    xyz = xyz-array (created with tiff2xyz function)
    testpoint_height = z-value of testpoint (above Amsterdam Ordnance Datum in
        case of tiff-file from pdok.nl
    cull_tol = tolerance which to use for the culling of points that are close
        to one another (in degrees of the azimuth-elevation domain)
    plot_proj = boolean whether to plot the projected points
    save_projplot = boolean whether to save the projected points plot
    save_proj = boolean whether to save the DataFrame of projected points
    proj_name = string with name to use for saving purposes
    cyl = boolean wheter to plot a cylindrical shape (True) or hemispherical
        (False)
    radius = radius of the cylinder / hemisphere."""
    # move LiDAR xyz down so origin = testpoint
    xyz['z'] = xyz['z'] - testpoint_height
    # remove LiDAR xyz points lower than the testpoint
    xyz = xyz[xyz['z'] > 0]
    # convert points to spherical coordinates
    sph = cart2sph(xyz['x'], xyz['y'], xyz['z'])
    # set the radius so the points are 'projected' onto a sphere
    sph['r'] = radius
    if cull_tol > 0:
        # remove points that are close to one another on the sky hemisphere
        sph = remove_neighbors(sph[['azimuth', 'elevation']], tol=cull_tol)
        # convert purged points back to cartesian coordinates
        sphxyz = sph2cart(sph['azimuth'], sph['elevation'], r=radius)
    # if you want to have the points on a cylinder:
    if cyl:
        # create z based on elevation
        z = np.tan(np.deg2rad(sph['elevation'])) * radius
        # convert cartesian to cyl coordinates with the new z
        cyl = cart2cyl(sphxyz['x'], sphxyz['y'], z)
        if plot_proj:
            # convert points back to cartesian coordinates while setting rho to
            # cyl_radius, so they're 'projected' on the cylinder
            cylxyz = cyl2cart(cyl['azimuth'], cyl['z'], rho=radius)
            # plot projected points in 3D
            plotprojected(cylxyz, save=save_projplot)
        # set the return variable
        proj = cyl
    else:
        if plot_proj:
            # plot projected points in 3D
            plotprojected(sphxyz, save=save_projplot)
        # set the return variable
        proj = sph
    if save_proj:
        save_df(proj, filename=proj_name, folder='Projection output')
    return proj
