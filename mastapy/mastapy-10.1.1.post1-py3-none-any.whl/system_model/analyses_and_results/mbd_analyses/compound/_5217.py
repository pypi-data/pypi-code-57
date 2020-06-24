'''_5217.py

SynchroniserHalfCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2137
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5086
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5218
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'SynchroniserHalfCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfCompoundMultiBodyDynamicsAnalysis',)


class SynchroniserHalfCompoundMultiBodyDynamicsAnalysis(_5218.SynchroniserPartCompoundMultiBodyDynamicsAnalysis):
    '''SynchroniserHalfCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2137.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2137.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5086.SynchroniserHalfMultiBodyDynamicsAnalysis]':
        '''List[SynchroniserHalfMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5086.SynchroniserHalfMultiBodyDynamicsAnalysis))
        return value

    @property
    def component_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5086.SynchroniserHalfMultiBodyDynamicsAnalysis]':
        '''List[SynchroniserHalfMultiBodyDynamicsAnalysis]: 'ComponentMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5086.SynchroniserHalfMultiBodyDynamicsAnalysis))
        return value
