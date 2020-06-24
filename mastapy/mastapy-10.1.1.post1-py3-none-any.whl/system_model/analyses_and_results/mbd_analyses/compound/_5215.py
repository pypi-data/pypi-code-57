'''_5215.py

StraightBevelSunGearCompoundMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5208
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'StraightBevelSunGearCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearCompoundMultiBodyDynamicsAnalysis',)


class StraightBevelSunGearCompoundMultiBodyDynamicsAnalysis(_5208.StraightBevelDiffGearCompoundMultiBodyDynamicsAnalysis):
    '''StraightBevelSunGearCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
