'''_650.py

PlungeShaverInputsAndMicroGeometry
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _646, _645, _653
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PLUNGE_SHAVER_INPUTS_AND_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving', 'PlungeShaverInputsAndMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('PlungeShaverInputsAndMicroGeometry',)


class PlungeShaverInputsAndMicroGeometry(_1.APIBase):
    '''PlungeShaverInputsAndMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _PLUNGE_SHAVER_INPUTS_AND_MICRO_GEOMETRY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlungeShaverInputsAndMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def do_both_flanks_have_the_same_micro_geometry(self) -> 'bool':
        '''bool: 'DoBothFlanksHaveTheSameMicroGeometry' is the original name of this property.'''

        return self.wrapped.DoBothFlanksHaveTheSameMicroGeometry

    @do_both_flanks_have_the_same_micro_geometry.setter
    def do_both_flanks_have_the_same_micro_geometry(self, value: 'bool'):
        self.wrapped.DoBothFlanksHaveTheSameMicroGeometry = bool(value) if value else False

    @property
    def micro_geometry_source(self) -> 'enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionType':
        '''enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionType: 'MicroGeometrySource' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionType)(self.wrapped.MicroGeometrySource) if self.wrapped.MicroGeometrySource else None

    @micro_geometry_source.setter
    def micro_geometry_source(self, value: 'enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionType.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionType.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionType.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.MicroGeometrySource = value

    @property
    def profile_measurement_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod':
        '''enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod: 'ProfileMeasurementMethod' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod)(self.wrapped.ProfileMeasurementMethod) if self.wrapped.ProfileMeasurementMethod else None

    @profile_measurement_method.setter
    def profile_measurement_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.ProfileMeasurementMethod = value

    @property
    def lead_measurement_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod':
        '''enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod: 'LeadMeasurementMethod' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod)(self.wrapped.LeadMeasurementMethod) if self.wrapped.LeadMeasurementMethod else None

    @lead_measurement_method.setter
    def lead_measurement_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MicroGeometryDefinitionMethod.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.LeadMeasurementMethod = value

    @property
    def number_of_points_of_interest(self) -> 'int':
        '''int: 'NumberOfPointsOfInterest' is the original name of this property.'''

        return self.wrapped.NumberOfPointsOfInterest

    @number_of_points_of_interest.setter
    def number_of_points_of_interest(self, value: 'int'):
        self.wrapped.NumberOfPointsOfInterest = int(value) if value else 0

    @property
    def points_of_interest_left_flank(self) -> 'List[_653.PointOfInterest]':
        '''List[PointOfInterest]: 'PointsOfInterestLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointsOfInterestLeftFlank, constructor.new(_653.PointOfInterest))
        return value

    @property
    def points_of_interest_right_flank(self) -> 'List[_653.PointOfInterest]':
        '''List[PointOfInterest]: 'PointsOfInterestRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointsOfInterestRightFlank, constructor.new(_653.PointOfInterest))
        return value
