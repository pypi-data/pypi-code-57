'''_3446.py

StraightBevelSunGearCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3439
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'StraightBevelSunGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearCompoundPowerFlow',)


class StraightBevelSunGearCompoundPowerFlow(_3439.StraightBevelDiffGearCompoundPowerFlow):
    '''StraightBevelSunGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
