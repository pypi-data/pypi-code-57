
import numpy as np
from ..primitives.dose import *
from ..primitives.dosearray import DoseArray


class LinearQuadratic():
    """Linear quadratic model.
    SF = exp(-a*dose -beta*dose^2) = exp(-a*dose*(1 + dose/ab_ratio)),
    where ab_ratio = alpha/beta

    """

    def __init__(self, ab_ratio: Dose, nfx: int) -> None:
        """
        LinearQuadratic ctor.

        :param ab_ratio: Dose.
        :param nfx: Number of fractions. A number from 1...+Inf.
        """
        if not isinstance(ab_ratio, Dose):
            raise ValueError('ab_ratio must be type(Dose)')
        if not isinstance(nfx, int) and nfx < 1:
            raise ValueError('nfx must be an int value from 1..+inf')
        self.nfx = nfx
        self.ab_ratio = ab_ratio

    def suvival_fraction(self, dose: DoseArray, alpha: float) -> float:
        """
        It calculates the survival fraction after the delivery of dose in nfx fractions. It assumes that the delivered
        dose is homogeneous to the cell with alpha radiosensetivity.

        :param alpha: Cells radiosensetivity.
        :param dose: Physical dose array.
        :return: Survival fraction
        """

        if isinstance(dose, DoseArray):
            return np.exp(-alpha * self.eqd0(dose).data)

    def _is_different_units(self, total_dose: DoseArray, ab_ratio):
        return total_dose.unit != ab_ratio.unit

    def eqd0(self, total_dose: DoseArray) -> DoseArray:
        if not isinstance(total_dose, DoseArray):
            raise ValueError('total dose must be type DoseArray')

        if self._is_different_units(total_dose, self.ab_ratio):
            raise ValueError('total_dose units and ab_ratio units must be the same')

        eqd0 = total_dose.data * (1.0 + (total_dose.data / self.nfx / self.ab_ratio.value))
        return DoseArray.create(data=eqd0, unit=total_dose.unit, dose_type=DoseType.EQD0,
                                params_dict={'ab_ratio': self.ab_ratio})
