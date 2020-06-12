"""
This module contains functions related to reading/writing Radiance-related files.
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
# Pyrano imports
from pyrano.pointcloud import sph2cart
# Geomeppy imports
from geomeppy.view_geometry import _get_collection, _get_collections, _get_limits
from io import StringIO
from eppy.iddcurrent import iddcurrent
from geomeppy import IDF
from geomeppy.geom.polygons import Polygon3D


def plot_sky_segments(sky_segments, dir_arrows=True, return_ax=False,
                      c_values=None, c_v_lims=None, cmap=None, r=1, alpha=0.2):
    '''Plots the sky-segments in 3D from a Pandas DataFrame made with
    divide_sky function. If return_ax is true then instead of plotting the
    function returns a matplotlib.axes object so further plots can be added to
    it. If dir_arrows is True, arrows for the 4 cardinal directions are added
    to the plot. North arrow is red, east arrow is yellow. c_values = iterable
    to color the sky segments (e.g. with DC values) if = None, the plot uses a
    default color; c_v_lims = tuple or list of 2 values for min and max range
    of coloring with c_values; cmap = matplotlib.cm colormapobject to use for
    coloring the sky segments; r = radius of the 3D sky segment plot; alpha =
    transparency of the colors in the plot.'''
    fig = plt.figure(figsize=(6,6))
    ax = Axes3D(fig, proj_type='persp')
    axlim = r/2 + 0.1*r
    ax.set_xlim(-axlim, axlim)
    ax.set_ylim(-axlim, axlim)
    ax.set_zlim(-axlim, axlim)
    # adding polygons of each sky segment to the plot: the vertices
    # (looking from the inside) start from bottom left and go counter clockwise
    if c_values is not None:
        norm = matplotlib.colors.Normalize(c_v_lims[0], c_v_lims[1])
        colors = [cmap(norm(c_value)) for c_value in c_values]
    else:
        colors = ['orange'] + ['deepskyblue'] * (len(sky_segments) - 1)
    sky_segments['colors'] = colors
    for ss in sky_segments.index[1:-1]:
        elevations = [sky_segments.loc[ss, 'elev_low_lims']]*2
        elevations += [sky_segments.loc[ss, 'elev_high_lims']]*2
        azimuths = [sky_segments.loc[ss, 'azim_left_lims']]
        azimuths += [sky_segments.loc[ss, 'azim_right_lims']]*2
        azimuths += [sky_segments.loc[ss, 'azim_left_lims']]
        ss_coords = sph2cart(az_deg=azimuths, el_deg=elevations, r=r)
        verts = [list(zip(ss_coords['x'], ss_coords['y'], ss_coords['z']))]
        coll3d = Poly3DCollection(verts, alpha=alpha,
                         facecolor=sky_segments.loc[ss, 'colors'],
                         edgecolor='k')
        ax.add_collection3d(coll3d)
        # TODO: implement plotting top sky segment later
    # top sky segment:
    top_segments = sky_segments[sky_segments['elev_high_lims'] ==
                   sky_segments.loc[sky_segments.index[-1], 'elev_low_lims']]
    elevations = top_segments['elev_high_lims']
    azimuths = sky_segments['azim_left_lims']
    ss_coords = sph2cart(az_deg=azimuths, el_deg=elevations, r=r)
    verts = [list(zip(ss_coords['x'], ss_coords['y'], ss_coords['z']))]
    coll3d = Poly3DCollection(verts, alpha=alpha,
                facecolor=sky_segments.loc[sky_segments.index[-1], 'colors'],
                edgecolor='k')
    ax.add_collection3d(coll3d)
    if dir_arrows:
        # add North-South arrows
        arrow_azverts = {'n':[345, 15, 0], 's':[165, 195, 180],
                         'w':[255, 285, 270], 'e':[75, 105, 90]}
        arrow_colors = {'n':'r', 's':'b', 'w':'g', 'e':'yellow'}
        for cd in arrow_azverts.keys():
            arrow = sph2cart(az_deg=arrow_azverts[cd], el_deg=[0, 0, 0],
                             r=[1.125*r, 1.125*r, 1.25*r])
            verts = [list(zip(arrow['x'], arrow['y'], arrow['z']))]
            ax.add_collection3d(Poly3DCollection(verts, alpha=0.5,
                                facecolor=arrow_colors[cd], edgecolor='k'))
    if return_ax:
        return ax
    else:
        plt.show(block=False)


def read_rad_dc_file(rad_dc_file):
    '''Returns a Pandas DataFrame from the Radiance-made mtx file'''
    # TODO: Make it more robust. Shouldn't rely on line count [11]
    f = open(rad_dc_file, 'r')
    dclines = [dcline.strip().split('\t') for dcline in f.readlines()[11:]]
    f.close()
    rad_dc_rgb = pd.DataFrame(data=dclines).transpose().astype(float)
    rad_dc = pd.DataFrame()
    for c in rad_dc_rgb.columns:
        rad_dc[c] = [np.mean((rad_dc_rgb.loc[i, c], rad_dc_rgb.loc[i+1, c],
        rad_dc_rgb.loc[i+2, c])) for i in range(0, len(rad_dc_rgb), 3)]
    return rad_dc


def read_smx_file(smx_file, index=None):
    '''Returns a Pandas DataFrame from the .smx file'''
    # this is very slow for now
    f = open(smx_file, 'r')
    flines = f.readlines()
    for l in flines:
        if l.startswith('NROWS'):
            nskypatch = int(l.split('=')[1])
        if l.startswith('NCOLS'):
            ntimestep = int(l.split('=')[1])
            break
    f.close()
    flines = flines[8:] # TODO: make this more robust later
    smx_df = pd.DataFrame()
    ss = 0
    ill_avgs = []
    for l in flines:
        if l == '\n':
            smx_df[ss] = ill_avgs
            ill_avgs = []
            ss += 1
        else:
            lums = l.strip().split()
            ill_avgs.append(np.mean(np.array(lums, dtype=float)))
        if ss > nskypatch:
            break
    if index is not None:
        smx_df.index = index
    return smx_df


def read_ill_file(ill_file, index=None, colnames=None, skiprows=15):
    '''Returns a Pandas DataFrame from the .ill file (the output file of a
    Radiance simulation). index: to replace the index column (e.g. with the
    timestamps of teh weather file used for the simulation). colnames: to
    replace the column names in the returned DataFrame. skiprows: number of
    rows to skip at the beginning of the ill file. The default 15 should work
    as of the current version of Radiance'''
    f = open(ill_file, 'r')
    nrows, ncols = None, None
    rl = 0
    while nrows == None or ncols == None:
        l = f.readline()
        rl += 1
        if l.startswith('NROWS'):
            nrows = int(l.split('=')[1])
        if l.startswith('NCOLS'):
            ncols = int(l.split('=')[1])
    ills_df = pd.read_csv(f, sep='\t', skiprows=skiprows-rl, header=None)
    f.close()
    del ills_df[ills_df.columns[-1]]
    # doublecheck if all rows and cols are read
    if (nrows, ncols) != ills_df.shape:
        raise ValueError('Mismatch between nrows or ncols in the ill file and '
                         'the returned DataFrame: '
                         'Check skiprows parameter and change if necessary.')
    # replacing index and column names if they are provided
    if index is not None:
        ills_df.index = index
    if colnames is not None:
        ills_df.columns = colnames
    return ills_df


def view_idf_to_ax(fname=None):
    """This is originally from https://github.com/jamiebull1/geomeppy/blob/master/geomeppy/view_geometry.py
    This just returns an ax instead of viewing it on order to  plot it together with the sensorpoints"""
    # set the IDD for the version of EnergyPlus
    iddfhandle = StringIO(iddcurrent.iddtxt)
    if IDF.getiddname() is None:
        IDF.setiddname(iddfhandle)
    # import the IDF
    idf = IDF(fname)
    # create the figure and add the surfaces
    ax = plt.axes(projection="3d")
    collections = _get_collections(idf, opacity=0.5)
    for c in collections:
        ax.add_collection3d(c)
    # calculate and set the axis limits
    limits = _get_limits(idf=idf)
    ax.set_xlim(limits["x"])
    ax.set_ylim(limits["y"])
    ax.set_zlim(limits["z"])
    return ax


def view_idf_and_ill(idf_name, sps, ill, return_ax=False, vmin=0, vmax=1000):
    """To view the e+ IDF and the sensorpoints together. Ill should be a
    pd.series with time in index"""
    surfcoords = []
    polys = []
    for surf in sps:
        polys.append(Polygon3D(surf['surf_coords']))
        for sp in surf['sensor_points']:
            surfcoords.append((sp[0], sp[1], sp[2]))
    xs = [c[0] for c in surfcoords]
    ys = [c[1] for c in surfcoords]
    zs = [c[2] for c in surfcoords]
    ax = view_idf_to_ax(fname=idf_name)
    ax.scatter(xs, ys, zs, marker='o', s=2, c=ill, cmap='nipy_spectral',
               vmin=vmin, vmax=vmax)
    if return_ax:
        return ax
    else:
        plt.show(block=False)
