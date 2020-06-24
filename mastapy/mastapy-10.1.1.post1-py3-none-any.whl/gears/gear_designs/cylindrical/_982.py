'''_982.py

CylindricalGearToothThicknessSpecification
'''


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy import _1
from mastapy.utility.units_and_measurements import _1035
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_TOOTH_THICKNESS_SPECIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearToothThicknessSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearToothThicknessSpecification',)


TMeasurement = TypeVar('TMeasurement', bound='_1035.MeasurementBase')


class CylindricalGearToothThicknessSpecification(_1.APIBase, Generic[TMeasurement]):
    '''CylindricalGearToothThicknessSpecification

    This is a mastapy class.

    Generic Types:
        TMeasurement
    '''

    TYPE = _CYLINDRICAL_GEAR_TOOTH_THICKNESS_SPECIFICATION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearToothThicknessSpecification.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def thickness_measurement_type(self) -> 'str':
        '''str: 'ThicknessMeasurementType' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ThicknessMeasurementType

    @property
    def minimum_thickness_reduction(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumThicknessReduction' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumThicknessReduction) if self.wrapped.MinimumThicknessReduction else None

    @minimum_thickness_reduction.setter
    def minimum_thickness_reduction(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.MinimumThicknessReduction = value

    @property
    def tolerance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Tolerance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Tolerance) if self.wrapped.Tolerance else None

    @tolerance.setter
    def tolerance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.Tolerance = value

    @property
    def nominal_zero_backlash(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'NominalZeroBacklash' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.NominalZeroBacklash) if self.wrapped.NominalZeroBacklash else None

    @nominal_zero_backlash.setter
    def nominal_zero_backlash(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.NominalZeroBacklash = value

    @property
    def maximum_metal(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MaximumMetal' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MaximumMetal) if self.wrapped.MaximumMetal else None

    @maximum_metal.setter
    def maximum_metal(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.MaximumMetal = value

    @property
    def average_mean_metal(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AverageMeanMetal' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AverageMeanMetal) if self.wrapped.AverageMeanMetal else None

    @average_mean_metal.setter
    def average_mean_metal(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.AverageMeanMetal = value

    @property
    def minimum_metal(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumMetal' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumMetal) if self.wrapped.MinimumMetal else None

    @minimum_metal.setter
    def minimum_metal(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.MinimumMetal = value

    @property
    def upper_allowance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'UpperAllowance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.UpperAllowance) if self.wrapped.UpperAllowance else None

    @upper_allowance.setter
    def upper_allowance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.UpperAllowance = value

    @property
    def lower_allowance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'LowerAllowance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.LowerAllowance) if self.wrapped.LowerAllowance else None

    @lower_allowance.setter
    def lower_allowance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.LowerAllowance = value

    @property
    def average_allowance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AverageAllowance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AverageAllowance) if self.wrapped.AverageAllowance else None

    @average_allowance.setter
    def average_allowance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.AverageAllowance = value
