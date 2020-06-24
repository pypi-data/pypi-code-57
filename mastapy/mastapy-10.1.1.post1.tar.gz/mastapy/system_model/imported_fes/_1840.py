'''_1840.py

BatchOperations
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.imported_fes import _1854
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_BATCH_OPERATIONS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'BatchOperations')


__docformat__ = 'restructuredtext en'
__all__ = ('BatchOperations',)


class BatchOperations(_1.APIBase):
    '''BatchOperations

    This is a mastapy class.
    '''

    TYPE = _BATCH_OPERATIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BatchOperations.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def perform_reduction_for_selected(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'PerformReductionForSelected' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PerformReductionForSelected

    @property
    def remove_all_full_fe_meshes_in_design(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'RemoveAllFullFEMeshesInDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RemoveAllFullFEMeshesInDesign

    @property
    def load_all_selected_external_files(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'LoadAllSelectedExternalFiles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadAllSelectedExternalFiles

    @property
    def unload_all_selected_external_files(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'UnloadAllSelectedExternalFiles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.UnloadAllSelectedExternalFiles

    @property
    def total_memory_for_all_loaded_external_fes(self) -> 'str':
        '''str: 'TotalMemoryForAllLoadedExternalFEs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalMemoryForAllLoadedExternalFEs

    @property
    def total_memory_for_all_files_selected_to_unload(self) -> 'str':
        '''str: 'TotalMemoryForAllFilesSelectedToUnload' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalMemoryForAllFilesSelectedToUnload

    @property
    def fe_components(self) -> 'List[_1854.FEComponentWithBatchOptions]':
        '''List[FEComponentWithBatchOptions]: 'FEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEComponents, constructor.new(_1854.FEComponentWithBatchOptions))
        return value

    @property
    def fe_components_with_external_files(self) -> 'List[_1854.FEComponentWithBatchOptions]':
        '''List[FEComponentWithBatchOptions]: 'FEComponentsWithExternalFiles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEComponentsWithExternalFiles, constructor.new(_1854.FEComponentWithBatchOptions))
        return value
