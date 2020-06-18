import numpy as np
import scipy

import materia

from .dataseries import RelativeSPDSpectrum


class BlackbodySPD(RelativeSPDSpectrum):
    def __init__(self, T, normalize_to=100):
        if not isinstance(T, materia.Qty):
            T = materia.Qty(value=T, unit=materia.kelvin)

        x = materia.Qty(value=np.linspace(380, 780, 1001), unit=materia.nanometer)

        c2 = materia.Qty(
            value=(
                scipy.constants.Planck
                * scipy.constants.speed_of_light
                / scipy.constants.Boltzmann
            )
            * 1e9,
            unit=materia.nanometer * materia.kelvin,
        )

        y = materia.Qty(
            value=1 / (np.power(x, 5) * (np.exp(c2 / (x * T)) - 1)),
            unit=materia.unitless,
        )  # wrong overall prefactor, but that's okay since it will be normalized in super().__init__

        super().__init__(x=x, y=y, normalize_to=normalize_to)
