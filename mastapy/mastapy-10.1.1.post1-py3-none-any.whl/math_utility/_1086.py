'''_1086.py

TransformMatrix3D
'''


from typing import Optional

from mastapy._internal import constructor, conversion
from mastapy._internal.vector_3d import Vector3D
from mastapy._internal.tuple_with_name import TupleWithName
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_TRANSFORM_MATRIX_3D = python_net_import('SMT.MastaAPI.MathUtility', 'TransformMatrix3D')


__docformat__ = 'restructuredtext en'
__all__ = ('TransformMatrix3D',)


class TransformMatrix3D(_0.APIBase):
    '''TransformMatrix3D

    This is a mastapy class.
    '''

    TYPE = _TRANSFORM_MATRIX_3D

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TransformMatrix3D.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def is_identity(self) -> 'bool':
        '''bool: 'IsIdentity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsIdentity

    @property
    def x_axis(self) -> 'Vector3D':
        '''Vector3D: 'XAxis' is the original name of this property.'''

        value = conversion.pn_to_mp_vector3d(self.wrapped.XAxis)
        return value

    @x_axis.setter
    def x_axis(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.XAxis = value

    @property
    def y_axis(self) -> 'Vector3D':
        '''Vector3D: 'YAxis' is the original name of this property.'''

        value = conversion.pn_to_mp_vector3d(self.wrapped.YAxis)
        return value

    @y_axis.setter
    def y_axis(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.YAxis = value

    @property
    def z_axis(self) -> 'Vector3D':
        '''Vector3D: 'ZAxis' is the original name of this property.'''

        value = conversion.pn_to_mp_vector3d(self.wrapped.ZAxis)
        return value

    @z_axis.setter
    def z_axis(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.ZAxis = value

    @property
    def translation(self) -> 'Vector3D':
        '''Vector3D: 'Translation' is the original name of this property.'''

        value = conversion.pn_to_mp_vector3d(self.wrapped.Translation)
        return value

    @translation.setter
    def translation(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.Translation = value

    def transposed(self) -> 'TransformMatrix3D':
        ''' 'Transposed' is the original name of this method.

        Returns:
            mastapy.math_utility.TransformMatrix3D
        '''

        method_result = self.wrapped.Transposed()
        return constructor.new(TransformMatrix3D)(method_result) if method_result else None

    def rigid_inverse(self) -> 'TransformMatrix3D':
        ''' 'RigidInverse' is the original name of this method.

        Returns:
            mastapy.math_utility.TransformMatrix3D
        '''

        method_result = self.wrapped.RigidInverse()
        return constructor.new(TransformMatrix3D)(method_result) if method_result else None

    def has_rotation(self, tolerance: Optional['float'] = 0.0) -> 'bool':
        ''' 'HasRotation' is the original name of this method.

        Args:
            tolerance (float, optional)

        Returns:
            bool
        '''

        tolerance = float(tolerance)
        method_result = self.wrapped.HasRotation(tolerance if tolerance else 0.0)
        return method_result

    def has_translation(self, tolerance: Optional['float'] = 0.0) -> 'bool':
        ''' 'HasTranslation' is the original name of this method.

        Args:
            tolerance (float, optional)

        Returns:
            bool
        '''

        tolerance = float(tolerance)
        method_result = self.wrapped.HasTranslation(tolerance if tolerance else 0.0)
        return method_result

    def negated(self) -> 'TransformMatrix3D':
        ''' 'Negated' is the original name of this method.

        Returns:
            mastapy.math_utility.TransformMatrix3D
        '''

        method_result = self.wrapped.Negated()
        return constructor.new(TransformMatrix3D)(method_result) if method_result else None

    def transform_linear_and_angular_components(self, linear: 'Vector3D', angular: 'Vector3D') -> 'TupleWithName':
        ''' 'TransformLinearAndAngularComponents' is the original name of this method.

        Args:
            linear (Vector3D)
            angular (Vector3D)

        Returns:
            TupleWithName
        '''

        linear = conversion.mp_to_pn_vector3d(linear)
        angular = conversion.mp_to_pn_vector3d(angular)
        return conversion.pn_to_mp_tuple_with_name(self.wrapped.TransformLinearAndAngularComponents(linear, angular), (conversion.pn_to_mp_vector3d, conversion.pn_to_mp_vector3d))

    def rotate(self, angular: 'Vector3D') -> 'Vector3D':
        ''' 'Rotate' is the original name of this method.

        Args:
            angular (Vector3D)

        Returns:
            Vector3D
        '''

        angular = conversion.mp_to_pn_vector3d(angular)
        return conversion.pn_to_mp_vector3d(self.wrapped.Rotate(angular))

    def transform(self, linear: 'Vector3D') -> 'Vector3D':
        ''' 'Transform' is the original name of this method.

        Args:
            linear (Vector3D)

        Returns:
            Vector3D
        '''

        linear = conversion.mp_to_pn_vector3d(linear)
        return conversion.pn_to_mp_vector3d(self.wrapped.Transform(linear))
