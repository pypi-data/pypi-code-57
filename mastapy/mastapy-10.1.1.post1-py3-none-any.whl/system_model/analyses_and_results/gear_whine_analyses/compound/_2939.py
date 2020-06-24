'''_2939.py

SpringDamperConnectionCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1828
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3772
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _2938
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_CONNECTION_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'SpringDamperConnectionCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperConnectionCompoundGearWhineAnalysis',)


class SpringDamperConnectionCompoundGearWhineAnalysis(_2938.CouplingConnectionCompoundGearWhineAnalysis):
    '''SpringDamperConnectionCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_CONNECTION_COMPOUND_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperConnectionCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1828.SpringDamperConnection':
        '''SpringDamperConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1828.SpringDamperConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1828.SpringDamperConnection':
        '''SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1828.SpringDamperConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3772.SpringDamperConnectionGearWhineAnalysis]':
        '''List[SpringDamperConnectionGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3772.SpringDamperConnectionGearWhineAnalysis))
        return value

    @property
    def connection_gear_whine_analysis_load_cases(self) -> 'List[_3772.SpringDamperConnectionGearWhineAnalysis]':
        '''List[SpringDamperConnectionGearWhineAnalysis]: 'ConnectionGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionGearWhineAnalysisLoadCases, constructor.new(_3772.SpringDamperConnectionGearWhineAnalysis))
        return value
