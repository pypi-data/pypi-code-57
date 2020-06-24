'''_1248.py

Complex
'''


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy import _1
from mastapy.utility.units_and_measurements import _1035
from mastapy._internal.python_net import python_net_import

_COMPLEX = python_net_import('SMT.MastaAPI.MathUtility.MeasuredVectors', 'Complex')


__docformat__ = 'restructuredtext en'
__all__ = ('Complex',)


TMeasurement = TypeVar('TMeasurement', bound='_1035.MeasurementBase')


class Complex(_1.APIBase, Generic[TMeasurement]):
    '''Complex

    This is a mastapy class.

    Generic Types:
        TMeasurement
    '''

    TYPE = _COMPLEX
    __hash__ = None

    def __init__(self, instance_to_wrap: 'Complex.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def magnitude(self) -> 'float':
        '''float: 'Magnitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Magnitude

    @property
    def phase(self) -> 'float':
        '''float: 'Phase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Phase

    @property
    def real(self) -> 'float':
        '''float: 'Real' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Real

    @property
    def imaginary(self) -> 'float':
        '''float: 'Imaginary' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Imaginary
