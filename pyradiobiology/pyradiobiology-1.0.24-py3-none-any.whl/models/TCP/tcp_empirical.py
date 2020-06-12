from ...primitives import DoseArray, DoseType, Dose
from ..linear_quadratic import *
from ...primitives.dose_converter import *

import numpy as np

class TcpEmpirical():

    def __init__(self, d50: Dose, gamma: float) -> None:
        self._validate_d50_or_throw_exception(d50)
        self._validate_positive_or_throw_exception(gamma, 'gamma must be positive number.')
        self.gamma = gamma
        self.d50 = d50

    def _validate_d50_or_throw_exception(self, d50):
        if not isinstance(d50, Dose):
            raise ValueError('d50 must be type of Dose')
        if d50.dose_type != DoseType.EQD2:
            raise ValueError('d50 must be in EQD2')

    def _validate_positive_or_throw_exception(self, value, message):
        if value < 0:
            raise ValueError(message)

    def _validate_doseArray_or_throw_exception(self, dose_array):
        if not isinstance(dose_array, DoseArray):
            raise ValueError('dose_array must be type of DoseArray')
        if dose_array.dose_type != type(DoseType.EQD2):
            raise ValueError('dose_array must be in EQD2')

    def response(self, dose_array_in_eqd2: DoseArray, volume_array):
        if not isinstance(volume_array, type(np.array)):
            volume_array = np.array(volume_array)
        if dose_array_in_eqd2.unit != self.d50.unit:
            raise ValueError(
                f'dose_array unit ({dose_array_in_eqd2.unit}) is different from d50 unit ({self.d50.unit})')

        if dose_array_in_eqd2.dose_type != DoseType.EQD2:
            raise ValueError("dose_array_inEQD2 must be in EQD2 DoseType")

        total_volume = np.sum(volume_array)
        tcp_voxels = self._voxel_responce(dose_array_in_eqd2=dose_array_in_eqd2)
        tcps = tcp_voxels ** (volume_array / total_volume)
        return np.prod(tcps)

    def response_from_pysical_dose(self, dose_array_in_physical_dose: DoseArray, volume_array, ab_ratio: Dose,
                                   nfx: int):
        lqmodel = LinearQuadratic(ab_ratio=ab_ratio, nfx=nfx)
        eqd0_dose_array = lqmodel.eqd0(dose_array_in_physical_dose)
        return self.response(dose_array_in_eqd2=DoseConverter.to_eqd2_from_eqd0(eqd0_dose_array),
                             volume_array=volume_array)

    def _voxel_responce(self, dose_array_in_eqd2):
        egamma = np.exp(1) * self.gamma
        lnln2 = np.log(np.log(2.0))
        egamma_minus_lnln2 = egamma - lnln2
        eqd2_devided_by_d50 = dose_array_in_eqd2.data / self.d50.value
        tcp_voxels = np.exp(- np.exp(egamma - (eqd2_devided_by_d50 * egamma_minus_lnln2)))
        return tcp_voxels

    def voxel_response(self, dose_array_in_eqd2: DoseArray):
        if dose_array_in_eqd2.unit != self.d50.unit:
            raise ValueError(
                f'dose_array unit ({dose_array_in_eqd2.unit}) is different from d50 unit ({self.d50.unit})')

        if dose_array_in_eqd2.dose_type != DoseType.EQD2:
            raise ValueError("dose_array_inEQD2 must be in EQD2 DoseType")

        return self._voxel_responce(dose_array_in_eqd2=dose_array_in_eqd2)
