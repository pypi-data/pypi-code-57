'''_2132.py

CompoundSteadyStateSynchronousResponseonaShaftAnalysis
'''


from mastapy.system_model.analyses_and_results import _2080
from mastapy._internal.python_net import python_net_import

_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSEONA_SHAFT_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundSteadyStateSynchronousResponseonaShaftAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundSteadyStateSynchronousResponseonaShaftAnalysis',)


class CompoundSteadyStateSynchronousResponseonaShaftAnalysis(_2080.CompoundAnalysis):
    '''CompoundSteadyStateSynchronousResponseonaShaftAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSEONA_SHAFT_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundSteadyStateSynchronousResponseonaShaftAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
