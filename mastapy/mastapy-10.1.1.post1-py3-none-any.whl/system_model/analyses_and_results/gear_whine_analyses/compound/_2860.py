'''_2860.py

PowerLoadCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1934
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3811
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _2864
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'PowerLoadCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadCompoundGearWhineAnalysis',)


class PowerLoadCompoundGearWhineAnalysis(_2864.VirtualComponentCompoundGearWhineAnalysis):
    '''PowerLoadCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_COMPOUND_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1934.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1934.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3811.PowerLoadGearWhineAnalysis]':
        '''List[PowerLoadGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3811.PowerLoadGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_3811.PowerLoadGearWhineAnalysis]':
        '''List[PowerLoadGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_3811.PowerLoadGearWhineAnalysis))
        return value
