'''_6127.py

PulleyCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2017
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5997
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6085
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'PulleyCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCompoundMultiBodyDynamicsAnalysis',)


class PulleyCompoundMultiBodyDynamicsAnalysis(_6085.CouplingHalfCompoundMultiBodyDynamicsAnalysis):
    '''PulleyCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _PULLEY_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2017.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2017.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5997.PulleyMultiBodyDynamicsAnalysis]':
        '''List[PulleyMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5997.PulleyMultiBodyDynamicsAnalysis))
        return value

    @property
    def component_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5997.PulleyMultiBodyDynamicsAnalysis]':
        '''List[PulleyMultiBodyDynamicsAnalysis]: 'ComponentMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5997.PulleyMultiBodyDynamicsAnalysis))
        return value
