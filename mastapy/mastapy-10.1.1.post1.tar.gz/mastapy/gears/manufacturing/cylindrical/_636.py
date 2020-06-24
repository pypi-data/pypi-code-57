'''_636.py

ModificationSegment
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_MODIFICATION_SEGMENT = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'ModificationSegment')


__docformat__ = 'restructuredtext en'
__all__ = ('ModificationSegment',)


class ModificationSegment(_1.APIBase):
    '''ModificationSegment

    This is a mastapy class.
    '''

    TYPE = _MODIFICATION_SEGMENT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModificationSegment.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def slope(self) -> 'float':
        '''float: 'Slope' is the original name of this property.'''

        return self.wrapped.Slope

    @slope.setter
    def slope(self, value: 'float'):
        self.wrapped.Slope = float(value) if value else 0.0

    @property
    def crown(self) -> 'float':
        '''float: 'Crown' is the original name of this property.'''

        return self.wrapped.Crown

    @crown.setter
    def crown(self, value: 'float'):
        self.wrapped.Crown = float(value) if value else 0.0
