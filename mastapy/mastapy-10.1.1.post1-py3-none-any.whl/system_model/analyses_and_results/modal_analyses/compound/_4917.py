'''_4917.py

OilSealCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2008
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4777
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4879
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'OilSealCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundModalAnalysis',)


class OilSealCompoundModalAnalysis(_4879.ConnectorCompoundModalAnalysis):
    '''OilSealCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2008.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2008.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4777.OilSealModalAnalysis]':
        '''List[OilSealModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4777.OilSealModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4777.OilSealModalAnalysis]':
        '''List[OilSealModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4777.OilSealModalAnalysis))
        return value
