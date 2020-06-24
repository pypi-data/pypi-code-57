'''_1273.py

SelectableFolder
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SELECTABLE_FOLDER = python_net_import('SMT.MastaAPI.Utility', 'SelectableFolder')


__docformat__ = 'restructuredtext en'
__all__ = ('SelectableFolder',)


class SelectableFolder(_1.APIBase):
    '''SelectableFolder

    This is a mastapy class.
    '''

    TYPE = _SELECTABLE_FOLDER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SelectableFolder.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def folder(self) -> 'str':
        '''str: 'Folder' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Folder

    @property
    def edit_folder_path(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'EditFolderPath' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EditFolderPath
