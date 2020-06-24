'''_3322.py

WormGearSetCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2011
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3321, _3374, _3303
from mastapy.system_model.analyses_and_results.modal_analyses import _3854
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'WormGearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundModalAnalysis',)


class WormGearSetCompoundModalAnalysis(_3303.GearSetCompoundModalAnalysis):
    '''WormGearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2011.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2011.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2011.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2011.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def worm_gears_compound_modal_analysis(self) -> 'List[_3321.WormGearCompoundModalAnalysis]':
        '''List[WormGearCompoundModalAnalysis]: 'WormGearsCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundModalAnalysis, constructor.new(_3321.WormGearCompoundModalAnalysis))
        return value

    @property
    def worm_meshes_compound_modal_analysis(self) -> 'List[_3374.WormGearMeshCompoundModalAnalysis]':
        '''List[WormGearMeshCompoundModalAnalysis]: 'WormMeshesCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundModalAnalysis, constructor.new(_3374.WormGearMeshCompoundModalAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3854.WormGearSetModalAnalysis]':
        '''List[WormGearSetModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3854.WormGearSetModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_3854.WormGearSetModalAnalysis]':
        '''List[WormGearSetModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_3854.WormGearSetModalAnalysis))
        return value
