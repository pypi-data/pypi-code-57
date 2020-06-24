'''_6102.py

GuideDxfModelCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1921
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5964
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6071
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'GuideDxfModelCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelCompoundMultiBodyDynamicsAnalysis',)


class GuideDxfModelCompoundMultiBodyDynamicsAnalysis(_6071.ComponentCompoundMultiBodyDynamicsAnalysis):
    '''GuideDxfModelCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1921.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1921.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5964.GuideDxfModelMultiBodyDynamicsAnalysis]':
        '''List[GuideDxfModelMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5964.GuideDxfModelMultiBodyDynamicsAnalysis))
        return value

    @property
    def component_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5964.GuideDxfModelMultiBodyDynamicsAnalysis]':
        '''List[GuideDxfModelMultiBodyDynamicsAnalysis]: 'ComponentMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5964.GuideDxfModelMultiBodyDynamicsAnalysis))
        return value
