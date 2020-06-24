'''_3335.py

ShaftHubConnectionCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2028
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _3867
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3265
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ShaftHubConnectionCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionCompoundModalAnalysis',)


class ShaftHubConnectionCompoundModalAnalysis(_3265.ConnectorCompoundModalAnalysis):
    '''ShaftHubConnectionCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2028.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2028.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3867.ShaftHubConnectionModalAnalysis]':
        '''List[ShaftHubConnectionModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3867.ShaftHubConnectionModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_3867.ShaftHubConnectionModalAnalysis]':
        '''List[ShaftHubConnectionModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_3867.ShaftHubConnectionModalAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionCompoundModalAnalysis]':
        '''List[ShaftHubConnectionCompoundModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionCompoundModalAnalysis))
        return value
