'''_3324.py

ZerolBevelGearSetCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2013
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3323, _3375, _3296
from mastapy.system_model.analyses_and_results.modal_analyses import _3856
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ZerolBevelGearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundModalAnalysis',)


class ZerolBevelGearSetCompoundModalAnalysis(_3296.BevelGearSetCompoundModalAnalysis):
    '''ZerolBevelGearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2013.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2013.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2013.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2013.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def zerol_bevel_gears_compound_modal_analysis(self) -> 'List[_3323.ZerolBevelGearCompoundModalAnalysis]':
        '''List[ZerolBevelGearCompoundModalAnalysis]: 'ZerolBevelGearsCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundModalAnalysis, constructor.new(_3323.ZerolBevelGearCompoundModalAnalysis))
        return value

    @property
    def zerol_bevel_meshes_compound_modal_analysis(self) -> 'List[_3375.ZerolBevelGearMeshCompoundModalAnalysis]':
        '''List[ZerolBevelGearMeshCompoundModalAnalysis]: 'ZerolBevelMeshesCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundModalAnalysis, constructor.new(_3375.ZerolBevelGearMeshCompoundModalAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3856.ZerolBevelGearSetModalAnalysis]':
        '''List[ZerolBevelGearSetModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3856.ZerolBevelGearSetModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_3856.ZerolBevelGearSetModalAnalysis]':
        '''List[ZerolBevelGearSetModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_3856.ZerolBevelGearSetModalAnalysis))
        return value
