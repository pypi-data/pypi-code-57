'''_4867.py

CoaxialConnectionCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1833
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4721
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4934
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'CoaxialConnectionCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionCompoundModalAnalysis',)


class CoaxialConnectionCompoundModalAnalysis(_4934.ShaftToMountableComponentConnectionCompoundModalAnalysis):
    '''CoaxialConnectionCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _COAXIAL_CONNECTION_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoaxialConnectionCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1833.CoaxialConnection':
        '''CoaxialConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1833.CoaxialConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1833.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1833.CoaxialConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4721.CoaxialConnectionModalAnalysis]':
        '''List[CoaxialConnectionModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4721.CoaxialConnectionModalAnalysis))
        return value

    @property
    def connection_modal_analysis_load_cases(self) -> 'List[_4721.CoaxialConnectionModalAnalysis]':
        '''List[CoaxialConnectionModalAnalysis]: 'ConnectionModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisLoadCases, constructor.new(_4721.CoaxialConnectionModalAnalysis))
        return value
