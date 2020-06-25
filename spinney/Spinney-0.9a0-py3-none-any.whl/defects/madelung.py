#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementations of Ewald Summation techniques

See for example:

A. Y. Toukmaji and J. A. Board, Computer Physics Communications 95, 73 (1996)
"""
import numpy as np
from scipy import special
from spinney.constants import (conversion_table, available_units,
                               UnitNotFoundError)
from spinney.tools.formulas import get_formula_unit, get_number_fu
from spinney import containers

def find_lattice_cutoff(cell, cutoff):
    """ Finds the lattice points within a given cutoff
    Parameters
    ----------
    cell : 3x3 np.ndarray
       the cartesian components of the cell parameters; each ROW represents
       a parameter

    cutoff : float
       the cutoff radius

    Returns
    -------
    lattice_points : np.ndarray
        each ROW is the coordinate of a lattice point within the cutoff
    """
    cell_norms = np.linalg.norm(cell, axis=1)
    # maximum lattice points within the cutoff in all directions
    a,b,c = np.floor(cutoff/cell_norms)
    a = int(a)
    b = int(b)
    c = int(c)
    points_a, points_b, points_c = np.meshgrid(np.arange(-a,a),
                                               np.arange(-b,b),
                                               np.arange(-c,c))
    lattice_points = np.vstack((points_a.ravel(),
                               points_b.ravel(),
                               points_c.ravel())).T
    norms = np.dot(lattice_points, cell)
    norms = np.linalg.norm(norms, axis=1)
    valid_points = np.where(norms < cutoff)
    return lattice_points[valid_points]

def calculate_madelung_constant(U_coulomb, structure, Z):
    """ Calculates the Madelung's constant of a biatomic system,
    :data:`structure`, given the calculated ionic Coulomb
    energy, :data:`U_coulomb`.

    Internally, Hartree atomic units are used.

    Parameters
    ----------
    U_coulomb : float
        Coulomb energy in eV

    structure : ase.Atoms-like object
        Unit of length has to be Angstrom

    Z : float
        the absolute value of the ion formal charge HIGHEST COMMON FACTOR

    Returns
    -------
    M : float
        the Madelung's constant
        M = -r_nn/(Z^2)*U_coulomb
    """
    U = U_coulomb
    # Madelung's constant is defined for unit formula
    fu = get_formula_unit(structure.get_chemical_formula())
    no_fu = get_number_fu(structure.get_chemical_formula(), fu)
    U /= no_fu
    U *= conversion_table['eV']['Hartree']
    r_nn = structure.get_all_distances(mic=True)[0]
    r_nn = np.min(r_nn[r_nn > 1e-6]) # NN distance
    r_nn *= conversion_table['Angstrom']['Bohr']
    return np.abs(U*r_nn/Z**2)

def get_monopole_correction(cell, charge, dielectric_constant,
                            length_units='Angstrom', energy_units='eV'):
    """ Return the energy of a point charge in a periodic array of itself
    and a neutralizing background.

    Parameters
    ----------
    cell : 2D array
        each row of the matrix represents the cartesian coordinates
        of one of the cell's primitive vectors

    charge : float
        formal charge of the point charge

    dielectric_constant : float
        the medium dielectric constant

    length_units : string
        the units used to specify :data:`cell`

    energy_units : string
        the units of energy in which the energy
        will be given as output
    """
    ew = Ewald(cell, [0,0,0], charge, dielectric_constant, 10, 1, None,
               length_units, energy_units)
    V = ew.get_ewald_potential([0,0,0])
    # this is the correction: sign is flipped
    return -charge*V/2

class Ewald:
    """ Implement the calculation of various quantities related to the
    Ewald summation.

    Whatever the input units, internally Hartree atomic units are used.
    The results are then converted back to the input units.

    Parameters
    ----------
    cell : 2D array
        each row represents the cartesian coordinates of a cell parameter

    positions : 2D array
        each row represents the fractional coordinate of an atom in
        :data:`cell`

    formal_charges : array
        for each atom of structure specifies a formal charge

    dielectric_constant : float or 2D array
        the host material dielectric constant or tensor

    direct_cutoff : float
        cutoff in real space in units of :data:`length_units`
        Cells with distance larger than :data:`direct_cutoff`
        will not be included in the summation

    reciprocal_cutoff : float
        cutoff in reciprocal space in units of :data:`length_units`^-1

    alpha : float
        the Ewald convergence parameter

    length_units : string
        the units used to specify :data:`cell` and the cutoffs

    energy_units : string
        the units of energy in which the potentials and potential energies
        will be given as output

    tol : float
        convergence tolerance for the various summations

    min_steps : int > 1
        minimum amount of steps in the cutoff optimization cycle

    Attributes
    ----------
    direct_cutoff : float
        cutoff used for the direct part of the sum. Units
        of :data:`length_units`

    reciprocal_cutoff : float
        cutoff used for the reciprocal part of the sum. Units of reciprocal
        :data:`length_units`

    Methods
    -------
    get_ewald_potential(r)
        calculate the Ewald potential at point :data:`r`

    get_madelung_energy()
        calculate the electrostatic energy of the periodic array of point
        charges

    get_ewald_potential_grid(xx, yy, zz)
        calculate the Ewald potential on a 3D grid defined by :data:`xx yy zz`

    """
    def __init__(self, cell, positions, formal_charges, dielectric_constant,
                 direct_cutoff=10, reciprocal_cutoff=2, alpha=None,
                 length_units='Angstrom', energy_units='eV', tol=1e-6,
                 min_steps=2):
        if not (length_units in available_units):
            raise UnitNotFoundError('{} is not a valid unit'.
                                    format(length_units))
        else:
            self._length_units = length_units
            self._conv_l = conversion_table[self._length_units]['Bohr']
        if not (energy_units in available_units):
            raise UnitNotFoundError('{} is not a valid unit'.
                                    format(energy_units))
        else:
            self._energy_units = energy_units
            self._conv_e = conversion_table[self._energy_units]['Hartree']
        if not (type(cell) is np.ndarray):
            cell = np.array(cell)
        if not (type(positions) is np.ndarray):
            positions = np.array(positions)
        if positions.ndim < 2:
            positions = np.array([positions])
        if not (type(formal_charges) in containers):
            self._charges = np.array([formal_charges])
        else:
            self._charges = np.array(formal_charges)
        if len(positions) != len(self._charges):
            raise ValueError('Found {} charges for {} atoms'
                             .format(len(formal_charges), len(positions)))

        self._cell = cell*self._conv_l
        self._volume = abs(np.linalg.det(self._cell))
        # one row, one vector
        self._reciprocal_cell = np.linalg.pinv(self._cell).T
        self._positions = positions

        self._dielectric_constant = dielectric_constant

        if not (type(self._dielectric_constant) in containers):
            self._dielectric_constant = np.eye(3)*self._dielectric_constant
        # coordinate system transformation for anisotropic systems
        # see G. Fischerauer, IEEE Trans. Ultrason. Ferroelect. Freq. Contr.
        # 44, 1179 (1997)
        er1, C = np.linalg.eig(self._dielectric_constant)
        er1 = np.diag(er1)
        D = np.sqrt(er1)
        self._anisoT = np.dot(np.linalg.inv(D), C.T)
        self._transformed_cell = np.dot(self._cell, self._anisoT.T)
        self._transformed_volume = abs(np.linalg.det(self._transformed_cell))
        rcell_tra = np.linalg.pinv(self._transformed_cell).T
        self._transformed_reciprocal_cell = rcell_tra

        self._direct_cutoff = direct_cutoff*self._conv_l
        self._reciprocal_cutoff = reciprocal_cutoff/self._conv_l

        if not alpha:
            # default value Nijbeor et al. Physica 23, 309 (1957)
            # squared to be consistent with the employed notation
            self._alpha = np.pi/np.power(self._volume,2/3)
        else:
            self._alpha = alpha
        self._tol = tol
        if min_steps < 2:
            self._min_steps = 2
        else:
            self._min_steps = int(min_steps)

        # typical distance of the cell
        self._L = self._volume**(1/3)
        self._Lr = (1/self._volume)**(1/3)

        scaling = self._reciprocal_cutoff//self._Lr - 1
        self._direct_cutoff += self._L*5
        self._reciprocal_cutoff -= scaling*self._Lr

    @property
    def direct_cutoff(self):
        return self._final_direct_cutoff/self._conv_l

    @property
    def reciprocal_cutoff(self):
        return self._final_reciprocal_cutoff*self._conv_l

    def _calculate_direct_ewald_potential(self, r):
        """
        r : 1D array
            the fractional coordinates wrt *cell* where the potential has
            to be calculated
        """
        cell = self._transformed_cell
        lattice_point = False
        # if r corresponds to one of the atoms of the system
        if (np.abs(self._positions - r) < 1e-12).all(axis=1).any():
            lattice_point = True
            condition = (np.abs(self._positions - r) < 1e-12).all(axis=1)
            point_index = np.where(condition)[0][0]
        direct_cutoff = self._direct_cutoff
        converged = False
        values = []
        positions = np.dot(self._positions, cell)
        r = np.dot(r, cell)

        while not converged:
            direct_points = find_lattice_cutoff(self._cell, direct_cutoff)
            if lattice_point:
                # skip cell 0,0,0
                condition = (np.abs(direct_points) > 1e-12).any(axis=1)
                direct_points = direct_points[condition]
                # calculate term for points in cell 0,0,0
                incell_points = positions - r
                if len(incell_points) == 1: # monoatomic system
                    incell_term = 0
                else:
                    condition = (np.abs(incell_points) > 1e-12).any(axis=1)
                    incell_points = incell_points[condition]
                    incell_points = np.linalg.norm(incell_points, axis=1)
                    incell_term = special.erfc(np.sqrt(self._alpha)*incell_points)
                    incell_term /= incell_points
                    mask = np.arange(len(self._charges)) != point_index
                    incell_term *= self._charges[mask]
                    incell_term = incell_term.sum()
            direct_points = np.dot(direct_points, cell)
            arg = positions[:, np.newaxis, :] + direct_points - r
            arg = np.linalg.norm(arg, axis=2)
            term = special.erfc(np.sqrt(self._alpha)*arg)/arg
            term = term.sum(axis=1)
            term *= self._charges
            V_r = term.sum()
            if lattice_point:
                V_r += incell_term
            if np.abs(V_r) < 1e-15:
                values.append(0) # otherwíse there may be convergence issues
            else:
                values.append(V_r)
            if len(values) >= self._min_steps:
                if np.abs(values[-1] - values[-2]) < 1e-15:
                    converged = True
                elif np.abs((values[-1] - values[-2])/values[-1]) < self._tol:
                    converged = True
                else:
                    direct_cutoff += self._L
            else:
                direct_cutoff += self._L

        self._final_direct_cutoff = direct_cutoff
        if lattice_point:
            pref = -self._charges[point_index]*2*np.sqrt(self._alpha/np.pi)
            return values[-1] + pref
        else:
            return values[-1]

    def _calculate_reciprocal_ewald_potential(self, r):
        cell = self._transformed_cell
        volume = self._transformed_volume
        reciprocal_cell = self._transformed_reciprocal_cell

        reciprocal_cutoff = self._reciprocal_cutoff
        converged = False
        values = []
        positions = np.dot(self._positions, cell)
        r = np.dot(r, cell)

        twopi = 2*np.pi*np.complex(0,1)

        while not converged:
            reciprocal_points = find_lattice_cutoff(self._reciprocal_cell,
                                                    reciprocal_cutoff)
            mask = (reciprocal_points != [0, 0, 0]).any(axis=1)
            reciprocal_points = reciprocal_points[mask]
            reciprocal_points = np.dot(reciprocal_points,
                                       reciprocal_cell)
            arg = np.dot(reciprocal_points, positions.T)
            str_factor = np.exp(twopi*(-arg))*self._charges
            str_factor = str_factor.sum(axis=1)
            m2 = np.linalg.norm(reciprocal_points, axis=1)**2
            arg2 = np.pi**2*m2/self._alpha
            term = np.exp(-arg2)*np.exp(twopi*np.dot(reciprocal_points, r))/m2
            V_m = (term*str_factor).sum()
            if np.abs(V_m) < 1e-15:
                values.append(0)
            else:
                values.append(V_m)
            if len(values) >= self._min_steps:
                if np.abs(values[-1]) < 1e-15:
                    converged = True
                elif np.abs((values[-1] - values[-2])/values[-1]) < self._tol:
                    converged = True
                else:
                    reciprocal_cutoff += self._Lr
            else:
                reciprocal_cutoff += self._Lr
        if np.abs(np.imag(values[-1])) > 1e-12:
            raise RuntimeError('The imaginary part of the '
                               'potential is not zero! '
                               'Value = {} Hartree'.format(np.imag(values[-1]))
                              )

        self._final_reciprocal_cutoff = reciprocal_cutoff
        V = np.real(values[-1])/volume/np.pi
        g_o_term = -self._charges.sum()*np.pi/self._alpha/volume
        return V + g_o_term

    def get_ewald_potential(self, r):
        """ Get the Ewald potential due to a periodic lattice of charges
        at a given point r.

        Parameters
        ----------
        r : 1D array
            the fractional coordinates wrt to *self._cell* of the point of
            interest

        Notes
        -----
        NOTE: if *r* equals the position of one of the cell atoms,
              then what will be returned is the Wigner potential
        """
        # r within the 0,0,0 cell
        r = np.array(r).copy()%1
        V_r = self._calculate_direct_ewald_potential(r)
        V_m = self._calculate_reciprocal_ewald_potential(r)
        er = self._dielectric_constant
        er = np.sqrt(np.linalg.det(er))
        V = (V_r + V_m)/er
        return V/self._conv_e

    def get_madelung_energy(self):
        """ Calculates the Madelung energy (electrostatic energy of the
        crystal seen as a set of point charges) of the crystal.
        """
        U = []
        for pos in self._positions:
            U.append(self.get_ewald_potential(pos))
        return (np.array(U)*self._charges).sum()/2
