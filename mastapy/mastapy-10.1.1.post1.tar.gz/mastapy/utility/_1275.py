'''_1275.py

SystemDirectoryPopulator
'''


from mastapy._internal.implicit import list_with_selected_item
from mastapy.utility import _1274
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SYSTEM_DIRECTORY_POPULATOR = python_net_import('SMT.MastaAPI.Utility', 'SystemDirectoryPopulator')


__docformat__ = 'restructuredtext en'
__all__ = ('SystemDirectoryPopulator',)


class SystemDirectoryPopulator(_1.APIBase):
    '''SystemDirectoryPopulator

    This is a mastapy class.
    '''

    TYPE = _SYSTEM_DIRECTORY_POPULATOR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SystemDirectoryPopulator.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def selected_version(self) -> 'list_with_selected_item.ListWithSelectedItem_SystemDirectory':
        '''list_with_selected_item.ListWithSelectedItem_SystemDirectory: 'SelectedVersion' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_SystemDirectory)(self.wrapped.SelectedVersion) if self.wrapped.SelectedVersion else None

    @selected_version.setter
    def selected_version(self, value: 'list_with_selected_item.ListWithSelectedItem_SystemDirectory.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_SystemDirectory.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_SystemDirectory.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.SelectedVersion = value

    @property
    def copy_from(self) -> 'SystemDirectoryPopulator.SetupFrom':
        '''SetupFrom: 'CopyFrom' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.CopyFrom)
        return constructor.new(SystemDirectoryPopulator.SetupFrom)(value) if value else None

    @copy_from.setter
    def copy_from(self, value: 'SystemDirectoryPopulator.SetupFrom'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CopyFrom = value

    @property
    def version_to_copy(self) -> '_1274.SystemDirectory':
        '''SystemDirectory: 'VersionToCopy' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1274.SystemDirectory)(self.wrapped.VersionToCopy) if self.wrapped.VersionToCopy else None

    @property
    def current_version(self) -> '_1274.SystemDirectory':
        '''SystemDirectory: 'CurrentVersion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1274.SystemDirectory)(self.wrapped.CurrentVersion) if self.wrapped.CurrentVersion else None
