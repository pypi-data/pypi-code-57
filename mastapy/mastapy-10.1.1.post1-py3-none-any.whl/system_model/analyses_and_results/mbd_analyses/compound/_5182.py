'''_5182.py

MountableComponentCompoundMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5134
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'MountableComponentCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponentCompoundMultiBodyDynamicsAnalysis',)


class MountableComponentCompoundMultiBodyDynamicsAnalysis(_5134.ComponentCompoundMultiBodyDynamicsAnalysis):
    '''MountableComponentCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _MOUNTABLE_COMPONENT_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountableComponentCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
