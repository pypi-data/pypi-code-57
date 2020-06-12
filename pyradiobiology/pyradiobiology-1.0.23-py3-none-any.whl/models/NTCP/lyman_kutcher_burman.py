from ..geud import Geud
from ..linear_quadratic import LinearQuadratic
from ...primitives import Dose, DoseType
from ...primitives.dosearray import DoseArray
from ...primitives.dose_converter import DoseConverter
import numpy as np
from math import erf


class LKB():
    def __init__(self, td50: Dose, m: float, n: float) -> None:
        self._validate_td50_or_throw_exception(td50)
        self._validate_positive_or_throw_exception(m, "m must be a positive number")
        self._validate_positive_or_throw_exception(n, "n must be a positive number")
        self.td50 = td50
        self.m = m
        self.n = n

    def _validate_positive_or_throw_exception(self, value, message):
        if value < 0:
            raise ValueError(message)

    def _validate_td50_or_throw_exception(self, td50):
        if not isinstance(td50, Dose):
            raise ValueError('td50 must be type of Dose')
        if td50.dose_type != DoseType.EQD2:
            raise ValueError('td50 must be in EQD2')

    def response(self, dose_array_in_eqd2: DoseArray, volume_array):
        if not isinstance(volume_array, type(np.array)):
            volume_array = np.array(volume_array)
        if dose_array_in_eqd2.unit != self.td50.unit:
            raise ValueError(
                f'dose_array unit ({dose_array_in_eqd2.unit}) is different from d50 unit ({self.td50.unit})')

        if dose_array_in_eqd2.dose_type != DoseType.EQD2:
            raise ValueError("dose_array_inEQD2 must be in EQD2 DoseType")

        total_volume = np.sum(volume_array)

        geud_model = Geud(1.0 / self.n)
        geud = geud_model.calculate(dose_array_in_eqd2, volume_array)
        t = self._calculate_t(geud, self.td50, self.m)
        x = t * (1.0 / np.sqrt(2.0))
        return 0.5 * (1.0 + erf(x))

    def _calculate_t(self, geud, td50, m):
        return (geud - td50.value) / (m * td50.value)

    def response_from_pysical_dose(self, dose_array_in_physical_dose: DoseArray, volume_array, ab_ratio: Dose,
                                   nfx: int):
        lqmodel = LinearQuadratic(ab_ratio=ab_ratio, nfx=nfx)
        eqd0_dose_array = lqmodel.eqd0(dose_array_in_physical_dose)
        return self.response(dose_array_in_eqd2=DoseConverter.to_eqd2_from_eqd0(eqd0_dose_array),
                             volume_array=volume_array)
