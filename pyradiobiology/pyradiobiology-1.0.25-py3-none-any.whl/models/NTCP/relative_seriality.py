from ..linear_quadratic import LinearQuadratic
from ...primitives import Dose, DoseType
from ...primitives.dosearray import DoseArray
from ...primitives.dose_converter import DoseConverter
import numpy as np


class RelativeSeriality():
    def __init__(self, td50: Dose, gamma: float, seriality: float) -> None:
        self._validate_td50_or_throw_exception(td50)
        self._validate_positive_or_throw_exception(gamma, 'gamma must be in range [0... +Inf]')
        self._validate_positive_or_throw_exception(seriality, 'seriality must be in range [0... +Inf]')
        self.seriality = seriality
        self.gamma = gamma
        self.td50 = td50

    def _validate_td50_or_throw_exception(self, td50):
        if not isinstance(td50, Dose):
            raise ValueError('td50 must be type of Dose')
        if td50.dose_type != DoseType.EQD2:
            raise ValueError('td50 must be in EQD2')

    def _validate_positive_or_throw_exception(self, value, message):
        if value < 0:
            raise ValueError(message)

    def response(self, dose_array_in_eqd2: DoseArray, volume_array):
        if not isinstance(volume_array, type(np.array)):
            volume_array = np.array(volume_array)
        if dose_array_in_eqd2.unit != self.td50.unit:
            raise ValueError(
                f'dose_array unit ({dose_array_in_eqd2.unit}) is different from d50 unit ({self.td50.unit})')

        if dose_array_in_eqd2.dose_type != DoseType.EQD2:
            raise ValueError("dose_array_inEQD2 must be in EQD2 DoseType")

        total_volume = np.sum(volume_array)
        egamma = np.exp(1) * self.gamma
        lnln2 = np.log(np.log(2.0))
        egamma_minus_lnln2 = egamma - lnln2
        eqd2_devided_by_td50 = dose_array_in_eqd2.data / self.td50.value
        ntcp_voxels = np.exp(- np.exp(egamma - (eqd2_devided_by_td50 * egamma_minus_lnln2)))
        ntcps = (1.0 - ntcp_voxels**self.seriality)**(volume_array/total_volume)
        return (1.0 - np.prod(ntcps))**(1.0 / self.seriality)

    def response_from_pysical_dose(self, dose_array_in_physical_dose: DoseArray, volume_array, ab_ratio: Dose,
                                   nfx: int):
        lqmodel = LinearQuadratic(ab_ratio=ab_ratio, nfx=nfx)
        eqd0_dose_array = lqmodel.eqd0(dose_array_in_physical_dose)
        return self.response(dose_array_in_eqd2=DoseConverter.to_eqd2_from_eqd0(eqd0_dose_array),
                             volume_array=volume_array)

