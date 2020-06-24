'''_1786.py

SocketConnectionOptions
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1787
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SOCKET_CONNECTION_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'SocketConnectionOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('SocketConnectionOptions',)


class SocketConnectionOptions(_1.APIBase):
    '''SocketConnectionOptions

    This is a mastapy class.
    '''

    TYPE = _SOCKET_CONNECTION_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SocketConnectionOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def sockets(self) -> 'List[_1787.SocketConnectionSelection]':
        '''List[SocketConnectionSelection]: 'Sockets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Sockets, constructor.new(_1787.SocketConnectionSelection))
        return value
