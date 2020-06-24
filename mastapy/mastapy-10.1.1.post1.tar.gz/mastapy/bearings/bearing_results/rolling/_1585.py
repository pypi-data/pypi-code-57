'''_1585.py

LoadedNeedleRollerBearingRow
'''


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling import _1584, _1573
from mastapy._internal.python_net import python_net_import

_LOADED_NEEDLE_ROLLER_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedNeedleRollerBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedNeedleRollerBearingRow',)


class LoadedNeedleRollerBearingRow(_1573.LoadedCylindricalRollerBearingRow):
    '''LoadedNeedleRollerBearingRow

    This is a mastapy class.
    '''

    TYPE = _LOADED_NEEDLE_ROLLER_BEARING_ROW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedNeedleRollerBearingRow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def load_dependent_power_loss(self) -> 'float':
        '''float: 'LoadDependentPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadDependentPowerLoss

    @property
    def speed_dependent_power_loss(self) -> 'float':
        '''float: 'SpeedDependentPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpeedDependentPowerLoss

    @property
    def total_power_loss(self) -> 'float':
        '''float: 'TotalPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalPowerLoss

    @property
    def total_power_loss_traction_coefficient(self) -> 'float':
        '''float: 'TotalPowerLossTractionCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalPowerLossTractionCoefficient

    @property
    def load_dependent_power_loss_traction_coefficient(self) -> 'float':
        '''float: 'LoadDependentPowerLossTractionCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadDependentPowerLossTractionCoefficient

    @property
    def speed_dependent_power_loss_traction_coefficient(self) -> 'float':
        '''float: 'SpeedDependentPowerLossTractionCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpeedDependentPowerLossTractionCoefficient

    @property
    def loaded_bearing(self) -> '_1584.LoadedNeedleRollerBearingResults':
        '''LoadedNeedleRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1584.LoadedNeedleRollerBearingResults)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None
