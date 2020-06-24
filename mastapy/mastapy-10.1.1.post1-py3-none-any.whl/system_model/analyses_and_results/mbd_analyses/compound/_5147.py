'''_5147.py

CouplingConnectionCompoundMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5170
from mastapy._internal.python_net import python_net_import

_COUPLING_CONNECTION_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'CouplingConnectionCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingConnectionCompoundMultiBodyDynamicsAnalysis',)


class CouplingConnectionCompoundMultiBodyDynamicsAnalysis(_5170.InterMountableComponentConnectionCompoundMultiBodyDynamicsAnalysis):
    '''CouplingConnectionCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_CONNECTION_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingConnectionCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
