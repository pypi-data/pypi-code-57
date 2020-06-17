# SatMAD: Satellite Mission Analysis and Design for Python
#
# Copyright (C) 2020 Egemen Imre
#
# Licensed under GNU GPL v3.0. See LICENSE.rst for more info.
"""
Trajectory Class tests.
"""

import numpy as np
from astropy import units as u
from astropy.coordinates import CartesianDifferential, CartesianRepresentation, SkyCoord
from astropy.time import Time, TimeDelta

from satmad.coordinates.trajectory import Trajectory
from satmad.propagation.tle import TLE


def test_interpolation_err():
    # Init TLE
    line1 = "1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991"
    line2 = "2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482"

    tle = TLE.from_tle(line1, line2)

    # Init satellite object from the TLE
    sat = tle._satrec

    # ****** Generate the discrete time instants through the propagation duration ******
    init_time = Time(2458826, format="jd", scale="utc")
    duration = TimeDelta(3.0, format="jd")
    steps = 4000  # number of steps within the propagation duration
    dt = duration / steps

    # Generate time list
    dt_list = dt * np.arange(0, steps, 1)
    time_list = init_time + dt_list

    # SGP4 module requires time instances as jd and fraction arrays
    jd_list = time_list.jd1
    fr_list = time_list.jd2

    # ****** Generate the pos, vel vectors for each time instant ******

    # Run the propagation and init pos and vel vectors in TEME
    e, r_list, v_list = sat.sgp4_array(jd_list, fr_list)

    # Load the time, pos, vel info into astropy objects (shallow copied)
    vel_list = CartesianDifferential(v_list, unit=u.km / u.s, xyz_axis=1)
    pos_list = CartesianRepresentation(
        r_list, unit=u.km, xyz_axis=1
    ).with_differentials(vel_list)

    # trajectory in astropy
    traj_astropy = SkyCoord(
        pos_list,
        obstime=time_list,
        frame="teme",
        representation_type="cartesian",
        differential_type="cartesian",
    )

    # Init trajectory in Trajectory object
    trajectory = Trajectory(traj_astropy)

    # TODO burada kaldım - buraya kadarki kısım aslında fixture

    # ****** Fill interpolator with time and (x, y, z) axes ******
    spline_degree = 5  # degree of spline
    extrapolate_action = (
        "raise"  # raise Exception if an out of bounds point is requested
    )

    r_interpolator = CartInterpolator3D(
        fr_list,
        r_truth_list[:, 0],
        r_truth_list[:, 1],
        r_truth_list[:, 2],
        spline_degree=spline_degree,
        extrapolate_action=extrapolate_action,
    )
    # TODO üst kısım muhtemelen gereksiz

    # ******  Test interpolation accuracy ******
    step_offset = 0
    test_stepsize = 1.0 / 86400  # stepsize in days
    test_end = 0.01  # days

    print(f"Test duration: {test_end - step_offset * stepsize} days")
    print(f"Step size: {test_stepsize * 86400} sec")

    fr_test_list = np.arange(step_offset * stepsize, test_end, test_stepsize)
    jd_test_list = np.full(len(fr_test_list), jd_init)

    # Generate the high-res test trajectory
    e_test_list, r_test_list, v_test_list = sat.sgp4_array(jd_test_list, fr_test_list)
    r_err_list = np.array(r_interpolator(fr_test_list))
    r_err_list = r_err_list.transpose() - r_test_list
