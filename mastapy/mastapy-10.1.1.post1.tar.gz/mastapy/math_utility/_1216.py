'''_1216.py

CoordinateSystemEditor
'''


from typing import Callable

from mastapy._internal import constructor, conversion
from mastapy.math_utility import _1231, _1217, _1215
from mastapy._internal.implicit import enum_with_selected_value
from mastapy._internal.vector_3d import Vector3D
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_COORDINATE_SYSTEM_EDITOR = python_net_import('SMT.MastaAPI.MathUtility', 'CoordinateSystemEditor')


__docformat__ = 'restructuredtext en'
__all__ = ('CoordinateSystemEditor',)


class CoordinateSystemEditor(_1.APIBase):
    '''CoordinateSystemEditor

    This is a mastapy class.
    '''

    TYPE = _COORDINATE_SYSTEM_EDITOR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoordinateSystemEditor.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def apply_rotation(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ApplyRotation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ApplyRotation

    @property
    def rotation_angle(self) -> 'float':
        '''float: 'RotationAngle' is the original name of this property.'''

        return self.wrapped.RotationAngle

    @rotation_angle.setter
    def rotation_angle(self, value: 'float'):
        self.wrapped.RotationAngle = float(value) if value else 0.0

    @property
    def rotation_axis(self) -> '_1231.RotationAxis':
        '''RotationAxis: 'RotationAxis' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.RotationAxis)
        return constructor.new(_1231.RotationAxis)(value) if value else None

    @rotation_axis.setter
    def rotation_axis(self, value: '_1231.RotationAxis'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RotationAxis = value

    @property
    def coordinate_system_for_rotation(self) -> 'enum_with_selected_value.EnumWithSelectedValue_CoordinateSystemForRotation':
        '''enum_with_selected_value.EnumWithSelectedValue_CoordinateSystemForRotation: 'CoordinateSystemForRotation' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_CoordinateSystemForRotation)(self.wrapped.CoordinateSystemForRotation) if self.wrapped.CoordinateSystemForRotation else None

    @coordinate_system_for_rotation.setter
    def coordinate_system_for_rotation(self, value: 'enum_with_selected_value.EnumWithSelectedValue_CoordinateSystemForRotation.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_CoordinateSystemForRotation.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CoordinateSystemForRotation.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.CoordinateSystemForRotation = value

    @property
    def apply_changes(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ApplyChanges' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ApplyChanges

    @property
    def cancel_changes(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CancelChanges' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CancelChanges

    @property
    def align_to_world_coordinate_system(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AlignToWorldCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AlignToWorldCoordinateSystem

    @property
    def move_to_origin(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'MoveToOrigin' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MoveToOrigin

    @property
    def show_preview(self) -> 'bool':
        '''bool: 'ShowPreview' is the original name of this property.'''

        return self.wrapped.ShowPreview

    @show_preview.setter
    def show_preview(self, value: 'bool'):
        self.wrapped.ShowPreview = bool(value) if value else False

    @property
    def create_datum_from_manual_alignment(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CreateDatumFromManualAlignment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateDatumFromManualAlignment

    @property
    def modified_coordinate_system(self) -> '_1215.CoordinateSystem3D':
        '''CoordinateSystem3D: 'ModifiedCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1215.CoordinateSystem3D)(self.wrapped.ModifiedCoordinateSystem) if self.wrapped.ModifiedCoordinateSystem else None

    @property
    def translation(self) -> 'Vector3D':
        '''Vector3D: 'Translation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.Translation)
        return value

    @property
    def specified_rotation_axis(self) -> 'Vector3D':
        '''Vector3D: 'SpecifiedRotationAxis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.SpecifiedRotationAxis)
        return value
