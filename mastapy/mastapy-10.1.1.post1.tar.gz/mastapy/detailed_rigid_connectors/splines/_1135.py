'''_1135.py

GBT3478SplineJointDesign
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.bearings.tolerances import _1388
from mastapy.detailed_rigid_connectors.splines import _1138
from mastapy._internal.python_net import python_net_import

_GBT3478_SPLINE_JOINT_DESIGN = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'GBT3478SplineJointDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('GBT3478SplineJointDesign',)


class GBT3478SplineJointDesign(_1138.ISO4156SplineJointDesign):
    '''GBT3478SplineJointDesign

    This is a mastapy class.
    '''

    TYPE = _GBT3478_SPLINE_JOINT_DESIGN
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GBT3478SplineJointDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def external_minimum_major_diameter(self) -> 'float':
        '''float: 'ExternalMinimumMajorDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExternalMinimumMajorDiameter

    @property
    def major_diameter_standard_tolerance_grade(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ITDesignation':
        '''enum_with_selected_value.EnumWithSelectedValue_ITDesignation: 'MajorDiameterStandardToleranceGrade' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_ITDesignation)(self.wrapped.MajorDiameterStandardToleranceGrade) if self.wrapped.MajorDiameterStandardToleranceGrade else None

    @major_diameter_standard_tolerance_grade.setter
    def major_diameter_standard_tolerance_grade(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ITDesignation.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_ITDesignation.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ITDesignation.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.MajorDiameterStandardToleranceGrade = value

    @property
    def minor_diameter_standard_tolerance_grade(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ITDesignation':
        '''enum_with_selected_value.EnumWithSelectedValue_ITDesignation: 'MinorDiameterStandardToleranceGrade' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_ITDesignation)(self.wrapped.MinorDiameterStandardToleranceGrade) if self.wrapped.MinorDiameterStandardToleranceGrade else None

    @minor_diameter_standard_tolerance_grade.setter
    def minor_diameter_standard_tolerance_grade(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ITDesignation.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_ITDesignation.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ITDesignation.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.MinorDiameterStandardToleranceGrade = value
