'''_3128.py

ClutchCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model.couplings import _1996
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2783
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _4330
from mastapy._internal.python_net import python_net_import

_CLUTCH_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'ClutchCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchCompoundSteadyStateSynchronousResponseOnAShaft',)


class ClutchCompoundSteadyStateSynchronousResponseOnAShaft(_4330.CouplingCompoundSteadyStateSynchronousResponseOnAShaft):
    '''ClutchCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1996.Clutch':
        '''Clutch: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1996.Clutch)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1996.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1996.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2783.ClutchSteadyStateSynchronousResponseOnAShaft]':
        '''List[ClutchSteadyStateSynchronousResponseOnAShaft]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2783.ClutchSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def assembly_steady_state_synchronous_response_on_a_shaft_load_cases(self) -> 'List[_2783.ClutchSteadyStateSynchronousResponseOnAShaft]':
        '''List[ClutchSteadyStateSynchronousResponseOnAShaft]: 'AssemblySteadyStateSynchronousResponseOnAShaftLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseOnAShaftLoadCases, constructor.new(_2783.ClutchSteadyStateSynchronousResponseOnAShaft))
        return value
