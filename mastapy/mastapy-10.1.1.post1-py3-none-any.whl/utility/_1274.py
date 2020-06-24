'''_1274.py

SystemDirectory
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SYSTEM_DIRECTORY = python_net_import('SMT.MastaAPI.Utility', 'SystemDirectory')


__docformat__ = 'restructuredtext en'
__all__ = ('SystemDirectory',)


class SystemDirectory(_1.APIBase):
    '''SystemDirectory

    This is a mastapy class.
    '''

    TYPE = _SYSTEM_DIRECTORY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SystemDirectory.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def version(self) -> 'str':
        '''str: 'Version' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Version

    @property
    def directory_path(self) -> 'str':
        '''str: 'DirectoryPath' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DirectoryPath

    @property
    def directory_name(self) -> 'str':
        '''str: 'DirectoryName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DirectoryName

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def open(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Open' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Open
