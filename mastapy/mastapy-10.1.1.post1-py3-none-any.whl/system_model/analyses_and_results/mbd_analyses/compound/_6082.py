'''_6082.py

ConnectorCompoundMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6119
from mastapy._internal.python_net import python_net_import

_CONNECTOR_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'ConnectorCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorCompoundMultiBodyDynamicsAnalysis',)


class ConnectorCompoundMultiBodyDynamicsAnalysis(_6119.MountableComponentCompoundMultiBodyDynamicsAnalysis):
    '''ConnectorCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectorCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
