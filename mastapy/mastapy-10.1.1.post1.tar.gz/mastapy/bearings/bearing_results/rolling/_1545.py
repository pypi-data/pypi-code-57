'''_1545.py

ISO14179SettingsDatabase
'''


from typing import Iterable

from mastapy.bearings.bearing_results.rolling import _1544
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ISO14179_SETTINGS_DATABASE = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'ISO14179SettingsDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO14179SettingsDatabase',)


class ISO14179SettingsDatabase(_1.APIBase):
    '''ISO14179SettingsDatabase

    This is a mastapy class.
    '''

    TYPE = _ISO14179_SETTINGS_DATABASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ISO14179SettingsDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_1544.ISO14179Settings':
        '''ISO14179Settings: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1544.ISO14179Settings)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_1544.ISO14179Settings':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.bearings.bearing_results.rolling.ISO14179Settings
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_1544.ISO14179Settings)(method_result) if method_result else None

    def can_be_removed(self, iso14179_settings: '_1544.ISO14179Settings') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            iso14179_settings (mastapy.bearings.bearing_results.rolling.ISO14179Settings)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(iso14179_settings.wrapped if iso14179_settings else None)
        return method_result

    def rename(self, iso14179_settings: '_1544.ISO14179Settings', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            iso14179_settings (mastapy.bearings.bearing_results.rolling.ISO14179Settings)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(iso14179_settings.wrapped if iso14179_settings else None, new_name if new_name else None)
        return method_result

    def remove(self, iso14179_settings: '_1544.ISO14179Settings'):
        ''' 'Remove' is the original name of this method.

        Args:
            iso14179_settings (mastapy.bearings.bearing_results.rolling.ISO14179Settings)
        '''

        self.wrapped.Remove(iso14179_settings.wrapped if iso14179_settings else None)

    def get_all_items(self) -> 'Iterable[_1544.ISO14179Settings]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.bearings.bearing_results.rolling.ISO14179Settings]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_1544.ISO14179Settings))

    def save_changes(self, iso14179_settings: '_1544.ISO14179Settings'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            iso14179_settings (mastapy.bearings.bearing_results.rolling.ISO14179Settings)
        '''

        self.wrapped.SaveChanges(iso14179_settings.wrapped if iso14179_settings else None)
