'''_1703.py

BearingImportFile
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_BEARING_IMPORT_FILE = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling.XmlImport', 'BearingImportFile')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingImportFile',)


class BearingImportFile(_1.APIBase):
    '''BearingImportFile

    This is a mastapy class.
    '''

    TYPE = _BEARING_IMPORT_FILE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingImportFile.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def file_name(self) -> 'str':
        '''str: 'FileName' is the original name of this property.'''

        return self.wrapped.FileName

    @file_name.setter
    def file_name(self, value: 'str'):
        self.wrapped.FileName = str(value) if value else None

    @property
    def view_bearing(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ViewBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ViewBearing

    @property
    def import_bearing(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ImportBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ImportBearing

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name
