'''_1252.py

TwoDVectorPolar
'''


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy import _1
from mastapy.utility.units_and_measurements import _1035
from mastapy._internal.python_net import python_net_import

_TWOD_VECTOR_POLAR = python_net_import('SMT.MastaAPI.MathUtility.MeasuredVectors', 'TwoDVectorPolar')


__docformat__ = 'restructuredtext en'
__all__ = ('TwoDVectorPolar',)


TMeasurement = TypeVar('TMeasurement', bound='_1035.MeasurementBase')


class TwoDVectorPolar(_1.APIBase, Generic[TMeasurement]):
    '''TwoDVectorPolar

    This is a mastapy class.

    Generic Types:
        TMeasurement
    '''

    TYPE = _TWOD_VECTOR_POLAR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TwoDVectorPolar.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def radius(self) -> 'float':
        '''float: 'Radius' is the original name of this property.'''

        return self.wrapped.Radius

    @radius.setter
    def radius(self, value: 'float'):
        self.wrapped.Radius = float(value) if value else 0.0

    @property
    def theta(self) -> 'float':
        '''float: 'Theta' is the original name of this property.'''

        return self.wrapped.Theta

    @theta.setter
    def theta(self, value: 'float'):
        self.wrapped.Theta = float(value) if value else 0.0

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
