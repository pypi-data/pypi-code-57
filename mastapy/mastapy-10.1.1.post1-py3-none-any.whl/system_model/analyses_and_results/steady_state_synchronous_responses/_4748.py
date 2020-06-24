'''_4748.py

SteadyStateSynchronousResponse
'''


from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3376
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.analysis_cases import _4863
from mastapy._internal.python_net import python_net_import

_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'SteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('SteadyStateSynchronousResponse',)


class SteadyStateSynchronousResponse(_4863.CompoundAnalysisCase):
    '''SteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _STEADY_STATE_SYNCHRONOUS_RESPONSE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def steady_state_analysis_options(self) -> '_3376.SteadyStateSynchronousResponseOptions':
        '''SteadyStateSynchronousResponseOptions: 'SteadyStateAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3376.SteadyStateSynchronousResponseOptions)(self.wrapped.SteadyStateAnalysisOptions) if self.wrapped.SteadyStateAnalysisOptions else None
