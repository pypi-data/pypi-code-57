'''_2778.py

DatumCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1916
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3798
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _2771
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'DatumCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundGearWhineAnalysis',)


class DatumCompoundGearWhineAnalysis(_2771.ComponentCompoundGearWhineAnalysis):
    '''DatumCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _DATUM_COMPOUND_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1916.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1916.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3798.DatumGearWhineAnalysis]':
        '''List[DatumGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3798.DatumGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_3798.DatumGearWhineAnalysis]':
        '''List[DatumGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_3798.DatumGearWhineAnalysis))
        return value
