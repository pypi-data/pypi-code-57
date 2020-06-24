'''_47.py

ShaftFeature
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SHAFT_FEATURE = python_net_import('SMT.MastaAPI.Shafts', 'ShaftFeature')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftFeature',)


class ShaftFeature(_1.APIBase):
    '''ShaftFeature

    This is a mastapy class.
    '''

    TYPE = _SHAFT_FEATURE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftFeature.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def delete(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Delete' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Delete

    @property
    def offset(self) -> 'float':
        '''float: 'Offset' is the original name of this property.'''

        return self.wrapped.Offset

    @offset.setter
    def offset(self, value: 'float'):
        self.wrapped.Offset = float(value) if value else 0.0
