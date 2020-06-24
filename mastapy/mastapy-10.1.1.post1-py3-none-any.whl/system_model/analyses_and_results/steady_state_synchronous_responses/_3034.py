'''_3034.py

MassDiscSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model import _2004
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6148
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3082
from mastapy._internal.python_net import python_net_import

_MASS_DISC_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'MassDiscSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscSteadyStateSynchronousResponse',)


class MassDiscSteadyStateSynchronousResponse(_3082.VirtualComponentSteadyStateSynchronousResponse):
    '''MassDiscSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2004.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2004.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6148.MassDiscLoadCase':
        '''MassDiscLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6148.MassDiscLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[MassDiscSteadyStateSynchronousResponse]':
        '''List[MassDiscSteadyStateSynchronousResponse]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscSteadyStateSynchronousResponse))
        return value
