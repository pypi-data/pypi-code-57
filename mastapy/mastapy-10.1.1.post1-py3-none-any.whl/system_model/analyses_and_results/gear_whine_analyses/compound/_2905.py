'''_2905.py

ZerolBevelGearSetCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1983
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _2904, _2956, _2877
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3738
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'ZerolBevelGearSetCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundGearWhineAnalysis',)


class ZerolBevelGearSetCompoundGearWhineAnalysis(_2877.BevelGearSetCompoundGearWhineAnalysis):
    '''ZerolBevelGearSetCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1983.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1983.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1983.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1983.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def zerol_bevel_gears_compound_gear_whine_analysis(self) -> 'List[_2904.ZerolBevelGearCompoundGearWhineAnalysis]':
        '''List[ZerolBevelGearCompoundGearWhineAnalysis]: 'ZerolBevelGearsCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundGearWhineAnalysis, constructor.new(_2904.ZerolBevelGearCompoundGearWhineAnalysis))
        return value

    @property
    def zerol_bevel_meshes_compound_gear_whine_analysis(self) -> 'List[_2956.ZerolBevelGearMeshCompoundGearWhineAnalysis]':
        '''List[ZerolBevelGearMeshCompoundGearWhineAnalysis]: 'ZerolBevelMeshesCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundGearWhineAnalysis, constructor.new(_2956.ZerolBevelGearMeshCompoundGearWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3738.ZerolBevelGearSetGearWhineAnalysis]':
        '''List[ZerolBevelGearSetGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3738.ZerolBevelGearSetGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_3738.ZerolBevelGearSetGearWhineAnalysis]':
        '''List[ZerolBevelGearSetGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_3738.ZerolBevelGearSetGearWhineAnalysis))
        return value
