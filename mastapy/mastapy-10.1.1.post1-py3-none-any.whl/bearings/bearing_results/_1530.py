'''_1530.py

LoadedNonLinearBearingResults
'''


from mastapy._internal import constructor
from mastapy.bearings.bearing_results import _1522
from mastapy._internal.python_net import python_net_import

_LOADED_NON_LINEAR_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedNonLinearBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedNonLinearBearingResults',)


class LoadedNonLinearBearingResults(_1522.LoadedBearingResults):
    '''LoadedNonLinearBearingResults

    This is a mastapy class.
    '''

    TYPE = _LOADED_NON_LINEAR_BEARING_RESULTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedNonLinearBearingResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def total_power_loss(self) -> 'float':
        '''float: 'TotalPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalPowerLoss

    @property
    def resistive_torque(self) -> 'float':
        '''float: 'ResistiveTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ResistiveTorque
