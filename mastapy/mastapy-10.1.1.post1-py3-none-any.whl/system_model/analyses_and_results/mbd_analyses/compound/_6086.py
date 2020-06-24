'''_6086.py

CVTBeltConnectionCompoundMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6055
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'CVTBeltConnectionCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionCompoundMultiBodyDynamicsAnalysis',)


class CVTBeltConnectionCompoundMultiBodyDynamicsAnalysis(_6055.BeltConnectionCompoundMultiBodyDynamicsAnalysis):
    '''CVTBeltConnectionCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
