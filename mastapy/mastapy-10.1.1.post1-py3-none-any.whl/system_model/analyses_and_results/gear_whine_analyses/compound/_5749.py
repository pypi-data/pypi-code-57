'''_5749.py

RollingRingCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2130
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5359
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5702
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'RollingRingCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingCompoundGearWhineAnalysis',)


class RollingRingCompoundGearWhineAnalysis(_5702.CouplingHalfCompoundGearWhineAnalysis):
    '''RollingRingCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2130.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2130.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5359.RollingRingGearWhineAnalysis]':
        '''List[RollingRingGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5359.RollingRingGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5359.RollingRingGearWhineAnalysis]':
        '''List[RollingRingGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5359.RollingRingGearWhineAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingCompoundGearWhineAnalysis]':
        '''List[RollingRingCompoundGearWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingCompoundGearWhineAnalysis))
        return value
