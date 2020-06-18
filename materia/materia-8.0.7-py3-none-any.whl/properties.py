from __future__ import annotations
from typing import Iterable, Optional, Union

import numpy as np
import scipy.linalg, scipy.spatial

import materia as mtr
from materia.utils import memoize

__all__ = ["Dipole", "Excitation", "ExcitationSpectrum", "Polarizability"]


class Dipole:
    def __init__(self, dipole_moment: mtr.Quantity) -> None:
        self.dipole_moment = dipole_moment

    @property
    @memoize
    def norm(self) -> mtr.Quantity:
        return np.linalg.norm(self.dipole_moment.value) * self.dipole_moment.unit


class Excitation:
    def __init__(
        self,
        energy: mtr.Quantity,
        oscillator_strength: Optional[float, mtr.Quantity],
        transition_moment=None,
        symmetry=None,
        total_energy=None,
        contributions=None,
    ) -> None:
        self.energy = energy
        self.oscillator_strength = oscillator_strength
        self.transition_moment = transition_moment
        self.symmetry = symmetry
        self.total_energy = total_energy
        self.contributions = contributions


class ExcitationSpectrum:
    def __init__(self, excitations: Iterable[Excitation]) -> None:
        self.excitations = excitations

    def to_gaussian(self) -> str:
        return "\n".join(
            f"Excited State {i+1} {1 if exc.symmetry == 'Singlet' else 2} {exc.energy.convert(mtr.eV).value}\n"
            + "".join(
                f"    {e} -> {h}    {coeff}\n"
                for (e, _), (h, _), coeff in exc.contributions
            )
            for i, exc in enumerate(self.excitations)
        )

    # def plot_stick_spectrum(self):
    #     linecoll = matplotlib.collections.LineCollection(
    #         ((eng, 0), (eng, s)) for eng, s in zip(self.energies, self.strengths)
    #     )
    #     fig, ax = plt.subplots()
    #     ax.add_collection(linecoll)
    #     plt.scatter(self.energies, self.strengths)

    #     plt.show()

    def broaden(
        self, fwhm: mtr.Quantity
    ) -> Callable[Iterable[Union[int, float]], Iterable[Union[int, float]]]:
        def f(energies: mtr.Quantity) -> Iterable[Union[int, float]]:
            s = 0
            # for excitation in self.excitations:
            #     x = (energies - excitation.energy) / fwhm
            #     x = np.array([e.value for e in x])
            #     s += excitation.oscillator_strength * np.exp(-np.log(2) * (2 * x ** 2))
            # return s
            for excitation in self.excitations:
                x = (energies - excitation.energy) / fwhm
                x = np.array([e.value for e in x])
                s += excitation.oscillator_strength * np.exp(-0.5 * x ** 2)
            return s / (np.sqrt(2 * np.pi) * fwhm)

        return f

    def dipole_strength(
        self, fwhm: mtr.Quantity
    ) -> Callable[Iterable[Union[int, float]], Iterable[Union[int, float]]]:
        def f(energies: mtr.Quantity) -> Iterable[Union[int, float]]:
            return self.broaden(fwhm)(energies)  # /energies

        return f

    def cross_section(
        self, fwhm: mtr.Quantity
    ) -> Callable[Iterable[Union[int, float]], Iterable[Union[int, float]]]:
        def f(energies: mtr.Quantity) -> Iterable[Union[int, float]]:
            return (
                np.pi * mtr.e ** 2 * mtr.hbar / (2 * mtr.epsilon_0 * mtr.m_e * mtr.c)
            ) * self.dipole_strength(fwhm)(energies)

        return f

    def molar_absorptivity(
        self, fwhm: mtr.Quantity
    ) -> Callable[Iterable[Union[int, float]], Iterable[Union[int, float]]]:
        def f(energies: mtr.Quantity) -> Iterable[Union[int, float]]:
            return (
                mtr.N_A * self.cross_section(fwhm)(energies) / 1e3 / np.log(10)
            ).convert(mtr.L / mtr.mol / mtr.cm)

        return f

    # def plot_broadened_spectrum(self, fwhm, energies):
    #     fig, ax = plt.subplots()
    #     plt.plot(energies, self.broaden_spectrum(fwhm=fwhm)(energies))

    #     plt.show()

    # def molar_absorptivities(self):
    #     return (
    #         3
    #         * np.pi
    #         * materia.mole.prefactor
    #         * materia.fundamental_charge.prefactor ** 2
    #         * self.strengths
    #         / (
    #             2e3
    #             * np.log(10)
    #             * materia.electron_mass.prefactor
    #             * np.array([eng.value for eng in self.energies])
    #         )
    #     )

    # def broaden_molar_absorptivities(self, fwhm):
    #     def f(engs):
    #         return sum(
    #             strength * np.exp(-np.log(2) * (2 * (engs - eng) / fwhm) ** 2)
    #             for eng, strength in zip(self.energies, self.molar_absorptivities())
    #         )

    #     return f

    # def plot_broadened_molar_absorptivities(self, fwhm, energies):
    #     fig, ax = plt.subplots()
    #     plt.plot(energies, self.broaden_molar_absorptivities(fwhm=fwhm)(energies))

    #     plt.show()

    # plt.plot(1240/energies,)

    # def stick_spectrum(self):
    #     # FIXME: just completely fix
    #     def f(w,w0,s):
    #         return np.exp(-((w-w0)/s)**2)
    #     sum(A*f(w=w,w0=W,s=0.5) for A,W in zip(a,ws))
    #     #self._parse()


class Orbitals:
    pass


class Polarizability:
    def __init__(self, polarizability_tensor, applied_field=None):
        self.pol_tensor = polarizability_tensor
        self.applied_field = None

    @property
    @memoize
    def isotropic(self):
        return np.trace(self.pol_tensor.value) * self.pol_tensor.unit / 3

    @property
    @memoize
    def anisotropy(self):
        # FIXME: verify accuracy of this method
        return (
            np.sqrt(
                (
                    np.trace(a=self.pol_tensor @ self.pol_tensor)
                    - 3 * self.isotropic ** 2
                ).value
            )
            * self.pol_tensor.unit
        )

    @property
    @memoize
    def eigenvalues(self):
        return np.linalg.eigvals(a=self.pol_tensor.value) * self.pol_tensor.unit


class Response:
    def __init__(self, applied_field):
        super().__init__()
        self.applied_field = applied_field


class TDDipole:  # (TimeSeries):
    def __init__(self, time, tddipole, applied_field=None):
        super().__init__(time=time, series=tddipole)
        self.tddipole = mtr.TimeSeries(x=time, y=tddipole)
        # # tddipole_norm.value should be 1xNt matrix where Nt is number of time steps
        # # tddipole_dir should be 3xNt matrix where Nt is number of time steps and each column is a unit direction vector
        # super().__init__()
        # self.tddipole_moment

    @property
    @memoize
    def dt(self):
        return self.tddipole.dt()

    @property
    @memoize
    def T(self):
        return self.tddipole.T()

    def damp(self, final_damp_value=1e-4):
        self.tddipole.damp(final_damp_value=final_damp_value)

    @property
    @memoize
    def fourier_transform(self, pad_len=None):
        return self.tddipole.fourier_transform(pad_len=pad_len)


class TDPolarizability:  # (TimeSeries):
    def __init__(self, time, td_polarizability):
        super().__init__(time=time, series=td_polarizability)

    @property
    @memoize
    def dt(self):
        return self.tddipole.dt()

    @property
    @memoize
    def T(self):
        return self.tddipole.T()

    def damp(self, final_damp_value=1e-4):
        self.tddipole.damp(final_damp_value=final_damp_value)

    @property
    @memoize
    def fourier_transform(self, pad_len=None):
        return self.tddipole.fourier_transform(pad_len=pad_len)


class Permittivity:
    def __init__(self, permittivity):
        self.permittivity = permittivity


class Volume:
    def __init__(self, volume):
        self.volume = volume
