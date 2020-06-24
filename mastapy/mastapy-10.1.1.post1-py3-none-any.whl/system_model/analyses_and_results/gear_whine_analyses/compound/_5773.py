'''_5773.py

SynchroniserSleeveCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2139
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5384
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5772
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'SynchroniserSleeveCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveCompoundGearWhineAnalysis',)


class SynchroniserSleeveCompoundGearWhineAnalysis(_5772.SynchroniserPartCompoundGearWhineAnalysis):
    '''SynchroniserSleeveCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2139.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2139.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5384.SynchroniserSleeveGearWhineAnalysis]':
        '''List[SynchroniserSleeveGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5384.SynchroniserSleeveGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5384.SynchroniserSleeveGearWhineAnalysis]':
        '''List[SynchroniserSleeveGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5384.SynchroniserSleeveGearWhineAnalysis))
        return value
