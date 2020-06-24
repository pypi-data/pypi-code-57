'''_2965.py

DatumCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1916
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _3916
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _2963
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'DatumCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundModalAnalysis',)


class DatumCompoundModalAnalysis(_2963.ComponentCompoundModalAnalysis):
    '''DatumCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _DATUM_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1916.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1916.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3916.DatumModalAnalysis]':
        '''List[DatumModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3916.DatumModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_3916.DatumModalAnalysis]':
        '''List[DatumModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_3916.DatumModalAnalysis))
        return value
