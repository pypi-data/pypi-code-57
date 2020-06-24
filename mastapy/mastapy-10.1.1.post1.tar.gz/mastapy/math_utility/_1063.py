'''_1063.py

CoordinateSystem3D
'''


from mastapy._internal.vector_3d import Vector3D
from mastapy._internal import constructor, conversion
from mastapy.math_utility import _1068, _1086
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_COORDINATE_SYSTEM_3D = python_net_import('SMT.MastaAPI.MathUtility', 'CoordinateSystem3D')


__docformat__ = 'restructuredtext en'
__all__ = ('CoordinateSystem3D',)


class CoordinateSystem3D(_0.APIBase):
    '''CoordinateSystem3D

    This is a mastapy class.
    '''

    TYPE = _COORDINATE_SYSTEM_3D

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoordinateSystem3D.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def origin(self) -> 'Vector3D':
        '''Vector3D: 'Origin' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.Origin)
        return value

    @property
    def x_axis(self) -> 'Vector3D':
        '''Vector3D: 'XAxis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.XAxis)
        return value

    @property
    def y_axis(self) -> 'Vector3D':
        '''Vector3D: 'YAxis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.YAxis)
        return value

    @property
    def z_axis(self) -> 'Vector3D':
        '''Vector3D: 'ZAxis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.ZAxis)
        return value

    def rotated_about_axis(self, axis: 'Vector3D', angle: 'float') -> 'CoordinateSystem3D':
        ''' 'RotatedAboutAxis' is the original name of this method.

        Args:
            axis (Vector3D)
            angle (float)

        Returns:
            mastapy.math_utility.CoordinateSystem3D
        '''

        axis = conversion.mp_to_pn_vector3d(axis)
        angle = float(angle)
        method_result = self.wrapped.RotatedAboutAxis(axis, angle if angle else 0.0)
        return constructor.new(CoordinateSystem3D)(method_result) if method_result else None

    def axis(self, degree_of_freedom: '_1068.DegreesOfFreedom') -> 'Vector3D':
        ''' 'Axis' is the original name of this method.

        Args:
            degree_of_freedom (mastapy.math_utility.DegreesOfFreedom)

        Returns:
            Vector3D
        '''

        degree_of_freedom = conversion.mp_to_pn_enum(degree_of_freedom)
        return conversion.pn_to_mp_vector3d(self.wrapped.Axis(degree_of_freedom))

    def transform_to_world_from_this(self) -> '_1086.TransformMatrix3D':
        ''' 'TransformToWorldFromThis' is the original name of this method.

        Returns:
            mastapy.math_utility.TransformMatrix3D
        '''

        method_result = self.wrapped.TransformToWorldFromThis()
        return constructor.new(_1086.TransformMatrix3D)(method_result) if method_result else None

    def transform_from_world_to_this(self) -> '_1086.TransformMatrix3D':
        ''' 'TransformFromWorldToThis' is the original name of this method.

        Returns:
            mastapy.math_utility.TransformMatrix3D
        '''

        method_result = self.wrapped.TransformFromWorldToThis()
        return constructor.new(_1086.TransformMatrix3D)(method_result) if method_result else None

    def transformed_by(self, transform: '_1086.TransformMatrix3D') -> 'CoordinateSystem3D':
        ''' 'TransformedBy' is the original name of this method.

        Args:
            transform (mastapy.math_utility.TransformMatrix3D)

        Returns:
            mastapy.math_utility.CoordinateSystem3D
        '''

        method_result = self.wrapped.TransformedBy(transform.wrapped if transform else None)
        return constructor.new(CoordinateSystem3D)(method_result) if method_result else None

    def without_translation(self) -> 'CoordinateSystem3D':
        ''' 'WithoutTranslation' is the original name of this method.

        Returns:
            mastapy.math_utility.CoordinateSystem3D
        '''

        method_result = self.wrapped.WithoutTranslation()
        return constructor.new(CoordinateSystem3D)(method_result) if method_result else None
