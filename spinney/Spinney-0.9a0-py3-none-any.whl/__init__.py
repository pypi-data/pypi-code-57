r""" Spinney: A Python package for first-principles
Point Defect calculations.

**Spinney** is a collection of Python modules aimed for the analysis and
postprocessing of first-principles calculations of point defects in solids.

**Spinney** can assists with the major tasks necessary for the characterization
of point defects in solids.
The classes and functions that it implements can be divided into the following
groups, which are related to the several steps necessary for processing
the *ab-initio* calculations:

- General high-level interface for point-defect calculations
    :mod:`spinney.structures.pointdefect`
        Contains the :class:`~spinney.structures.pointdefect.PointDefect`
        class which offers a convenient
        interface to  calculate the properties of a point defect, such as
        its formation energy including finite-size corrections.

- Determination of the possible values of equilibrium chemical potentials
    :mod:`spinney.thermodynamics.chempots`
        Contains the :class:`~spinney.thermodynamics.chempots.Range`
        class which is able to determine the
        possible equilibrium values of the chemical potentials given a
        set of competing phases.

        It also contains classes describing the chemical potentials of common
        gas phases, such as :math:`\mathrm{O}_2`, :math:`\mathrm{H}_2`,
        :math:`\mathrm{N}_2`, :math:`\mathrm{Cl}_2` and
        :math:`\mathrm{F}_2`, as a function of temperature and pressure
        employing experimental data and empirical formulas.

- Correction schemes for electrostatic finite-size effects in supercells
    - :mod:`spinney.defects.kumagai`
        Implements the correction scheme proposed by Kumagai and Oba in
        Phys. Rev. B 89, 195205 (2014)

    - :mod:`spinney.defects.fnv`
        Implements the correction scheme proposed by Freysoldt,
        Neugebauer and Van de Walle in Phys. Rev. Lett. 102, 016402 (2009)

- Calculation of equilibrium defect properties
    - :mod:`spinney.defects.diagrams`
        Contains the :class:`spinney.defects.diagrams.Diagram`
        class which allows to plot the defect
        formation energies as a function of the Fermi level and calculate
        charge transition levels.

    - :mod:`spinney.defects.concentration`
        Contains the
        :class:`spinney.defects.concentration.EquilibriumConcentration`
        class that allows to
        calculate equilibrium properties, such as defects and carriers
        concentrations and the Fermi level position.

- General-purpose tools
    - :mod:`spinney.tools.formulas`
        Contains some helper functions useful for dealing with chemical formulas.

    - :mod:`spinney.tools.reactions`
        Contains helper functions useful for calculating reaction energies.

- Support for first-principles codes
    The **Spinney** package currently offers interfaces for these computer codes:

    - `VASP <https://www.vasp.at/>`_: :mod:`spinney.io.vasp`

    - `WIEN2k <http://www.wien2k.at/>`_: :mod:`spinney.io.wien2k`

"""
import numpy as np
from spinney.__about__ import *

containers = (list, tuple, np.ndarray)
