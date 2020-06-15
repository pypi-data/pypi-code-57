""" Unit tests for the the 'sound.pe.propagator' module in the 'kadlu' package

    Authors: Oliver Kirsebom
    contact: oliver.kirsebom@dal.ca
    Organization: MERIDIAN-Intitute for Big Data Analytics
    Team: Acoustic data Analytics, Dalhousie University
    Project: packages/kadlu
             Project goal: Tools for underwater soundscape modeling
     
    License:

"""
import pytest
from datetime import datetime
import os
import numpy as np
from kadlu.sound.pe.propagator import Propagator
from kadlu.sound.sound_propagation import Seafloor
from kadlu.sound.pe.grid import Grid
from kadlu.geospatial.ocean import Ocean


# dummy bounds, needed to initialize Ocean
bounds = dict(
        start=datetime(2015, 1, 9), end=datetime(2015, 1, 9, 3),
        south=44,                   west=-64.5, 
        north=46,                   east=-62.5, 
        top=0,                      bottom=5000
    )


def test_can_initialize_propapagator(grid):
    o = Ocean(**bounds)
    s = Seafloor()
    s.frequency=10
    s.c0 = 1500
    k0 = 2 * np.pi * 10 / 1500
    p = Propagator(ocean=o, seafloor=s, c=1480, c0=1500, grid=grid, k0=k0,\
                smooth_len_den=1500/10/4, smooth_len_c=0.001,\
                absorption_layer=0.2, ignore_bathy_gradient=False,\
                bathy_step=1, c_step=1)

    U = p._free_propagation_matrix()


def test_test():
    grid = Grid(dr=50, rmax=200, dq=180*np.pi/180., qmax=2*np.pi, dz=50, zmax=150)
    o = Ocean(**bounds, load_bathymetry=90)
    s = Seafloor()
    s.frequency=100
    s.c0 = 1500
    k0 = 2 * np.pi * s.frequency / 1500
    source_depth = 16.

    from kadlu.sound.sound_speed_old import SoundSpeed
    c = SoundSpeed(ssp=1480)

    p = Propagator(ocean=o, seafloor=s, c=c, c0=1500, grid=grid, k0=k0,\
                smooth_len_den=1500/s.frequency/4, smooth_len_c=0.0001,\
                absorption_layer=15/150., ignore_bathy_gradient=False,\
                bathy_step=1, c_step=1)

    from kadlu.sound.pe.starter import Starter

    st = Starter(grid=grid, k0=k0, method='THOMSON', aperture=86)
    psi = st.eval(zs=source_depth) * np.ones(shape=(1,1,grid.Nq))


    p.run(psi, receiver_depth=np.array([.1]), vertical_slice=True)