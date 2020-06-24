'''_788.py

ShavingDynamicsCalculationForDesignedGears
'''


from typing import List, Generic, TypeVar

from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _560
from mastapy._internal.python_net import python_net_import
from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _785, _782, _787, _786
)

_REPORTING_OVERRIDABLE = python_net_import('SMT.MastaAPI.Utility.Property', 'ReportingOverridable')
_SHAVING_DYNAMICS_CALCULATION_FOR_DESIGNED_GEARS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'ShavingDynamicsCalculationForDesignedGears')


__docformat__ = 'restructuredtext en'
__all__ = ('ShavingDynamicsCalculationForDesignedGears',)


T = TypeVar('T', bound='_786.ShavingDynamics')


class ShavingDynamicsCalculationForDesignedGears(_787.ShavingDynamicsCalculation['T'], Generic[T]):
    '''ShavingDynamicsCalculationForDesignedGears

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _SHAVING_DYNAMICS_CALCULATION_FOR_DESIGNED_GEARS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShavingDynamicsCalculationForDesignedGears.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def selected_redressing(self) -> 'list_with_selected_item.ListWithSelectedItem_T':
        '''list_with_selected_item.ListWithSelectedItem_T: 'SelectedRedressing' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_T)(self.wrapped.SelectedRedressing) if self.wrapped.SelectedRedressing else None

    @selected_redressing.setter
    def selected_redressing(self, value: 'list_with_selected_item.ListWithSelectedItem_T.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_T.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_T.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.SelectedRedressing = value

    @property
    def start_of_shaving_profile(self) -> '_560.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'StartOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_560.CylindricalGearProfileMeasurement)(self.wrapped.StartOfShavingProfile.Value) if self.wrapped.StartOfShavingProfile.Value else None

    @property
    def end_of_shaving_profile(self) -> '_560.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'EndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_560.CylindricalGearProfileMeasurement)(self.wrapped.EndOfShavingProfile.Value) if self.wrapped.EndOfShavingProfile.Value else None

    @property
    def redressing(self) -> '_785.ShaverRedressing[T]':
        '''ShaverRedressing[T]: 'Redressing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_785.ShaverRedressing)[T](self.wrapped.Redressing) if self.wrapped.Redressing else None

    @property
    def redressing_settings(self) -> 'List[_782.RedressingSettings[T]]':
        '''List[RedressingSettings[T]]: 'RedressingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RedressingSettings, constructor.new(_782.RedressingSettings)[T])
        return value
