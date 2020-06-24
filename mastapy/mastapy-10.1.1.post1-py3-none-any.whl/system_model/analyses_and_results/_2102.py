'''_2102.py

SteadyStateSynchronousResponseataSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results import _2081
from mastapy._internal.python_net import python_net_import

_STEADY_STATE_SYNCHRONOUS_RESPONSEATA_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'SteadyStateSynchronousResponseataSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SteadyStateSynchronousResponseataSpeedAnalysis',)


class SteadyStateSynchronousResponseataSpeedAnalysis(_2081.SingleAnalysis):
    '''SteadyStateSynchronousResponseataSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _STEADY_STATE_SYNCHRONOUS_RESPONSEATA_SPEED_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SteadyStateSynchronousResponseataSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
