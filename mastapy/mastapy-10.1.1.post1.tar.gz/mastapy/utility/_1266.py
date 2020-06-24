'''_1266.py

FolderMonitor
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_FOLDER_MONITOR = python_net_import('SMT.MastaAPI.Utility', 'FolderMonitor')


__docformat__ = 'restructuredtext en'
__all__ = ('FolderMonitor',)


class FolderMonitor(_1.APIBase):
    '''FolderMonitor

    This is a mastapy class.
    '''

    TYPE = _FOLDER_MONITOR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FolderMonitor.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def edit_folder_path(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'EditFolderPath' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EditFolderPath

    @property
    def folder_to_monitor(self) -> 'str':
        '''str: 'FolderToMonitor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FolderToMonitor

    @property
    def stop_monitoring(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'StopMonitoring' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StopMonitoring
