import numpy as np
import pytest

from orographic_precipitation import compute_orographic_precip
from orographic_precipitation.fastscape_ext import OrographicDrainageDischarge
from orographic_precipitation.tests.fixture_orographic_precipitation import input_params

def test_orographic_drainage_discharge(input_params):

    grid = (3, 4)
    cell_area = 50
    stack =
    nb_receivers =
    receivers = 
    weights = 
    elevation = np.random.uniform(size=grid)
    dx = dy = 0.1
    
    precip_rate = compute_orographic_precip(elevation, dx, dy, **input_params)
    expected = precip_rate * 8.76e-6

    p = OrographicDrainageDischarge(
        runoff=precip_rate,
        shape=grid
    )

    p.run_step()

    np.testing.assert_equal(p.flowacc, expected)