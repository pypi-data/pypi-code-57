'''_3318.py

StraightBevelGearSetCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2007
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3317, _3373, _3296
from mastapy.system_model.analyses_and_results.modal_analyses import _3968
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'StraightBevelGearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetCompoundModalAnalysis',)


class StraightBevelGearSetCompoundModalAnalysis(_3296.BevelGearSetCompoundModalAnalysis):
    '''StraightBevelGearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2007.StraightBevelGearSet':
        '''StraightBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.StraightBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2007.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_gears_compound_modal_analysis(self) -> 'List[_3317.StraightBevelGearCompoundModalAnalysis]':
        '''List[StraightBevelGearCompoundModalAnalysis]: 'StraightBevelGearsCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsCompoundModalAnalysis, constructor.new(_3317.StraightBevelGearCompoundModalAnalysis))
        return value

    @property
    def straight_bevel_meshes_compound_modal_analysis(self) -> 'List[_3373.StraightBevelGearMeshCompoundModalAnalysis]':
        '''List[StraightBevelGearMeshCompoundModalAnalysis]: 'StraightBevelMeshesCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesCompoundModalAnalysis, constructor.new(_3373.StraightBevelGearMeshCompoundModalAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3968.StraightBevelGearSetModalAnalysis]':
        '''List[StraightBevelGearSetModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3968.StraightBevelGearSetModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_3968.StraightBevelGearSetModalAnalysis]':
        '''List[StraightBevelGearSetModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_3968.StraightBevelGearSetModalAnalysis))
        return value
