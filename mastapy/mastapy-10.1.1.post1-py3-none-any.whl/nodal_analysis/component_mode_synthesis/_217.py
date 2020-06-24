'''_217.py

FullFEModel
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis.dev_tools_analyses import _180
from mastapy.nodal_analysis.component_mode_synthesis import _215, _212
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_FULL_FE_MODEL = python_net_import('SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis', 'FullFEModel')


__docformat__ = 'restructuredtext en'
__all__ = ('FullFEModel',)


class FullFEModel(_1.APIBase):
    '''FullFEModel

    This is a mastapy class.
    '''

    TYPE = _FULL_FE_MODEL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FullFEModel.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def memory_required_for_stiffness_and_mass_matrices(self) -> 'str':
        '''str: 'MemoryRequiredForStiffnessAndMassMatrices' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MemoryRequiredForStiffnessAndMassMatrices

    @property
    def memory_required_for_displacement_expansion(self) -> 'str':
        '''str: 'MemoryRequiredForDisplacementExpansion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MemoryRequiredForDisplacementExpansion

    @property
    def total_memory_required_for_mesh(self) -> 'str':
        '''str: 'TotalMemoryRequiredForMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalMemoryRequiredForMesh

    @property
    def total_memory_required_for_results(self) -> 'str':
        '''str: 'TotalMemoryRequiredForResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalMemoryRequiredForResults

    @property
    def estimated_memory_required_for_stiffness_and_mass_matrices(self) -> 'str':
        '''str: 'EstimatedMemoryRequiredForStiffnessAndMassMatrices' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EstimatedMemoryRequiredForStiffnessAndMassMatrices

    @property
    def estimated_memory_required_for_displacement_expansion(self) -> 'str':
        '''str: 'EstimatedMemoryRequiredForDisplacementExpansion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EstimatedMemoryRequiredForDisplacementExpansion

    @property
    def estimated_total_memory_required_for_results(self) -> 'str':
        '''str: 'EstimatedTotalMemoryRequiredForResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EstimatedTotalMemoryRequiredForResults

    @property
    def time_taken_for_reduction(self) -> 'str':
        '''str: 'TimeTakenForReduction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TimeTakenForReduction

    @property
    def specifications_of_computer_used_for_reduction(self) -> 'str':
        '''str: 'SpecificationsOfComputerUsedForReduction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpecificationsOfComputerUsedForReduction

    @property
    def has_condensation_result(self) -> 'bool':
        '''bool: 'HasCondensationResult' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasCondensationResult

    @property
    def fe_model(self) -> '_180.FEModel':
        '''FEModel: 'FEModel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_180.FEModel)(self.wrapped.FEModel) if self.wrapped.FEModel else None

    @property
    def reduction_options(self) -> '_215.CMSOptions':
        '''CMSOptions: 'ReductionOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_215.CMSOptions)(self.wrapped.ReductionOptions) if self.wrapped.ReductionOptions else None

    @property
    def element_face_groups(self) -> 'List[_212.CMSElementFaceGroup]':
        '''List[CMSElementFaceGroup]: 'ElementFaceGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ElementFaceGroups, constructor.new(_212.CMSElementFaceGroup))
        return value
