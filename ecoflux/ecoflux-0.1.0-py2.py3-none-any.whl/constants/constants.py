"""A collection of physical, chemical, and environmental constants."""
from typing import List

import scipy.constants as _sc

# chemical constants
M_d: float = 28.964_5e-3  # dry air molar mass [kg mol^-1]
M_w: float = 18.015_28e-3  # water vapor molar mass [kg mol^-1]
R_d: float = _sc.R / M_d  # specific gas constant of dry air [J kg^-1 K^-1]
R_w: float = _sc.R / M_w  # specific gas constant of water vapor[J kg^-1 K^-1]

# isobaric specific heat capacity of dry air [J kg^-1 K^-1]
cp_d: float = 1.004e3
# isobaric molar heat capacity of dry air [J mol^-1 K^-1]
cpm_d: float = cp_d * M_d
# note: variation with temperature is negligible in the atmosphere

# soil texture names, USDA classification
soil_textures: List[str] = [
    "sand",
    "loamy sand",
    "sandy loam",
    "loam",
    "silt",
    "silt loam",
    "sandy clay loam",
    "clay loam",
    "silty clay loam",
    "sandy clay",
    "silty clay",
    "clay",
]

# properties of the earth
eccentricity: float = 0.016_704_232

# properties of the atmosphere
m_atm: float = 5.1480e18  # total mass of the atmosphere [kg]
m_atm_d: float = 5.1352e18  # dry mass of the atmosphere [kg]
Gamma_d: float = _sc.g / cp_d  # dry lapse rate [K m^-1]
Gamma_mean: float = 6.5e-3  # mean lapse rate [K m^-1]
kappa: float = 0.40  # von Karman constant [-]
