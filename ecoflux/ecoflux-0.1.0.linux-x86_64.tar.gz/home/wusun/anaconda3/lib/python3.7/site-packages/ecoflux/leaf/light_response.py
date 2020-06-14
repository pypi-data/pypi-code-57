"""Light response of leaf photosynthesis."""
from typing import Tuple

import numpy as _np


def michaelis_menten(p: Tuple[float, float, float], par: _np.ndarray):
    r"""
    Michaelis–Menten light response function.

    Parameters
    ----------
    p : tuple
        A tuple of three parameters

        * p[0]: *K*\ :sub:`PAR`, Michaelis constant
          [µmol photons m\ :sup:`–2` s\ :sup:`–1`];
        * p[1]: *P*\ :sub:`m`, maximum gross photosynthetic rate
          [µmol m\ :sup:`–2` s\ :sup:`–1`];
        * p[2]: *R*\ :sub:`d`, daytime respiration rate
          [µmol m\ :sup:`–2` s\ :sup:`–1`].

    par : array_like
        Photosynthetically active radiation
        [µmol photons m\ :sup:`–2` s\ :sup:`–1`].

    Returns
    -------
    array_like
        Photosynthetic assimilation rate [µmol m\ :sup:`–2` s\ :sup:`–1`].

    Examples
    --------
    >>> import numpy as np
    >>> michaelis_menten([500., 20., 2.], np.array([1500., 2000.]))
    array([13., 14.])

    """
    k_par, p_m, r_d = p
    return p_m * par / (k_par + par) - r_d


def residual_michaelis_menten(
    p: Tuple[float, float, float], par: _np.ndarray, A_n: _np.ndarray,
):
    r"""
    Residual function for Michaelis–Menten light response.

    Parameters
    ----------
    p : tuple
        A tuple of three parameters

        * p[0]: *K*\ :sub:`PAR`, Michaelis constant
          [µmol photons m\ :sup:`–2` s\ :sup:`–1`];
        * p[1]: *P*\ :sub:`m`, maximum gross photosynthetic rate
          [µmol m\ :sup:`–2` s\ :sup:`–1`];
        * p[2]: *R*\ :sub:`d`, daytime respiration rate
          [µmol m\ :sup:`–2` s\ :sup:`–1`].

    par : array_like
        Photosynthetically active radiation
        [µmol photons m\ :sup:`–2` s\ :sup:`–1`].
    A_n : array_like
        Measured photosynthetic assimilation rate
        [µmol m\ :sup:`–2` s\ :sup:`–1`].

    Returns
    -------
    array_like
        Residual of the photosynthetic assimilation rate
        [µmol m\ :sup:`–2` s\ :sup:`–1`].

    """
    k_par, p_m, r_d = p
    return p_m * par / (k_par + par) - r_d - A_n


def hyperbolic(p: Tuple[float, float, float, float], par: _np.ndarray):
    r"""
    Hyperbolic light response function.

    Parameters
    ----------
    p : tuple
        A tuple of four parameters

        * p[0]: *θ*, a curvature parameter;
        * p[1]: *α*, apparent quantum yield;
        * p[2]: *P*\ :sub:`m`, maximum gross photosynthetic rate
          [µmol m\ :sup:`–2` s\ :sup:`–1`];
        * p[3]: *R*\ :sub:`d`, daytime respiration rate
          [µmol m\ :sup:`–2` s\ :sup:`–1`].

    par : array_like
        Photosynthetically active radiation
        [µmol photons m\ :sup:`–2` s\ :sup:`–1`].

    Returns
    -------
    A_n : array_like
        Photosynthetic assimilation rate [µmol m\ :sup:`–2` s\ :sup:`–1`].

    Examples
    --------
    >>> import numpy as np
    >>> hyperbolic([0.7, 0.04, 20., 2.], np.array([1500., 2000.]))
    array([15.75986071, 16.35949823])

    References
    ----------
    * Ögren, E. and Evans, J. R. (1993). Photosynthetic light-response curves:
      I. The influence of CO2 partial pressure and leaf inversion. *Planta*,
      189, 182–190. https://doi.org/10.1007/BF00195075

    """
    theta, alpha, p_m, r_d = p
    if _np.isclose(theta, 0.0):
        A_n = alpha * p_m * par / (alpha * par + p_m) - r_d
    else:
        A_n = (
            alpha * par
            + p_m
            - _np.sqrt(
                (alpha * par + p_m) ** 2 - 4.0 * theta * alpha * par * p_m
            )
        ) * 0.5 / theta - r_d
    return A_n


def residual_hyperbolic(
    p: Tuple[float, float, float, float], par: _np.ndarray, A_n: _np.ndarray,
):
    r"""
    Residual function for the hyperbolic light response.

    Parameters
    ----------
    p : tuple
        A tuple of four parameters

        * p[0]: *θ*, a curvature parameter;
        * p[1]: *α*, apparent quantum yield;
        * p[2]: *P*\ :sub:`m`, maximum gross photosynthetic rate
          [µmol m\ :sup:`–2` s\ :sup:`–1`];
        * p[3]: *R*\ :sub:`d`, daytime respiration rate
          [µmol m\ :sup:`–2` s\ :sup:`–1`].

    par : array_like
        Photosynthetically active radiation
        [µmol photons m\ :sup:`–2` s\ :sup:`–1`].
    A_n : array_like
        Measured photosynthetic assimilation rate
        [µmol m\ :sup:`–2` s\ :sup:`–1`].

    Returns
    -------
    array_like
        Residual of the photosynthetic assimilation rate
        [µmol m\ :sup:`–2` s\ :sup:`–1`].

    """
    return hyperbolic(p, par) - A_n
