'''_5207.py

SpringDamperHalfCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2134
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5076
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5148
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'SpringDamperHalfCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfCompoundMultiBodyDynamicsAnalysis',)


class SpringDamperHalfCompoundMultiBodyDynamicsAnalysis(_5148.CouplingHalfCompoundMultiBodyDynamicsAnalysis):
    '''SpringDamperHalfCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2134.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2134.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5076.SpringDamperHalfMultiBodyDynamicsAnalysis]':
        '''List[SpringDamperHalfMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5076.SpringDamperHalfMultiBodyDynamicsAnalysis))
        return value

    @property
    def component_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5076.SpringDamperHalfMultiBodyDynamicsAnalysis]':
        '''List[SpringDamperHalfMultiBodyDynamicsAnalysis]: 'ComponentMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5076.SpringDamperHalfMultiBodyDynamicsAnalysis))
        return value
