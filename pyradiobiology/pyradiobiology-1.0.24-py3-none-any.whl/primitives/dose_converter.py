
from .dose import *
from .dosearray import DoseArray


class DoseConverter():
    @staticmethod
    def _get_ab_ratio(eqd0, ab_ratio: Dose):
        ab_from_data = eqd0.param_dict.get('ab_ratio')
        if ab_ratio is not None and ab_from_data is not None:
            if ab_ratio != ab_from_data:
                raise ValueError('Users ab_ratio is different from the reported ab_ratio in EQD0 data')
            return ab_from_data

        if ab_from_data is None:
            return ab_ratio
        if ab_ratio is None:
            return ab_from_data

    @staticmethod
    def to_eqd2_from_eqd0(eqd0: DoseArray, ab_ratio=None):
        if not isinstance(eqd0, DoseArray):
            raise ValueError('eqd0 must be a DoseArray.')
        if eqd0.dose_type != DoseType.EQD0:
            raise ValueError('DoseType.EQD0 was expected.')

        ab_ratio = DoseConverter._get_ab_ratio(eqd0, ab_ratio)
        eqd2 = eqd0.data / (1.0 + 2.0 / ab_ratio.value)
        return DoseArray.create(data=eqd2, unit=eqd0.unit, dose_type=DoseType.EQD2, params_dict=eqd0.param_dict)
