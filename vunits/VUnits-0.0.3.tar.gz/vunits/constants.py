# -*- coding: utf-8 -*-
"""
vunits.constants

Contains universal constants for catalysis research.
"""

import numpy as np
from vunits.db import _temp_units
from vunits.quantity import Quantity, _force_get_quantity

R = Quantity.from_units(mag=8.3144598, units='J/mol/K')
r""":class:`~vunits.quantity.Quantity`: Molar (univeral or ideal) gas constant.

**SI Value**: 8.3144598 J/mol/K

**Dimensions**: :ref:`energy <energy_table>`/:ref:`amount <amount_table>`/
:ref:`temperature <temp_table>` or equivalent quantities.
"""

h = Quantity.from_units(mag=6.626070040e-34, units='J s')
r""":class:`~vunits.quantity.Quantity`: Planck's constant.

**SI Value**: 6.626070040e-34 J s.

**Dimensions**: :ref:`energy <energy_table>`/:ref:`time <time_table>` or equivalent
quantities."""

h_bar = h/2./np.pi
r""":class:`~vunits.quantity.Quantity`: Planck's constant divided by
2\ :math:`\pi`\ .
    
**SI Value**: 1.0545718e-34 J s

**Dimensions**: :ref:`energy <energy_table>`/:ref:`time <time_table>` or
equivalent quantities."""

kb = Quantity.from_units(mag=1.38064852e-23, units='J/K')
r""":class:`~vunits.quantity.Quantity`: Boltzmann constant.

**SI Value**: 1.38064852e-23 J/K

**Dimensions**: :ref:`energy <energy_table>`/:ref:`temperature <temp_table>` or
equivalent quantities."""

c = Quantity(mag=299792458., m=1., s=-1.)
r""":class:`~vunits.quantity.Quantity`: Speed of light.

**SI Value**: 299792458 m/s

**Dimensions**: :ref:`length <length_table>`/:ref:`time <time_table>` or equivalent
quantities.
"""

m_e = Quantity(mag=9.1093837015e-31, kg=1.)
r""":class:`~vunits.quantity.Quantity`: Mass of a electron.

**SI Value**: 9.1093837015e-31 kg

**Dimensions**: :ref:`mass <mass_table>` or equivalent quantities."""

m_p = Quantity(mag=1.67262192369e-27, kg=1.)
r""":class:`~vunits.quantity.Quantity`: Mass of a proton.

**SI Value**: 1.67262192369e-27 kg

**Dimensions**: :ref:`mass <mass_table>` or equivalent quantities."""

m_n = Quantity(mag=1.67492749804e-27, kg=1.)
r""":class:`~vunits.quantity.Quantity`: Mass of a neutron.

**SI Value**: 1.67492749804 kg

**Dimensions**: :ref:`mass <mass_table>` or equivalent quantities."""

P0 = Quantity.from_units(mag=1., units='bar')
r""":class:`~vunits.quantity.Quantity`: Standard pressure.

**SI Value**: 1 bar

**Dimensions**: :ref:`pressure <pressure_table>` or equivalent quantities."""

T0 = Quantity(mag=298.15, K=1.)
r""":class:`~vunits.quantity.Quantity`: Standard temperature.

**SI Value**: 298.15 K

**Dimensions**: :ref:`temperature <temp_table>` or equivalent quantities."""

V0 = R*T0/P0
r""":class:`~vunits.quantity.Quantity`: Standard volume. 

**SI Value**: 0.024789561893699998 m\ :sup:`3`\ /mol

**Dimensions**: :ref:`volume <volume_table>`/:ref:`amount <amount_table>` or
equivalent quantities."""

N0 = Quantity(mag=6.02214086e23)
r""":class:`~vunits.quantity.Quantity`: Avogadro number. Use this value instead
of Avogadro's constant (``Na``) to preserve units.

**SI Value**: 6.02214086e23 molecules/mol

**Dimensions**: None"""

Na = Quantity(mag=6.02214086e23, mol=-1.)
r""":class:`~vunits.quantity.Quantity`: Avogadro constant.

**SI Value**: 6.02214086e23 1/mol

**Dimensions**: :ref:`amount <amount_table>`\ :sup:`-1`\ ."""

e = Quantity.from_units(mag=1.6021766208e-19, units='C')
r""":class:`~vunits.quantity.Quantity`: Charge of electron.

**SI Value**: 1.6021766208e-19 C

**Dimensions**: :ref:`charge <charge_table>` or equivalent quantities."""

F = e*Na
r""":class:`~vunits.quantity.Quantity`: Faraday's constant.

**SI Value**: 96485.33293056407 C/mol

**Dimensions**: :ref:`charge <charge_table>`/:ref:`amount <amount_table>` or
equivalent quantities."""

G = Quantity(mag=6.67430e-11, m=3., kg=-1., s=-2)
r""":class:`~vunits.quantity.Quantity`: Gravitational constant.

**SI Value**: 6.67430e-11 m\ :sup:`3`\ kg\ :sup:`-1`\ s\ :sup:`-2`\.

**Dimensions**: :ref:`volume <volume_table>`/:ref:`mass <mass_table>`/
:ref:`time <time_table>` or equivalent quantities."""

eps_0 = Quantity.from_units(8.8541878128e-12, 'F/m')
r""":class:`~vunits.quantity.Quantity`: Vacuum permittivity.

**SI Value**: 8.8541878128e-12 F/m

**Dimensions**: :ref:`capacitance <capacitance_table>`/
:ref:`length <length_table>` or equivalent quantities.
"""

mu_0 = Quantity.from_units(1.25663706212e-6, 'H/m')
r""":class:`~vunits.quantity.Quantity`: Vacuum permeability.

**SI Value**: 1.25663706212e-6 H/m

**Dimensions**: :ref:`inductance <inductance_table>`/
:ref:`length <length_table>` or equivalent quantities.
"""

R_inf = m_e*e**4/8./eps_0**2/h**2
r""":class:`~vunits.quantity.Quantity`: Rydberg constant.

**SI Value**: 2.1799233153862138e-18 J

**Dimensions**: :ref:`energy <energy_table>` or equivalent quantities."""

r_bohr = 4.*np.pi*eps_0*h_bar**2/m_e/e**2
r""":class:`~vunits.quantity.Quantity`: Bohr radius.

**SI Value**: 5.291648330110941e-11 m

**Dimensions**: :ref:`length <length_table>` or equivalent quantities.
"""