"""
====================================
Constants (:mod:`ecoflux.constants`)
====================================

.. currentmodule:: ecoflux.constants

Physical, chemical, and environmental constants.

Gases
=====

============  ==========================================================
``M_d``       dry air molar mass [kg mol^-1]
``M_w``       water vapor molar mass [kg mol^-1]
``R_d``       specific gas constant of dry air [J kg^-1 K^-1]
``R_w``       specific gas constant of water vapor[J kg^-1 K^-1]
``cp_d``      isobaric specific heat capacity of dry air [J kg^-1 K^-1]
``cpm_d``     isobaric molar heat capacity of dry air [J mol^-1 K^-1]
============  ==========================================================

Soil
====

===================  =======================================================
``soil_textures``    soil texture names according to the USDA classification
===================  =======================================================

Earth
=====

==================  =============================================
``eccentricity``    present-day eccentricity of the earth's orbit
==================  =============================================

Atmosphere
==========

===============  =================================
``m_atm``        total mass of the atmosphere [kg]
``m_atm_d``      dry mass of the atmosphere [kg]
``Gamma_d``      dry lapse rate [K m^-1]
``Gamma_mean``   mean lapse rate [K m^-1]
``kappa``        von Karman constant [-]
===============  =================================

References
==========

* Or, D. and Wraith, J. M. (2002). Soil Water Content and Water Potential
  Relationships, in Warrick, A. W. (eds.) *Soil Physics Companion*, pp 81–82.,
  CRC Press, Boca Raton, FL, USA.
* Rumble, J. (eds.) (2017). *CRC Handbook of Chemistry and Physics* (98th ed.).
  CRC Press, Boca Raton, FL, USA. ISBN: 9781498784542.
  http://hbcponline.com/faces/contents/ContentsSearch.xhtml
* Trenberth, K. E. and Smith, L. (2005). The mass of the atmosphere: a
  constraint on global analyses. *Journal of Climate*, 18, 864–875.
  https://doi.org/10.1175/JCLI-3299.1

"""
from .constants import *  # noqa

__all__ = [_s for _s in dir() if not _s.startswith("_")]
