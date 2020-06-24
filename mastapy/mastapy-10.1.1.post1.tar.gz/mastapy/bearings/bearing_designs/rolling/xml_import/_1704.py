'''_1704.py

RollingBearingImporter
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_designs.rolling.xml_import import _1705
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ROLLING_BEARING_IMPORTER = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling.XmlImport', 'RollingBearingImporter')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingBearingImporter',)


class RollingBearingImporter(_1.APIBase):
    '''RollingBearingImporter

    This is a mastapy class.
    '''

    TYPE = _ROLLING_BEARING_IMPORTER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingBearingImporter.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def replace_existing_bearings(self) -> 'bool':
        '''bool: 'ReplaceExistingBearings' is the original name of this property.'''

        return self.wrapped.ReplaceExistingBearings

    @replace_existing_bearings.setter
    def replace_existing_bearings(self, value: 'bool'):
        self.wrapped.ReplaceExistingBearings = bool(value) if value else False

    @property
    def open_files_in_directory(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'OpenFilesInDirectory' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OpenFilesInDirectory

    @property
    def import_all(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ImportAll' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ImportAll

    @property
    def number_of_bearings_ready_to_import(self) -> 'int':
        '''int: 'NumberOfBearingsReadyToImport' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfBearingsReadyToImport

    @property
    def save_setup(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SaveSetup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SaveSetup

    @property
    def load_setup(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'LoadSetup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadSetup

    @property
    def reset_to_defaults(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ResetToDefaults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ResetToDefaults

    @property
    def mappings(self) -> 'List[_1705.XmlBearingTypeMapping]':
        '''List[XmlBearingTypeMapping]: 'Mappings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Mappings, constructor.new(_1705.XmlBearingTypeMapping))
        return value
