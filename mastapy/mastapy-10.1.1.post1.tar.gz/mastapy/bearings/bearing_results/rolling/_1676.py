'''_1676.py

OuterRaceFittingThermalResults
'''


from mastapy.bearings.bearing_results.rolling import _1679
from mastapy._internal.python_net import python_net_import

_OUTER_RACE_FITTING_THERMAL_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'OuterRaceFittingThermalResults')


__docformat__ = 'restructuredtext en'
__all__ = ('OuterRaceFittingThermalResults',)


class OuterRaceFittingThermalResults(_1679.RaceFittingThermalResults):
    '''OuterRaceFittingThermalResults

    This is a mastapy class.
    '''

    TYPE = _OUTER_RACE_FITTING_THERMAL_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OuterRaceFittingThermalResults.TYPE'):
        super().__init__(instance_to_wrap)
