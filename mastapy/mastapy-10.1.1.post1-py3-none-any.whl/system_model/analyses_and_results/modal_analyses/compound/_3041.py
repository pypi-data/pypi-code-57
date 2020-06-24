'''_3041.py

PointLoadCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1933
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _3929
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3046
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'PointLoadCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundModalAnalysis',)


class PointLoadCompoundModalAnalysis(_3046.VirtualComponentCompoundModalAnalysis):
    '''PointLoadCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1933.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1933.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3929.PointLoadModalAnalysis]':
        '''List[PointLoadModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3929.PointLoadModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_3929.PointLoadModalAnalysis]':
        '''List[PointLoadModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_3929.PointLoadModalAnalysis))
        return value
