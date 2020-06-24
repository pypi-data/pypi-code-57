'''_1886.py

OptionsWhenExternalFEFileAlreadyExists
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_OPTIONS_WHEN_EXTERNAL_FE_FILE_ALREADY_EXISTS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'OptionsWhenExternalFEFileAlreadyExists')


__docformat__ = 'restructuredtext en'
__all__ = ('OptionsWhenExternalFEFileAlreadyExists',)


class OptionsWhenExternalFEFileAlreadyExists(_1.APIBase):
    '''OptionsWhenExternalFEFileAlreadyExists

    This is a mastapy class.
    '''

    TYPE = _OPTIONS_WHEN_EXTERNAL_FE_FILE_ALREADY_EXISTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'OptionsWhenExternalFEFileAlreadyExists.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def overwrite_existing_mesh_file(self) -> 'bool':
        '''bool: 'OverwriteExistingMeshFile' is the original name of this property.'''

        return self.wrapped.OverwriteExistingMeshFile

    @overwrite_existing_mesh_file.setter
    def overwrite_existing_mesh_file(self, value: 'bool'):
        self.wrapped.OverwriteExistingMeshFile = bool(value) if value else False

    @property
    def overwrite_existing_vectors_file(self) -> 'bool':
        '''bool: 'OverwriteExistingVectorsFile' is the original name of this property.'''

        return self.wrapped.OverwriteExistingVectorsFile

    @overwrite_existing_vectors_file.setter
    def overwrite_existing_vectors_file(self, value: 'bool'):
        self.wrapped.OverwriteExistingVectorsFile = bool(value) if value else False

    @property
    def output_mesh_file_path(self) -> 'str':
        '''str: 'OutputMeshFilePath' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OutputMeshFilePath

    @property
    def output_vectors_file_path(self) -> 'str':
        '''str: 'OutputVectorsFilePath' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OutputVectorsFilePath

    @property
    def append_current_date_and_time_to_new_file_names(self) -> 'bool':
        '''bool: 'AppendCurrentDateAndTimeToNewFileNames' is the original name of this property.'''

        return self.wrapped.AppendCurrentDateAndTimeToNewFileNames

    @append_current_date_and_time_to_new_file_names.setter
    def append_current_date_and_time_to_new_file_names(self, value: 'bool'):
        self.wrapped.AppendCurrentDateAndTimeToNewFileNames = bool(value) if value else False
