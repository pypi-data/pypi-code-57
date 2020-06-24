'''_1787.py

SocketConnectionSelection
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SOCKET_CONNECTION_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'SocketConnectionSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('SocketConnectionSelection',)


class SocketConnectionSelection(_1.APIBase):
    '''SocketConnectionSelection

    This is a mastapy class.
    '''

    TYPE = _SOCKET_CONNECTION_SELECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SocketConnectionSelection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def select(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Select' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Select
