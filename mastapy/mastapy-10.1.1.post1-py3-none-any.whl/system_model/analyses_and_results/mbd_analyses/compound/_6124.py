'''_6124.py

PlanetCarrierCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1932
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5994
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6119
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'PlanetCarrierCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierCompoundMultiBodyDynamicsAnalysis',)


class PlanetCarrierCompoundMultiBodyDynamicsAnalysis(_6119.MountableComponentCompoundMultiBodyDynamicsAnalysis):
    '''PlanetCarrierCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1932.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1932.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5994.PlanetCarrierMultiBodyDynamicsAnalysis]':
        '''List[PlanetCarrierMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5994.PlanetCarrierMultiBodyDynamicsAnalysis))
        return value

    @property
    def component_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5994.PlanetCarrierMultiBodyDynamicsAnalysis]':
        '''List[PlanetCarrierMultiBodyDynamicsAnalysis]: 'ComponentMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5994.PlanetCarrierMultiBodyDynamicsAnalysis))
        return value
