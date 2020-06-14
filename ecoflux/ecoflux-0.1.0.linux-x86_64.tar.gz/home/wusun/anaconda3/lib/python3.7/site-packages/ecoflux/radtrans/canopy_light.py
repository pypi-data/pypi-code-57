"""Canopy radiative transfer."""
import numpy as _np


def extinc_coef(theta, chi):
    """
    Calculate the extinction coefficient of the plant canopy.

    Parameters
    ----------
    theta : float or array_like
        Solar zenith angle in radians. Must be within [0, pi / 2).
    chi : float or array_like
        Leaf shape parameter for light extinction.

    Returns
    -------
    float or array_like
        The light extinction coefficient of the canopy [m^2 m^-2].

    """
    return _np.sqrt(chi * chi + _np.tan(theta) ** 2) / (
        chi + 1.774 * (chi + 1.182) ** (-0.733)
    )
