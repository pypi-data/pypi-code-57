'''_1986.py

BearingRaceMountingOptions
'''


from mastapy._internal.implicit import enum_with_selected_value
from mastapy.bearings.bearing_results import _1584, _1583
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_BEARING_RACE_MOUNTING_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'BearingRaceMountingOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingRaceMountingOptions',)


class BearingRaceMountingOptions(_0.APIBase):
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

        value = enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.RadialMounting, value) if self.wrapped.RadialMounting else None

    @radial_mounting.setter
    def radial_mounting(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.RadialMounting = value

    @property
    def axial_mounting(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType':
        '''enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType: 'AxialMounting' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.AxialMounting, value) if self.wrapped.AxialMounting else None

    @axial_mounting.setter
    def axial_mounting(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.AxialMounting = value

    @property
    def radial_mounting_clearance(self) -> 'float':
        '''float: 'RadialMountingClearance' is the original name of this property.'''

        return self.wrapped.RadialMountingClearance

    @radial_mounting_clearance.setter
    def radial_mounting_clearance(self, value: 'float'):
        self.wrapped.RadialMountingClearance = float(value) if value else 0.0

    @property
    def radial_clearance_contact_stiffness(self) -> 'float':
        '''float: 'RadialClearanceContactStiffness' is the original name of this property.'''

        return self.wrapped.RadialClearanceContactStiffness

    @radial_clearance_contact_stiffness.setter
    def radial_clearance_contact_stiffness(self, value: 'float'):
        self.wrapped.RadialClearanceContactStiffness = float(value) if value else 0.0

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
