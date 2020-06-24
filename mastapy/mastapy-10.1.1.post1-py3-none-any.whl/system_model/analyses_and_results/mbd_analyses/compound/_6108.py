'''_6108.py

KlingelnbergCycloPalloidConicalGearCompoundMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6078
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'KlingelnbergCycloPalloidConicalGearCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearCompoundMultiBodyDynamicsAnalysis',)


class KlingelnbergCycloPalloidConicalGearCompoundMultiBodyDynamicsAnalysis(_6078.ConicalGearCompoundMultiBodyDynamicsAnalysis):
    '''KlingelnbergCycloPalloidConicalGearCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
