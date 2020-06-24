'''_2882.py

CVTCompoundSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _2851
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'CVTCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundSteadyStateSynchronousResponseAtASpeed',)


class CVTCompoundSteadyStateSynchronousResponseAtASpeed(_2851.BeltDriveCompoundSteadyStateSynchronousResponseAtASpeed):
    '''CVTCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CVT_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
