'''_3305.py

HypoidGearSetCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1994
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3304, _3368, _3290
from mastapy.system_model.analyses_and_results.modal_analyses import _3955
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'HypoidGearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundModalAnalysis',)


class HypoidGearSetCompoundModalAnalysis(_3290.AGMAGleasonConicalGearSetCompoundModalAnalysis):
    '''HypoidGearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1994.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1994.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1994.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1994.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def hypoid_gears_compound_modal_analysis(self) -> 'List[_3304.HypoidGearCompoundModalAnalysis]':
        '''List[HypoidGearCompoundModalAnalysis]: 'HypoidGearsCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCompoundModalAnalysis, constructor.new(_3304.HypoidGearCompoundModalAnalysis))
        return value

    @property
    def hypoid_meshes_compound_modal_analysis(self) -> 'List[_3368.HypoidGearMeshCompoundModalAnalysis]':
        '''List[HypoidGearMeshCompoundModalAnalysis]: 'HypoidMeshesCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCompoundModalAnalysis, constructor.new(_3368.HypoidGearMeshCompoundModalAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3955.HypoidGearSetModalAnalysis]':
        '''List[HypoidGearSetModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3955.HypoidGearSetModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_3955.HypoidGearSetModalAnalysis]':
        '''List[HypoidGearSetModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_3955.HypoidGearSetModalAnalysis))
        return value
