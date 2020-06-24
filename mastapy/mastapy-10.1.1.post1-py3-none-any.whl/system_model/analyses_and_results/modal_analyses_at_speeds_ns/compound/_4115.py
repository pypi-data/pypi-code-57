'''_4115.py

ConceptCouplingCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2116
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _3992
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4126
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'ConceptCouplingCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingCompoundModalAnalysesAtSpeeds',)


class ConceptCouplingCompoundModalAnalysesAtSpeeds(_4126.CouplingCompoundModalAnalysesAtSpeeds):
    '''ConceptCouplingCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2116.ConceptCoupling':
        '''ConceptCoupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2116.ConceptCoupling)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2116.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2116.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3992.ConceptCouplingModalAnalysesAtSpeeds]':
        '''List[ConceptCouplingModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3992.ConceptCouplingModalAnalysesAtSpeeds))
        return value

    @property
    def assembly_modal_analyses_at_speeds_load_cases(self) -> 'List[_3992.ConceptCouplingModalAnalysesAtSpeeds]':
        '''List[ConceptCouplingModalAnalysesAtSpeeds]: 'AssemblyModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtSpeedsLoadCases, constructor.new(_3992.ConceptCouplingModalAnalysesAtSpeeds))
        return value
