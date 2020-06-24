'''_649.py

PlungeShaverGeneration
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _708
from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _656, _642
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PLUNGE_SHAVER_GENERATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving', 'PlungeShaverGeneration')


__docformat__ = 'restructuredtext en'
__all__ = ('PlungeShaverGeneration',)


class PlungeShaverGeneration(_1.APIBase):
    '''PlungeShaverGeneration

    This is a mastapy class.
    '''

    TYPE = _PLUNGE_SHAVER_GENERATION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlungeShaverGeneration.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def shaft_angle_unsigned(self) -> 'float':
        '''float: 'ShaftAngleUnsigned' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaftAngleUnsigned

    @property
    def gear_start_of_active_profile_diameter(self) -> 'float':
        '''float: 'GearStartOfActiveProfileDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GearStartOfActiveProfileDiameter

    @property
    def manufactured_end_of_active_profile_diameter(self) -> 'float':
        '''float: 'ManufacturedEndOfActiveProfileDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ManufacturedEndOfActiveProfileDiameter

    @property
    def manufactured_start_of_active_profile_diameter(self) -> 'float':
        '''float: 'ManufacturedStartOfActiveProfileDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ManufacturedStartOfActiveProfileDiameter

    @property
    def crossed_axis_calculation_details(self) -> '_708.CrossedAxisCylindricalGearPairLineContact':
        '''CrossedAxisCylindricalGearPairLineContact: 'CrossedAxisCalculationDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_708.CrossedAxisCylindricalGearPairLineContact)(self.wrapped.CrossedAxisCalculationDetails) if self.wrapped.CrossedAxisCalculationDetails else None

    @property
    def points_of_interest_on_the_shaver(self) -> 'List[_656.ShaverPointOfInterest]':
        '''List[ShaverPointOfInterest]: 'PointsOfInterestOnTheShaver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointsOfInterestOnTheShaver, constructor.new(_656.ShaverPointOfInterest))
        return value

    @property
    def calculation_errors(self) -> 'List[_642.CalculationError]':
        '''List[CalculationError]: 'CalculationErrors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CalculationErrors, constructor.new(_642.CalculationError))
        return value
