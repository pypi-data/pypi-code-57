'''_6074.py

ConceptCouplingHalfCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2016
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5934
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6085
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'ConceptCouplingHalfCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfCompoundMultiBodyDynamicsAnalysis',)


class ConceptCouplingHalfCompoundMultiBodyDynamicsAnalysis(_6085.CouplingHalfCompoundMultiBodyDynamicsAnalysis):
    '''ConceptCouplingHalfCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2016.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2016.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5934.ConceptCouplingHalfMultiBodyDynamicsAnalysis]':
        '''List[ConceptCouplingHalfMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5934.ConceptCouplingHalfMultiBodyDynamicsAnalysis))
        return value

    @property
    def component_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5934.ConceptCouplingHalfMultiBodyDynamicsAnalysis]':
        '''List[ConceptCouplingHalfMultiBodyDynamicsAnalysis]: 'ComponentMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5934.ConceptCouplingHalfMultiBodyDynamicsAnalysis))
        return value
