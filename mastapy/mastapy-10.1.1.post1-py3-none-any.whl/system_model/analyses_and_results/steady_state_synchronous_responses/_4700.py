'''_4700.py

ExternalCADModelSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model import _1919
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2274
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _4676
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'ExternalCADModelSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelSteadyStateSynchronousResponse',)


class ExternalCADModelSteadyStateSynchronousResponse(_4676.ComponentSteadyStateSynchronousResponse):
    '''ExternalCADModelSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_STEADY_STATE_SYNCHRONOUS_RESPONSE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1919.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1919.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2274.ExternalCADModelLoadCase':
        '''ExternalCADModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2274.ExternalCADModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
