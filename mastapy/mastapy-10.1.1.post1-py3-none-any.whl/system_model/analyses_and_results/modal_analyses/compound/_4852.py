'''_4852.py

BeltConnectionCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1832
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4706
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4904
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'BeltConnectionCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionCompoundModalAnalysis',)


class BeltConnectionCompoundModalAnalysis(_4904.InterMountableComponentConnectionCompoundModalAnalysis):
    '''BeltConnectionCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionCompoundModalAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_4706.BeltConnectionModalAnalysis]':
        '''List[BeltConnectionModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4706.BeltConnectionModalAnalysis))
        return value

    @property
    def connection_modal_analysis_load_cases(self) -> 'List[_4706.BeltConnectionModalAnalysis]':
        '''List[BeltConnectionModalAnalysis]: 'ConnectionModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisLoadCases, constructor.new(_4706.BeltConnectionModalAnalysis))
        return value
