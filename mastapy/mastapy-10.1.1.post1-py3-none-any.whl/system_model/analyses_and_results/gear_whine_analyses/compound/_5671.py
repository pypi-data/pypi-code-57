'''_5671.py

BearingCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1985
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5259
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5699
from mastapy._internal.python_net import python_net_import

_BEARING_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'BearingCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCompoundGearWhineAnalysis',)


class BearingCompoundGearWhineAnalysis(_5699.ConnectorCompoundGearWhineAnalysis):
    '''BearingCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1985.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5259.BearingGearWhineAnalysis]':
        '''List[BearingGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5259.BearingGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5259.BearingGearWhineAnalysis]':
        '''List[BearingGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5259.BearingGearWhineAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[BearingCompoundGearWhineAnalysis]':
        '''List[BearingCompoundGearWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingCompoundGearWhineAnalysis))
        return value
