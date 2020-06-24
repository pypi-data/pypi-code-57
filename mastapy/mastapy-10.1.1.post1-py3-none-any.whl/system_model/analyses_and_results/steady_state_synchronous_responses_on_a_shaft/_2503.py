'''_2503.py

ConceptCouplingHalfSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model.couplings import _2117
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6073
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2514
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'ConceptCouplingHalfSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfSteadyStateSynchronousResponseOnAShaft',)


class ConceptCouplingHalfSteadyStateSynchronousResponseOnAShaft(_2514.CouplingHalfSteadyStateSynchronousResponseOnAShaft):
    '''ConceptCouplingHalfSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2117.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2117.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6073.ConceptCouplingHalfLoadCase':
        '''ConceptCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6073.ConceptCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
