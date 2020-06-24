'''_1837.py

AlignmentUsingAxialNodePositions
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.math_utility import _1213
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ALIGNMENT_USING_AXIAL_NODE_POSITIONS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'AlignmentUsingAxialNodePositions')


__docformat__ = 'restructuredtext en'
__all__ = ('AlignmentUsingAxialNodePositions',)


class AlignmentUsingAxialNodePositions(_1.APIBase):
    '''AlignmentUsingAxialNodePositions

    This is a mastapy class.
    '''

    TYPE = _ALIGNMENT_USING_AXIAL_NODE_POSITIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AlignmentUsingAxialNodePositions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def rotation_angle(self) -> 'float':
        '''float: 'RotationAngle' is the original name of this property.'''

        return self.wrapped.RotationAngle

    @rotation_angle.setter
    def rotation_angle(self, value: 'float'):
        self.wrapped.RotationAngle = float(value) if value else 0.0

    @property
    def fe_axis_for_angle_alignment(self) -> 'enum_with_selected_value.EnumWithSelectedValue_AlignmentAxis':
        '''enum_with_selected_value.EnumWithSelectedValue_AlignmentAxis: 'FEAxisForAngleAlignment' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_AlignmentAxis)(self.wrapped.FEAxisForAngleAlignment) if self.wrapped.FEAxisForAngleAlignment else None

    @fe_axis_for_angle_alignment.setter
    def fe_axis_for_angle_alignment(self, value: 'enum_with_selected_value.EnumWithSelectedValue_AlignmentAxis.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_AlignmentAxis.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_AlignmentAxis.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.FEAxisForAngleAlignment = value
