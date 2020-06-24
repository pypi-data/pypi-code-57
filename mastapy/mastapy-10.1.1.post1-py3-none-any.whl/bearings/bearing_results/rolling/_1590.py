'''_1590.py

InnerRaceFittingThermalResults
'''


from mastapy.bearings.bearing_results.rolling import _1679
from mastapy._internal.python_net import python_net_import

_INNER_RACE_FITTING_THERMAL_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'InnerRaceFittingThermalResults')


__docformat__ = 'restructuredtext en'
__all__ = ('InnerRaceFittingThermalResults',)


class InnerRaceFittingThermalResults(_1679.RaceFittingThermalResults):
    '''InnerRaceFittingThermalResults

    This is a mastapy class.
    '''

    TYPE = _INNER_RACE_FITTING_THERMAL_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'InnerRaceFittingThermalResults.TYPE'):
        super().__init__(instance_to_wrap)
