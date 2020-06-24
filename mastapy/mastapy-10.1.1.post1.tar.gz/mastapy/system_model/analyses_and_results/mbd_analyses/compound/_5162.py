'''_5162.py

GearCompoundMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5182
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'GearCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundMultiBodyDynamicsAnalysis',)


class GearCompoundMultiBodyDynamicsAnalysis(_5182.MountableComponentCompoundMultiBodyDynamicsAnalysis):
    '''GearCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
