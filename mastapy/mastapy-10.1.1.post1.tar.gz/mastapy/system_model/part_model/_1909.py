'''_1909.py

BearingRaceMountingOptions
'''


from mastapy._internal.implicit import enum_with_selected_value
from mastapy.bearings.bearing_results import _1536, _1535
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_BEARING_RACE_MOUNTING_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'BearingRaceMountingOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingRaceMountingOptions',)


class BearingRaceMountingOptions(_1.APIBase):
    '''BearingRaceMountingOptions

    This is a mastapy class.
    '''

    TYPE = _BEARING_RACE_MOUNTING_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingRaceMountingOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def radial_mounting(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType':
        '''enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType: 'RadialMounting' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType)(self.wrapped.RadialMounting) if self.wrapped.RadialMounting else None

    @radial_mounting.setter
    def radial_mounting(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.RadialMounting = value

    @property
    def axial_mounting(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType':
        '''enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType: 'AxialMounting' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType)(self.wrapped.AxialMounting) if self.wrapped.AxialMounting else None

    @axial_mounting.setter
    def axial_mounting(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.AxialMounting = value

    @property
    def radial_mounting_clearance(self) -> 'float':
        '''float: 'RadialMountingClearance' is the original name of this property.'''

        return self.wrapped.RadialMountingClearance

    @radial_mounting_clearance.setter
    def radial_mounting_clearance(self, value: 'float'):
        self.wrapped.RadialMountingClearance = float(value) if value else 0.0

    @property
    def left_axial_mounting_clearance(self) -> 'float':
        '''float: 'LeftAxialMountingClearance' is the original name of this property.'''

        return self.wrapped.LeftAxialMountingClearance

    @left_axial_mounting_clearance.setter
    def left_axial_mounting_clearance(self, value: 'float'):
        self.wrapped.LeftAxialMountingClearance = float(value) if value else 0.0

    @property
    def right_axial_mounting_clearance(self) -> 'float':
        '''float: 'RightAxialMountingClearance' is the original name of this property.'''

        return self.wrapped.RightAxialMountingClearance

    @right_axial_mounting_clearance.setter
    def right_axial_mounting_clearance(self, value: 'float'):
        self.wrapped.RightAxialMountingClearance = float(value) if value else 0.0

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name
