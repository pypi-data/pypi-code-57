'''_1912.py

Component
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy.scripting import _712
from mastapy._internal.vector_3d import Vector3D
from mastapy.system_model.connections_and_sockets import _1762, _1779
from mastapy.system_model.part_model import _1931
from mastapy._internal.python_net import python_net_import

_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')


__docformat__ = 'restructuredtext en'
__all__ = ('Component',)


class Component(_1931.Part):
    '''Component

    This is a mastapy class.
    '''

    TYPE = _COMPONENT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'Component.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def length(self) -> 'float':
        '''float: 'Length' is the original name of this property.'''

        return self.wrapped.Length

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value else 0.0

    @property
    def polar_inertia_for_synchroniser_sizing_only(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'PolarInertiaForSynchroniserSizingOnly' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.PolarInertiaForSynchroniserSizingOnly) if self.wrapped.PolarInertiaForSynchroniserSizingOnly else None

    @polar_inertia_for_synchroniser_sizing_only.setter
    def polar_inertia_for_synchroniser_sizing_only(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.PolarInertiaForSynchroniserSizingOnly = value

    @property
    def polar_inertia(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'PolarInertia' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.PolarInertia) if self.wrapped.PolarInertia else None

    @polar_inertia.setter
    def polar_inertia(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.PolarInertia = value

    @property
    def transverse_inertia(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TransverseInertia' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TransverseInertia) if self.wrapped.TransverseInertia else None

    @transverse_inertia.setter
    def transverse_inertia(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.TransverseInertia = value

    @property
    def x_axis(self) -> 'str':
        '''str: 'XAxis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.XAxis

    @property
    def y_axis(self) -> 'str':
        '''str: 'YAxis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.YAxis

    @property
    def z_axis(self) -> 'str':
        '''str: 'ZAxis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ZAxis

    @property
    def translation(self) -> 'str':
        '''str: 'Translation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Translation

    @property
    def reason_mass_properties_are_unknown(self) -> 'str':
        '''str: 'ReasonMassPropertiesAreUnknown' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReasonMassPropertiesAreUnknown

    @property
    def reason_mass_properties_are_zero(self) -> 'str':
        '''str: 'ReasonMassPropertiesAreZero' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReasonMassPropertiesAreZero

    @property
    def additional_modal_damping_ratio(self) -> 'float':
        '''float: 'AdditionalModalDampingRatio' is the original name of this property.'''

        return self.wrapped.AdditionalModalDampingRatio

    @additional_modal_damping_ratio.setter
    def additional_modal_damping_ratio(self, value: 'float'):
        self.wrapped.AdditionalModalDampingRatio = float(value) if value else 0.0

    @property
    def twod_drawing_full_model(self) -> '_712.SMTBitmap':
        '''SMTBitmap: 'TwoDDrawingFullModel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_712.SMTBitmap)(self.wrapped.TwoDDrawingFullModel) if self.wrapped.TwoDDrawingFullModel else None

    @property
    def coordinate_system_euler_angles(self) -> 'Vector3D':
        '''Vector3D: 'CoordinateSystemEulerAngles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.CoordinateSystemEulerAngles)
        return value

    @property
    def position(self) -> 'Vector3D':
        '''Vector3D: 'Position' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.Position)
        return value

    @property
    def component_connections(self) -> 'List[_1762.ComponentConnection]':
        '''List[ComponentConnection]: 'ComponentConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentConnections, constructor.new(_1762.ComponentConnection))
        return value

    @property
    def translation_vector(self) -> 'Vector3D':
        '''Vector3D: 'TranslationVector' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.TranslationVector)
        return value

    @property
    def x_axis_vector(self) -> 'Vector3D':
        '''Vector3D: 'XAxisVector' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.XAxisVector)
        return value

    @property
    def y_axis_vector(self) -> 'Vector3D':
        '''Vector3D: 'YAxisVector' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.YAxisVector)
        return value

    @property
    def z_axis_vector(self) -> 'Vector3D':
        '''Vector3D: 'ZAxisVector' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.ZAxisVector)
        return value

    def move_along_axis(self, delta: 'float'):
        ''' 'MoveAlongAxis' is the original name of this method.

        Args:
            delta (float)
        '''

        delta = float(delta)
        self.wrapped.MoveAlongAxis(delta if delta else 0.0)

    def set_position_of_component_and_connected_components(self, position: 'Vector3D') -> '_1779.RealignmentResult':
        ''' 'SetPositionOfComponentAndConnectedComponents' is the original name of this method.

        Args:
            position (Vector3D)

        Returns:
            mastapy.system_model.connections_and_sockets.RealignmentResult
        '''

        position = conversion.mp_to_pn_vector3d(position)
        method_result = self.wrapped.SetPositionOfComponentAndConnectedComponents(position)
        return constructor.new(_1779.RealignmentResult)(method_result) if method_result else None

    def move_all_concentric_parts_radially(self, delta_x: 'float', delta_y: 'float') -> 'bool':
        ''' 'MoveAllConcentricPartsRadially' is the original name of this method.

        Args:
            delta_x (float)
            delta_y (float)

        Returns:
            bool
        '''

        delta_x = float(delta_x)
        delta_y = float(delta_y)
        method_result = self.wrapped.MoveAllConcentricPartsRadially(delta_x if delta_x else 0.0, delta_y if delta_y else 0.0)
        return method_result
