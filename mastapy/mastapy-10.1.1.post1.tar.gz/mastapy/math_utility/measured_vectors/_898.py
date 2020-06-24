'''_898.py

Vector2D
'''


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy import _1
from mastapy.utility.units_and_measurements import _1034
from mastapy._internal.python_net import python_net_import

_VECTOR_2D = python_net_import('SMT.MastaAPI.MathUtility.MeasuredVectors', 'Vector2D')


__docformat__ = 'restructuredtext en'
__all__ = ('Vector2D',)


TMeasurement = TypeVar('TMeasurement', bound='_1034.MeasurementBase')


class Vector2D(_1.APIBase, Generic[TMeasurement]):
    '''Vector2D

    This is a mastapy class.

    Generic Types:
        TMeasurement
    '''

    TYPE = _VECTOR_2D
    __hash__ = None

    def __init__(self, instance_to_wrap: 'Vector2D.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def x(self) -> 'float':
        '''float: 'X' is the original name of this property.'''

        return self.wrapped.X

    @x.setter
    def x(self, value: 'float'):
        self.wrapped.X = float(value) if value else 0.0

    @property
    def y(self) -> 'float':
        '''float: 'Y' is the original name of this property.'''

        return self.wrapped.Y

    @y.setter
    def y(self, value: 'float'):
        self.wrapped.Y = float(value) if value else 0.0

    @property
    def magnitude(self) -> 'float':
        '''float: 'Magnitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Magnitude
