'''_1900.py

ImportedFEVersionComparer
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.imported_fes.version_comparer import _1902, _1898
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_VERSION_COMPARER = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs.VersionComparer', 'ImportedFEVersionComparer')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEVersionComparer',)


class ImportedFEVersionComparer(_1.APIBase):
    '''ImportedFEVersionComparer

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_VERSION_COMPARER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEVersionComparer.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def save_new_design_files(self) -> 'bool':
        '''bool: 'SaveNewDesignFiles' is the original name of this property.'''

        return self.wrapped.SaveNewDesignFiles

    @save_new_design_files.setter
    def save_new_design_files(self, value: 'bool'):
        self.wrapped.SaveNewDesignFiles = bool(value) if value else False

    @property
    def check_all_files_in_directory(self) -> 'bool':
        '''bool: 'CheckAllFilesInDirectory' is the original name of this property.'''

        return self.wrapped.CheckAllFilesInDirectory

    @check_all_files_in_directory.setter
    def check_all_files_in_directory(self, value: 'bool'):
        self.wrapped.CheckAllFilesInDirectory = bool(value) if value else False

    @property
    def edit_folder_path(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'EditFolderPath' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EditFolderPath

    @property
    def file(self) -> 'str':
        '''str: 'File' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.File

    @property
    def select_file(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SelectFile' is the original name of this property.'''

        return self.wrapped.SelectFile

    @select_file.setter
    def select_file(self, value: 'Callable[[], None]'):
        value = value if value else None
        self.wrapped.SelectFile = value

    @property
    def folder_path_for_saved_files(self) -> 'str':
        '''str: 'FolderPathForSavedFiles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FolderPathForSavedFiles

    @property
    def run(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Run' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Run

    @property
    def status(self) -> 'str':
        '''str: 'Status' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Status

    @property
    def load_cases_to_run(self) -> '_1902.LoadCasesToRun':
        '''LoadCasesToRun: 'LoadCasesToRun' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.LoadCasesToRun)
        return constructor.new(_1902.LoadCasesToRun)(value) if value else None

    @load_cases_to_run.setter
    def load_cases_to_run(self, value: '_1902.LoadCasesToRun'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.LoadCasesToRun = value

    @property
    def design_results(self) -> 'List[_1898.DesignResults]':
        '''List[DesignResults]: 'DesignResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DesignResults, constructor.new(_1898.DesignResults))
        return value
