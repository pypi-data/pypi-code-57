'''_1215.py

CoordinateSystem3D
'''


from mastapy._internal import constructor, conversion
from mastapy._internal.vector_3d import Vector3D
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_COORDINATE_SYSTEM_3D = python_net_import('SMT.MastaAPI.MathUtility', 'CoordinateSystem3D')


__docformat__ = 'restructuredtext en'
__all__ = ('CoordinateSystem3D',)


class CoordinateSystem3D(_1.APIBase):
    '''CoordinateSystem3D

    This is a mastapy class.
    '''

    TYPE = _COORDINATE_SYSTEM_3D
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoordinateSystem3D.TYPE'):
        super().__init__(instance_to_wrap)

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
    def translation(self) -> 'Vector3D':
        '''Vector3D: 'Translation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.Translation)
        return value
