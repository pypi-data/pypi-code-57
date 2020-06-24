'''_6158.py

UnbalancedMassCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1938
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _6033
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6159
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'UnbalancedMassCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassCompoundMultiBodyDynamicsAnalysis',)


class UnbalancedMassCompoundMultiBodyDynamicsAnalysis(_6159.VirtualComponentCompoundMultiBodyDynamicsAnalysis):
    '''UnbalancedMassCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1938.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1938.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6033.UnbalancedMassMultiBodyDynamicsAnalysis]':
        '''List[UnbalancedMassMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6033.UnbalancedMassMultiBodyDynamicsAnalysis))
        return value

    @property
    def component_multi_body_dynamics_analysis_load_cases(self) -> 'List[_6033.UnbalancedMassMultiBodyDynamicsAnalysis]':
        '''List[UnbalancedMassMultiBodyDynamicsAnalysis]: 'ComponentMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultiBodyDynamicsAnalysisLoadCases, constructor.new(_6033.UnbalancedMassMultiBodyDynamicsAnalysis))
        return value
