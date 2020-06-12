import numpy as np
from .dose import *

class DoseArray():

    def __init__(self, data, unit, dose_type=DoseType.PHYSICAL_DOSE, params_dict={}):
        self.unit = unit
        self.data = np.array(data)
        self.dose_type = dose_type
        self.param_dict = params_dict

    def __repr__(self) -> str:
        return f"data={self.data}, unit={self.unit}, dose_type={self.dose_type}"

    @classmethod
    def create(cls, data=[], unit=DoseUnit.GY, dose_type=DoseType.PHYSICAL_DOSE, params_dict={}):
        return cls(data, unit, dose_type, params_dict)
