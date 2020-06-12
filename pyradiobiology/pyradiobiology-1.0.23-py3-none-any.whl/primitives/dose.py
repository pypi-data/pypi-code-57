from enum import Enum
from math import isnan


class DoseUnit(Enum):
    def __eq__(self, o: object) -> bool:
        if not isinstance(o, DoseUnit):
            return False
        return self.value == o.value

    def __neq__(self, o: object) -> bool:
        return not self.__eq__()

    GY = 1
    CGY = 2
    PERCENTAGE = 3


class DoseType(Enum):
    def __eq__(self, o: object) -> bool:
        if not isinstance(o, DoseType):
            return False
        return self.value == o.value

    def __neq__(self, o: object) -> bool:
        return not self.__eq__()

    PHYSICAL_DOSE = 1
    EQD0 = 2
    EQD2 = 3


class Dose():
    def __init__(self, value, unit=DoseUnit.GY, dose_type=DoseType.PHYSICAL_DOSE) -> None:
        """
        :type dose_type: Type of dose: PHYICAL_DOSE, EQD0, or EQD2
        :type value: the dose value
        :type unit: the dose unit in 'Gy', 'cGy', '%'
        """

        self._validate_input_or_throw_exception(value, unit)
        self.dose_type = dose_type
        self.value = value
        self.unit = unit

    def _validate_input_or_throw_exception(self, value, unit):
        if not isinstance(value, (float, int)):
            raise ValueError("Dose must be a number")
        if value < 0.0:
            raise ValueError("Dose cannot be negative.")
        if not isinstance(unit, DoseUnit):
            raise ValueError(f"unit must be type of DoseUnit. Current type is {type(unit)}")

    def __repr__(self) -> str:
        if isnan(self.value):
            return "N/A"
        return f"{self.value} {self._unit_as_string()}"

    def _unit_as_string(self):
        if self.unit == DoseUnit.GY:
            return 'Gy'
        if self.unit == DoseUnit.CGY:
            return 'cGy'
        if self.unit == DoseUnit.PERCENTAGE:
            return '%'
        return 'N/A'

    @classmethod
    def gy(cls, value, dose_type=DoseType.PHYSICAL_DOSE):
        return cls(value, DoseUnit.GY, dose_type)

    @classmethod
    def cgy(cls, value, dose_type=DoseType.PHYSICAL_DOSE):
        return cls(value, DoseUnit.CGY, dose_type)

    @classmethod
    def percent(cls, value):
        return cls(value, DoseUnit.PERCENTAGE)

    def __add__(self, other):
        if isinstance(other, Dose):
            if self.unit == other.unit:
                return Dose(self.value + other.value, self.unit)
            else:
                raise ValueError("Cannot add dose with different units.")

    def __radd__(self, other):
        return self.__add__(other)

    def __float__(self):
        return self.value

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Dose):
            return False
        if o.unit == self.unit and \
                o.value == self.value and \
                o.dose_type == self.dose_type:
            return True

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)
