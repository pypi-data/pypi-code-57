'''_3045.py

PointLoadSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model import _2012
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6165
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3082
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'PointLoadSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadSteadyStateSynchronousResponse',)


class PointLoadSteadyStateSynchronousResponse(_3082.VirtualComponentSteadyStateSynchronousResponse):
    '''PointLoadSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2012.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2012.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6165.PointLoadLoadCase':
        '''PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6165.PointLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
