'''_6152.py

SynchroniserPartCompoundMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6085
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_PART_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'SynchroniserPartCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserPartCompoundMultiBodyDynamicsAnalysis',)


class SynchroniserPartCompoundMultiBodyDynamicsAnalysis(_6085.CouplingHalfCompoundMultiBodyDynamicsAnalysis):
    '''SynchroniserPartCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_PART_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserPartCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
