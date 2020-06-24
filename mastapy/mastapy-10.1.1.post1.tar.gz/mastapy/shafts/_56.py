'''_56.py

ShaftProfilePoint
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy.shafts import _38
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SHAFT_PROFILE_POINT = python_net_import('SMT.MastaAPI.Shafts', 'ShaftProfilePoint')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftProfilePoint',)


class ShaftProfilePoint(_1.APIBase):
    '''ShaftProfilePoint

    This is a mastapy class.
    '''

    TYPE = _SHAFT_PROFILE_POINT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftProfilePoint.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def offset(self) -> 'float':
        '''float: 'Offset' is the original name of this property.'''

        return self.wrapped.Offset

    @offset.setter
    def offset(self, value: 'float'):
        self.wrapped.Offset = float(value) if value else 0.0

    @property
    def delete(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Delete' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Delete

    @property
    def insert(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Insert' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Insert

    @property
    def fillet_radius(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'FilletRadius' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.FilletRadius) if self.wrapped.FilletRadius else None

    @fillet_radius.setter
    def fillet_radius(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.FilletRadius = value

    @property
    def diameter(self) -> 'float':
        '''float: 'Diameter' is the original name of this property.'''

        return self.wrapped.Diameter

    @diameter.setter
    def diameter(self, value: 'float'):
        self.wrapped.Diameter = float(value) if value else 0.0

    @property
    def stress_concentration_factors(self) -> '_38.ProfilePointFilletStressConcentrationFactors':
        '''ProfilePointFilletStressConcentrationFactors: 'StressConcentrationFactors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_38.ProfilePointFilletStressConcentrationFactors)(self.wrapped.StressConcentrationFactors) if self.wrapped.StressConcentrationFactors else None
