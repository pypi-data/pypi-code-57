#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone implementation of the correction scheme for charged defects
proposed by Freysoldt, Neugebauer and Van de Walle.

    Phys. Rev. Lett. 102, 016402 (2009)

Internally, the code use atomic units of Hartree and Bohr, as implemented in
Freysoldt et al. papers.

The input values have to be inserted in units of eV and Angstrom and the
final values will also be converted to these units.
"""
import numpy as np
import scipy.integrate
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from spinney.constants import conversion_table

def plane_average_potential(locpot, axis):
    """
    Makes the plane-average of the electrostatic potential
    along the chosen axis.

    Parameters
    ----------
    locpot : 3D array
        the local electrostatic potential on a 3D mesh

    axis : int
        0 for a
        1 for b
        2 for c
        where a,b,c are the cell parameters along which the 3D grid is defined

    Returns
    -------
        1D numpy array : the plane-averaged potential along the chosen axis
    """
    # FFT grid points
    fft_grid = np.array(locpot.shape)
    av_potential_list = []
    for index in range(fft_grid[axis]):
        if axis == 0:
            av_potential = locpot[index].mean()
            av_potential_list.append(av_potential)
        elif axis == 1:
            av_potential = locpot[:, index].mean()
            av_potential_list.append(av_potential)
        elif axis == 2:
            av_potential = locpot[:, :, index].mean()
            av_potential_list.append(av_potential)
        else:
            raise ValueError('Index {} not valid!'.format(axis))

    return np.array(av_potential_list, dtype=np.float64)

class FChargeDistribution:
    r"""
    Gaussian + exponential tail radial charge distribution employed by
    Freysoldt et. al., Phys. Status Solidi B 248, 5 (2011)

    .. math::
        :nowrap:

        \begin{align*}
        q(r) &= q \left(x N_1 e^{-r/\gamma} + 
                (1-x) N_2 e^{-r^2/\beta^2} \right)\\
        N_1 &= \frac{1}{8 \pi \gamma^3}\\
        N_2 &= \frac{1}{(\sqrt \pi \beta)^3}
        \end{align*}


    ``x`` and ``gamma`` may be found from looking at the defect wave function.
    The value of ``beta`` is not so important as long as the defect remains
    localized.
    A Gaussian function usually performs well enough.

    Parameters
    ----------
    x : float

    gamma : float
        units of Angstrom

    beta : float
        units of Angstrom

    Notes
    -----
    For localized states, `x` = 0; for delocalized ones, usually
    `x` is around 0.54-0.6 in semiconductors.
    """
    def __init__(self, x=0, gamma=1, beta=1):
        self.x = x
        self.gamma = gamma
        self.beta = beta
        self.N1 = 1/(8*np.pi*self.gamma**3)
        self.N2 = 1/(np.sqrt(np.pi)*self.beta)**3

    def Direct(self):
        """ The normalized charge distribution in real space """
        x = self.x
        N1 = self.N1
        N2 = self.N2
        beta = self.beta
        gamma = self.gamma
        return lambda r: (x * N1 * np.exp(-np.sqrt((r*r))/gamma)
                          + (1-x) * N2 * np.exp(-(r*r)/(beta**2))
                         )

    def Fourier_transform(self):
        """ The Fourier trasform of :meth:`Direct` """
        x = self.x
        beta = self.beta
        gamma = self.gamma
        return lambda g: ((x * 1/((np.dot(g, g)*gamma**2 + 1)**2)
                           + (1-x) * np.exp(-0.25*np.dot(g, g)*beta**2))
                         )

    def Fourier_transform_gto0(self):
        r"""
        The second derivative of the charge distribution with respect to g.
        It approximates the distribution for :math:`g \rightarrow 0`:

        ``q(g-->0) ~ q.Fourier_transform(0) + 1/2 q.Fourier_transform_gto0()``

        The term  is used for getting the potential alignment :math:`V_0`
        of equation 17.
        """
        return (self.x - 1)*0.5*self.beta**2 - 4*self.x * self.gamma**2

    @classmethod
    def get_model_D(cls):
        """ Model function to be used for fitting """
        def model_f(r, x, gamma, beta):
            N1 = 1/(8*np.pi*gamma**3)
            N2 = 1/(np.sqrt(np.pi)*beta)**3
            return (x * N1 * np.exp(-np.sqrt((r*r))/gamma)
                    + (1-x) * N2 * np.exp(-(r*r)/(beta**2)))
        return model_f

class FCorrection:
    """ Implementation of Freysoldt et al. correction.

    Note:
        the code assumes that the units are Angstrom for lengths and
        eV for energies!

    Parameters
    ----------
    supercell : 2D array
        each rows represents the cartesian coordinates of the vectors
        describing the supercell

    q : int
        charge state of the defect

    pristine_pot : 3D numpy array
        this array must contain the total electrostatic potential calculated
        on 3D grid for the pristine system. The shape of the array is:
        (Na, Nb, Nc)

        where Nx is the number of grid points along the cell parameter x

    defective_pot : 3D numpy array
        as `pristine_pot` but for the defective system

    charge_distribution : :class:`FChargeDistribution` instance
        the model charge distribution used for the defect-induced charge
        density

    dielectric_constant : float
            dielectric constant of the bulk system

    def_position : array
            defect position in the defective supercell
            in fractional coordinates with respect to `supercell`

    axis_average : int
            axis which will be used to perform the plane-average of the
            electrostatic potential:

            - 0 for a
            - 1 for b
            - 2 for c

    cutoff : float
            cutoff for reciprocal space vectors, **IN** eV

    tolerance : float
        tolerance threshold used in calculating the energy terms

    shift_tol : float
            tolerance in findind the defect position on the 3D grid
    """
    def __init__(self, supercell, q, charge_distribution,
                 pristine_pot, defective_pot,
                 dielectric_constant, def_position, axis_average,
                 cutoff=500, tolerance=1e-6,
                 shift_tol=1e-5):
        self.cell = np.copy(supercell)
        self.volume = np.linalg.det(supercell)
        self.reciprocal_cell = np.linalg.pinv(supercell).T
        self.q = q
        self.qmodel = charge_distribution
        self.cutoff = cutoff*conversion_table['Hartree']['eV']
        self.max_g = np.sqrt(2*self.cutoff)
        self.tol = tolerance
        self.pristine_locpot = pristine_pot.copy()
        self.defective_locpot = defective_pot.copy()
        self.eps = dielectric_constant
        self.def_position = def_position
        self.axis = axis_average
        self.shift_tol = shift_tol

    def generate_reciprocal_space_grid(self, cutoff):
        """ Generates a regular mesh of reciprocal space points given a cutoff
        energy.

        Parameters
        ----------
        cutoff : float
            maximum kinetic energy, in Hartree, of the k-point

        Returns
        -------
        grid : list
            the reciprocal lattice vectors in Cartesian coordinates in
            units of Bohr
        """
        gmax = np.sqrt(2*cutoff)

        conv = conversion_table['Angstrom']['Bohr']
        rec_basis = 2*np.pi*self.reciprocal_cell/conv
        # find max components smaller/equal to gmax on a sphere
        m = 1
        while True:
            g = np.dot(np.array([0, 0, m]), rec_basis)
            if np.linalg.norm(g) > gmax:
                break
            m += 1
        grid = [np.dot(rec_basis, np.array([a, b, c]))
                for a in np.arange(-m, m)
                for b in np.arange(-m, m) for c in np.arange(-m, m)]
        self.grid = grid
        return grid

    def _get_E_lat1(self):
        r"""
        Gets the energy of the periodic array of defects in their own
        potential of :math:`E^{lat}`.
        I.e the first term  in eq (8) of PSS B 248, 5 (2011).
        """
        vol = self.volume*conversion_table['Angstrom']['Bohr']**3
        pref = 2*np.pi*self.q**2/(vol*self.eps)
        en_list = []
        # compute the correction energy
        # we start from a smaller cutoff and increase it until the energy
        # converges or we reach the maximum cutoff self.cutoff
        cutoff = 2
        converged = False
        while not converged:
            energy = 0
            grid = self.generate_reciprocal_space_grid(cutoff)
            for g in grid:
                if (g == np.zeros(3)).all():
                    # analytic term V0, eq. (17): potential alignment
                    energy += self.qmodel.Fourier_transform_gto0()
                else:
                    energy += (self.qmodel.Fourier_transform()(g)**2
                               /np.dot(g, g))
            en_list.append(energy)
            if len(en_list) >= 2:
                if np.abs(en_list[-1] - en_list[-2]) < self.tol:
                    converged = True
                elif cutoff > self.cutoff:
                    raise ValueError('The energy of the periodic array '
                                     'did not converged. Increase the cutoff')
            cutoff += 1

        return en_list[-1]*pref

    def _get_E_lat2(self):
        """ Gets the self interaction energy of the model charge.
        I.e the second term  in eq (8) of PSS B 248, 5 (2011)
        """
        pref = self.q**2/(self.eps*np.pi)
        en_list = []
        # compute the correction energy
        # we start from a smaller cutoff and increase it until the energy
        # converges or we reach the maximum cutoff self.cutoff
        cutoff = 2
        converged = False
        while not converged:
            energy = 0
            g_max = np.sqrt(2*cutoff)
            f = lambda g: self.qmodel.Fourier_transform()(g)**2
            energy = scipy.integrate.quad(f, 0, g_max)[0]
            en_list.append(energy)
            if len(en_list) >= 2:
                if np.abs(en_list[-1] - en_list[-2]) < self.tol:
                    converged = True
                    self._found_cutoff = cutoff
                elif cutoff > self.cutoff:
                    raise ValueError('The self interaction energy '
                                     'did not converged. Increase the cutoff')
            cutoff += 1

        return en_list[-1]*pref

    def get_E_lat(self, all_contributions=False):
        r""" Gets the :math:`E^{lat}[q]` part of the correction scheme.
        From equation (8) in Freysoldt et al. PSS B 248, 5 (2011).

        Parameters
        ----------
        all_contributions : bool
            if True, the function returns the various contributions:
            E_lat, E_lat1, E_lat2; otherwise just the total E_lat

        Returns
        -------
        energy_values : float/tuple
            The values **IN** eV.
        """
        self.eper = self._get_E_lat1()*conversion_table['Hartree']['eV']
        self.eself = self._get_E_lat2()*conversion_table['Hartree']['eV']

        if all_contributions:
            return ((self.eper - self.eself),
                    self.eper,
                    self.eself)
        return self.eper - self.eself

    def get_potential_alignment(self):
        r""" Get the potential alignment term.
        I.e. the :math:`q \Delta V` term in equation (13)
        of PSS B 248, 5 (2011)
        """
        locpot_pristine = self.pristine_locpot.copy()
        locpot_defective = self.defective_locpot.copy()
        try:
            assert locpot_pristine.shape == locpot_defective.shape
        except AssertionError:
            raise AssertionError('The two potentials must be defined on '
                                 'the same grid!')
        grid_axis = locpot_pristine.shape[self.axis]
        self._grid_axis = grid_axis

        locpot = locpot_defective - locpot_pristine
        av_locpot = plane_average_potential(locpot, self.axis)
        self.av_locpot = av_locpot

        # Shift the average potential such that the defect lies at the origin
        self.av_locpot = self._shift_av_pot(self.av_locpot)
        # calculate long-range potential
        v_long_range, self.Vo = self._get_long_range_potential()
        self.av_long_range_potential = v_long_range
        v_short_range = self.av_locpot - self.av_long_range_potential
        self.av_short_range_potential = v_short_range

        # get potential alignment
        # get it from the value of the short-range potential
        # far from the defect
        delta = self._grid_axis*0.025
        delta = int(delta)
        start = self._grid_axis//2 - delta + 1
        end = self._grid_axis//2 + delta
        v_alignment = v_short_range[start : end]
        self.v_alignment = -v_alignment.mean()
        return self.v_alignment

    def _shift_av_pot(self, locpot):
        """ Shifts the averaged locpot such that the defective site lies
        at the origin
        """
        pos = self.def_position
        # coordinate of the defect position along the axis of average
        axis_pos = pos[self.axis]
        step = 1/self._grid_axis
        point_found = False
        index = None
        for i in range(self._grid_axis):
            if np.abs(i*step - axis_pos) < self.shift_tol:
                index = i
                point_found = True
        if not point_found:
            raise Exception('The potential grid mesh is not fine enough! '
                            'Cannot shift '
                            'the plane-averaged electrostatic potential. '
                            'Use a finer mesh or set a larger self.shift_tol')
        locpot = np.roll(locpot, self._grid_axis - index)
        return locpot

    def _get_long_range_potential(self):
        """ Calculates the long-range electrostatic potential originated by
        the model charge distribution. Since the distribution is spherically
        symmetric, we approximate the potential to one dimension.
        Use the Fourier components as in equation (7) of PSS B 248, 5 (2011).

        Returns the value in eV
        """
        v_rec = np.zeros(self._grid_axis, dtype=np.complex128)
        pref = 4*np.pi*self.q/self.eps
        # ordere follows the frequencies ordering in np.fft
        v_rec[0] = (-self.q*2*np.pi
                    *self.qmodel.Fourier_transform_gto0()/self.eps)
        # on the rest of the 1D grid
        conv = conversion_table['Angstrom']['Bohr']
        cell_r = 2*np.pi*self.reciprocal_cell/conv

        reciprocal_vectors = []
        for i in range(1, self._grid_axis):
            # first the positive frequencies:
            if i < self._grid_axis//2:
                j = i
            # then the negative ones
            else:
                j = i - self._grid_axis
            g_frac = np.zeros(3, dtype=np.float64)
            g_frac[self.axis] = j
            g = np.dot(cell_r, g_frac)
            reciprocal_vectors.append(np.linalg.norm(g))
            v_rec[i] = pref * self.qmodel.Fourier_transform()(g)/np.dot(g, g)
        v_rec /= (self.volume*conversion_table['Angstrom']['Bohr']**3)
        # trasform to real space
        v = np.fft.ifft(v_rec)
        v *= len(v_rec)
        v *= conversion_table['Hartree']['eV']
        v_real_part = np.real(v)
        v_im_part = np.imag(v)
        try:
            assert np.abs(np.max(v_im_part)) < self.tol
        except AssertionError:
            raise AssertionError('The imaginary part of the long range '
                                 'potential is not zero!')
        return v_real_part, v_rec[0]

    def get_correction_energy(self):
        """ Returns the correction energy for finite-size effects to add
        to the calculated DFT energy.

        Returns
        -------
        E_corr : float
            The correction term
        """
        try:
            alignment = self.v_alignment
        except AttributeError:
            self.get_potential_alignment()
            alignment = self.v_alignment
        return -self.get_E_lat() + self.q*alignment


class FPlotterPot:
    """
    Helper class for plotting the potentials.

    Parameters
    ----------
    coordinates : array
        coordinates to plot the potentials along an axis,
        can be fractional or Cartesian

    av_locpot_diff : array
        difference DFT potential between defective and pristine system
        plane-averaged along an axis

    av_lr_pot : array
        the analytical long-range potential, plane-averaged over an axis

    av_sr_pot : array
        the short-range potential

    pot_alignment : float
        the final aligment of the potentials far from the defect

    axis_name : string
        the name of the axis along which the potentials were calculated
    """
    def __init__(self, coordinates, av_locpot_diff, av_lr_pot, av_sr_pot,
                 pot_alignment, axis_name):
        self.x = np.array(coordinates)
        self.av_locpot = av_locpot_diff
        self.av_lr_locpot = av_lr_pot
        self.av_sr_locpot = av_sr_pot
        self.c = pot_alignment
        self.axis_name = axis_name

    def plot(self, title=''):
        """ Plot the potentials

        Parameters
        ----------
        title : string, optional
            the plot title
        """
        fig = plt.figure(figsize=(12, 8))
        fig.suptitle(title, fontsize=40)
        ax = fig.add_subplot(111)
        ax.plot(self.x, self.av_locpot, c='black', linewidth=2,
                label='DFT local potential: defective - pristine')
        ax.plot(self.x, self.av_lr_locpot, c='red', linewidth=2,
                label='Long-range potential')
        ax.plot(self.x, self.av_sr_locpot, c='blue', linewidth=2,
                label='Short-range potential')
        ax.plot(self.x, np.full(len(self.x), self.c), c='black',
                linestyle='--')

        x_lim = (round(self.x[0]), self.x[-2])
        ymin = min(min(self.av_locpot), min(self.av_lr_locpot),
                   min(self.av_sr_locpot)) * 1.1
        ymax = max(max(self.av_locpot), max(self.av_lr_locpot),
                   max(self.av_sr_locpot)) * 1.1
        y_lim = (ymin, ymax)
        ax.set_xlim(x_lim)
        ax.set_ylim(y_lim)
        if (self.x <= 1).all():
            x_label = 'Fractional coordinates axis ' + self.axis_name
        else:
            x_label = ('Distance from defect along axis '
                       + self.axis_name + r' ($\AA$)')

        ax.set_xlabel(x_label, fontsize=30)
        ax.set_ylabel('Local electrostatic potential (V)', fontsize=30)

        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        ax.legend(fontsize=18, loc='best')
        fig.savefig('plot_' + title + '_potentials.pdf', bbox_inches='tight',
                    figsize=(12, 8), format='pdf', dpi=300)
        plt.show()


class FFitChargeDensity:
    """ Fits the model charge density to the DFT defective charge density
    averaged along an axis.

    Parameters
    ----------
    cell : 2D numpy array
        each row reoresents the Cartesian coordinates of one cell parameter
        of the crystal unit cell

    charge_model : class
        model of the charge density

    density_proj_def : 3D numpy array
        the defect-induced charge density on a 3D grid.
        In case of spin-polarized calculations, it is the net charge
        density.
        The shape of the array is:
        (Na, Nb, Nc)

        where Nx is the number of grid points along the cell parameter x

    defect_position : 1D array
        the position of the defect with respect to the cell parameters (i.e.
        the fractional coordinates)

    axis_average : int
        the axis along which perform the plane-average

    tol : float
        numerical spatial tolerance
    """
    def __init__(self, cell, charge_model, density_proj_def, defect_position,
                 axis_average, tol=1e-5):
        self.cell = cell.copy()
        self.cell_lenghts = np.linalg.norm(cell, axis=1)
        self.qmodel = charge_model()
        self.chgcar_proj = density_proj_def.copy()
        self.defect_pos = defect_position
        self.axis = axis_average
        self.tol = tol

    def _get_average_chgcar(self):
        chgcar_p = self.chgcar_proj.copy()
        dx = chgcar_p.shape[self.axis]
        dx = self.cell_lenghts[self.axis]/dx
        av_chgcar = plane_average_potential(chgcar_p, self.axis)
        # normalize it
        N = np.trapz(av_chgcar, dx=dx)
        av_chgcar /= N

        self.av_chgcar = av_chgcar

    def _shift_av_chgcar(self, chgcar):
        self._grid_axis = chgcar.shape[0]
        pos = self.defect_pos
        axis_pos = pos[self.axis]
        step = 1/self._grid_axis
        point_found = False
        index = None
        for i in range(self._grid_axis):
            if np.abs(i*step - axis_pos) < self.tol:
                index = i
                point_found = True
        if not point_found:
            raise Exception('The grid mesh ({} points) is not fine enough! '
                            'Cannot shift the averaged '
                            'density'.format(self._grid_axis))
        chgcar = np.roll(chgcar, self._grid_axis - index)
        return chgcar

    def fit_model(self):
        """ Fit the model charge density """
        self._get_average_chgcar()
        av_chgcar = self.av_chgcar
        av_chgcar = self._shift_av_chgcar(av_chgcar)
        self.av_chgcar = av_chgcar
        cell_p = self.cell_lenghts[self.axis]

        self.cart_grid = np.array([n*cell_p/self._grid_axis
                                   for n in range(self._grid_axis)])
        # make symmetric grid
        if self._grid_axis % 2 == 0:
            mid = self._grid_axis//2
        else:
            mid = self._grid_axis//2 +1
        ga = self.cart_grid[:self._grid_axis//2]
        gb = self.cart_grid[self._grid_axis//2:]
        gb = -(self.cart_grid[-1] - gb)
        self.symm_cart_grid = np.zeros_like(self.cart_grid)
        self.symm_cart_grid[:mid] = gb
        self.symm_cart_grid[mid:] = ga
        # make symmetric charge density
        av_chgcar = np.roll(av_chgcar, mid)
        # shift to the value far from the defect
        align = av_chgcar[0]
        av_chgcar -= align
        self.symm_av_chgcar = av_chgcar
        # fit
        model = self.qmodel.get_model_D()
        popt, pcov = curve_fit(model, self.symm_cart_grid, av_chgcar,
                               bounds=([0, 0, 0], [1, np.inf, np.inf]))

        return popt, pcov
