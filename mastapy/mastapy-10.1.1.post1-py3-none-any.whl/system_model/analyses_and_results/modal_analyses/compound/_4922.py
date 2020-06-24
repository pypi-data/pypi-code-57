'''_4922.py

PlanetaryConnectionCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1848
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4783
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4934
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'PlanetaryConnectionCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionCompoundModalAnalysis',)


class PlanetaryConnectionCompoundModalAnalysis(_4934.ShaftToMountableComponentConnectionCompoundModalAnalysis):
    '''PlanetaryConnectionCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1848.PlanetaryConnection':
        '''PlanetaryConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1848.PlanetaryConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1848.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1848.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4783.PlanetaryConnectionModalAnalysis]':
        '''List[PlanetaryConnectionModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4783.PlanetaryConnectionModalAnalysis))
        return value

    @property
    def connection_modal_analysis_load_cases(self) -> 'List[_4783.PlanetaryConnectionModalAnalysis]':
        '''List[PlanetaryConnectionModalAnalysis]: 'ConnectionModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisLoadCases, constructor.new(_4783.PlanetaryConnectionModalAnalysis))
        return value
