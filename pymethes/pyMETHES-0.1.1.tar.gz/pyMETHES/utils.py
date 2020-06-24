#  Copyright (c) 2020 ETH Zurich

"""
Module with some utility methods.
"""

import numpy as np
import scipy.constants as sc
from typing import Union

num = Union[int, float, np.ndarray]


def velocity_from_energy(energy: num) -> num:
    """
    Calculate the velocity norm of electrons, based on their kinetic energy.

    Args:
        energy: Energy of the electron (eV)

    Returns: Velocity norm of the electrons (m.s-1)
    """

    return np.sqrt(2 * energy * sc.elementary_charge / sc.electron_mass)


def energy_from_velocity(velocity: num) -> num:
    """
    Calculate the kinetic energy of electrons, based on the norm of their velocity.

    Args:
        velocity: velocity norm of the electrons (m.s-1)

    Returns: Energy of the electrons (eV)
    """

    return 0.5 * sc.electron_mass * velocity ** 2 / sc.elementary_charge


def acceleration_from_electric_field(electric_field: num) -> num:
    """
    Calculates the acceleration of electrons, based on the local electric field.

    Args:
        electric_field: local electric field strength (V.m-1)

    Returns: acceleration (m.s-2)
    """

    return electric_field * (sc.elementary_charge / sc.electron_mass)
