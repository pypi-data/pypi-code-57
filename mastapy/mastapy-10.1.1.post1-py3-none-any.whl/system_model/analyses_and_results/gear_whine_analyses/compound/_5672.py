'''_5672.py

BeltConnectionCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1832
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5260
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5724
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'BeltConnectionCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionCompoundGearWhineAnalysis',)


class BeltConnectionCompoundGearWhineAnalysis(_5724.InterMountableComponentConnectionCompoundGearWhineAnalysis):
    '''BeltConnectionCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1832.BeltConnection':
        '''BeltConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1832.BeltConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1832.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1832.BeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5260.BeltConnectionGearWhineAnalysis]':
        '''List[BeltConnectionGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5260.BeltConnectionGearWhineAnalysis))
        return value

    @property
    def connection_gear_whine_analysis_load_cases(self) -> 'List[_5260.BeltConnectionGearWhineAnalysis]':
        '''List[BeltConnectionGearWhineAnalysis]: 'ConnectionGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionGearWhineAnalysisLoadCases, constructor.new(_5260.BeltConnectionGearWhineAnalysis))
        return value
