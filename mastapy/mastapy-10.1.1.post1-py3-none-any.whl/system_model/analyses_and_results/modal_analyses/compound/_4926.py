'''_4926.py

PowerLoadCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2013
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4787
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4959
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'PowerLoadCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadCompoundModalAnalysis',)


class PowerLoadCompoundModalAnalysis(_4959.VirtualComponentCompoundModalAnalysis):
    '''PowerLoadCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2013.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2013.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4787.PowerLoadModalAnalysis]':
        '''List[PowerLoadModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4787.PowerLoadModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4787.PowerLoadModalAnalysis]':
        '''List[PowerLoadModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4787.PowerLoadModalAnalysis))
        return value
