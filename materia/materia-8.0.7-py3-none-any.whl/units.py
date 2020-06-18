import scipy.constants
import materia as mtr

# UNITLESS
unitless = mtr.Quantity()

# LENGTH
meter = m = mtr.Quantity(L=1)
centimeter = cm = (1e-2 * meter).to_unit()
millimeter = mm = (1e-3 * meter).to_unit()
micrometer = micron = (1e-6 * meter).to_unit()
nanometer = nm = (1e-9 * meter).to_unit()
angstrom = (1e-10 * meter).to_unit()
bohr = au_length = (scipy.constants.value("Bohr radius") * meter).to_unit()
picometer = pm = (1e-12 * meter).to_unit()
femtometer = fm = (1e-15 * meter).to_unit()
attometer = (1e-18 * meter).to_unit()
kilometer = km = (1e3 * meter).to_unit()
astronomical_unit = au = (1.495978707e11 * meter).to_unit()

# MASS
kilogram = kg = mtr.Quantity(M=1)
gram = g = (1e-3 * kilogram).to_unit()
milligram = mg = (1e-6 * kilogram).to_unit()
microgram = (1e-9 * kilogram).to_unit()
amu = (scipy.constants.value("atomic mass constant") * kilogram).to_unit()
electron_mass = (scipy.constants.m_e * kilogram).to_unit()

# TIME
second = s = mtr.Quantity(T=1)
millisecond = ms = (1e-3 * second).to_unit()
microsecond = (1e-6 * second).to_unit()
nanosecond = ns = (1e-9 * second).to_unit()
picosecond = ps = (1e-12 * second).to_unit()
femtosecond = fs = (1e-15 * second).to_unit()
au_time = (
    (
        scipy.constants.value("Bohr radius")
        / (scipy.constants.fine_structure * scipy.constants.c)
    )
    * second
).to_unit()
attosecond = (1e-18 * second).to_unit()
minute = min = (60 * second).to_unit()
hour = hr = (60 * minute).to_unit()
day = d = (24 * hour).to_unit()


# CURRENT
ampere = amp = mtr.Quantity(I=1)

# TEMPERATURE
kelvin = K = mtr.Quantity(K=1)

# NUMBER
mole = mol = mtr.Quantity(N=1)

# LUMINOUS INTENSITY
candela = mtr.Quantity(J=1)

# AREA
barn = (1e-28 * (meter ** 2)).to_unit()
hectare = ha = (1e4 * (meter ** 2)).to_unit()


# VOLUME
milliliter = ml = (centimeter ** 3).to_unit()
liter = L = (1e3 * milliliter).to_unit()
au_volume = (au_length ** 3).to_unit()


# CHARGE
coulomb = C = (ampere * second).to_unit()
e = fundamental_charge = au_charge = (scipy.constants.e * coulomb).to_unit()


# CGS CHARGE
# FIXME: is it really okay to convert from CGS to SI like this?
statcoulomb = statC = franklin = Fr = electrostatic_unit = esu = (
    coulomb / (10 * scipy.constants.c)
).to_unit()


# FORCE
newton = (kilogram * meter / (second ** 2)).to_unit()


# PRESSURE
pascal = (newton / (meter ** 2)).to_unit()


# ENERGY
joule = J = (newton * meter).to_unit()
calorie = cal = (4.184 * joule).to_unit()
kilocalorie = kcal = (calorie * 1e3).to_unit()
electronvolt = ev = eV = (scipy.constants.e * joule).to_unit()
hartree = au_energy = (
    (
        scipy.constants.value("electron mass energy equivalent")
        * scipy.constants.fine_structure ** 2
    )
    * joule
).to_unit()
rydberg = (hartree / 2).to_unit()


# POWER
watt = W = (joule / second).to_unit()


# ELECTRIC POTENTIAL
volt = V = (joule / coulomb).to_unit()


# CAPACITANCE
farad = F = (coulomb / volt).to_unit()


# RESISTANCE
ohm = (volt / ampere).to_unit()


# CONDUCTANCE
siemens = (1 / ohm).to_unit()


# MAGNETIC FLUX
weber = (volt * second).to_unit()


# MAGNETIC FLUX DENSITY
telsa = (weber / (meter ** 2)).to_unit()


# INDUCTANCE
henry = (weber / ampere).to_unit()


# ABSORBED DOSE
gray = (joule / kilogram).to_unit()


# DIPOLE MOMENT
# FIXME: is it really okay to convert from CGS to SI like this?
debye = ((1e-21 / scipy.constants.c) * coulomb * meter).to_unit()
au_dipole_moment = (e * bohr).to_unit()


# FREQUENCY
hertz = (1 / second).to_unit()
au_frequency = (
    (
        scipy.constants.fine_structure
        * scipy.constants.c
        / scipy.constants.value("Bohr radius")
    )
    * hertz
).to_unit()


# ANGULAR FREQUENCY
radian_per_second = (2 * scipy.constants.pi * hertz).to_unit()
au_angular_frequency = (2 * scipy.constants.pi * au_frequency).to_unit()


# # PLANAR ANGLE
# radian = rad = (mtr.Quantity()).to_unit()
# degree = ((scipy.constants.pi/180)*radian).to_unit()

#
# # SOLID ANGLE
# steradian = sr = (mtr.Quantity()).to_unit()).to_unit()

# CONSTANTS
c = scipy.constants.c * meter / second
h = scipy.constants.h * joule * second
hbar = scipy.constants.hbar * joule * second
a_0 = scipy.constants.value("Bohr radius") * meter
kB = scipy.constants.k * joule / kelvin
epsilon_0 = scipy.constants.epsilon_0 * farad / meter
m_e = scipy.constants.m_e * kilogram
N_A = scipy.constants.N_A / mole
