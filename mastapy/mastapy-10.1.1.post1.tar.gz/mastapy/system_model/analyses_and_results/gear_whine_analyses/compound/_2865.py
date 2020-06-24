'''_2865.py

ShaftCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _1942
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3816
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _2841
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'ShaftCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundGearWhineAnalysis',)


class ShaftCompoundGearWhineAnalysis(_2841.AbstractShaftOrHousingCompoundGearWhineAnalysis):
    '''ShaftCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_COMPOUND_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1942.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1942.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3816.ShaftGearWhineAnalysis]':
        '''List[ShaftGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3816.ShaftGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_3816.ShaftGearWhineAnalysis]':
        '''List[ShaftGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_3816.ShaftGearWhineAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundGearWhineAnalysis]':
        '''List[ShaftCompoundGearWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftCompoundGearWhineAnalysis))
        return value
