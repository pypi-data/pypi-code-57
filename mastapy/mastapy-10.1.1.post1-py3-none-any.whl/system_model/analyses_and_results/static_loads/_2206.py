'''_2206.py

TorqueConverterLoadCase
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.system_model.analyses_and_results.mbd_analyses import _6028
from mastapy.system_model.part_model.couplings import _1991
from mastapy.system_model.analyses_and_results.static_loads import _2178
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'TorqueConverterLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterLoadCase',)


class TorqueConverterLoadCase(_2178.CouplingLoadCase):
    '''TorqueConverterLoadCase

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_LOAD_CASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def time_to_change_locking_state(self) -> 'float':
        '''float: 'TimeToChangeLockingState' is the original name of this property.'''

        return self.wrapped.TimeToChangeLockingState

    @time_to_change_locking_state.setter
    def time_to_change_locking_state(self, value: 'float'):
        self.wrapped.TimeToChangeLockingState = float(value) if value else 0.0

    @property
    def initially_locked(self) -> 'bool':
        '''bool: 'InitiallyLocked' is the original name of this property.'''

        return self.wrapped.InitiallyLocked

    @initially_locked.setter
    def initially_locked(self, value: 'bool'):
        self.wrapped.InitiallyLocked = bool(value) if value else False

    @property
    def locking_speed_ratio_threshold(self) -> 'float':
        '''float: 'LockingSpeedRatioThreshold' is the original name of this property.'''

        return self.wrapped.LockingSpeedRatioThreshold

    @locking_speed_ratio_threshold.setter
    def locking_speed_ratio_threshold(self, value: 'float'):
        self.wrapped.LockingSpeedRatioThreshold = float(value) if value else 0.0

    @property
    def time_for_full_clutch_pressure(self) -> 'float':
        '''float: 'TimeForFullClutchPressure' is the original name of this property.'''

        return self.wrapped.TimeForFullClutchPressure

    @time_for_full_clutch_pressure.setter
    def time_for_full_clutch_pressure(self, value: 'float'):
        self.wrapped.TimeForFullClutchPressure = float(value) if value else 0.0

    @property
    def lock_up_clutch_pressure_for_no_torque_converter_operation(self) -> 'float':
        '''float: 'LockUpClutchPressureForNoTorqueConverterOperation' is the original name of this property.'''

        return self.wrapped.LockUpClutchPressureForNoTorqueConverterOperation

    @lock_up_clutch_pressure_for_no_torque_converter_operation.setter
    def lock_up_clutch_pressure_for_no_torque_converter_operation(self, value: 'float'):
        self.wrapped.LockUpClutchPressureForNoTorqueConverterOperation = float(value) if value else 0.0

    @property
    def lock_up_clutch_rule(self) -> 'enum_with_selected_value.EnumWithSelectedValue_TorqueConverterLockupRule':
        '''enum_with_selected_value.EnumWithSelectedValue_TorqueConverterLockupRule: 'LockUpClutchRule' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_TorqueConverterLockupRule)(self.wrapped.LockUpClutchRule) if self.wrapped.LockUpClutchRule else None

    @lock_up_clutch_rule.setter
    def lock_up_clutch_rule(self, value: 'enum_with_selected_value.EnumWithSelectedValue_TorqueConverterLockupRule.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_TorqueConverterLockupRule.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_TorqueConverterLockupRule.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.LockUpClutchRule = value

    @property
    def vehicle_speed_to_unlock(self) -> 'float':
        '''float: 'VehicleSpeedToUnlock' is the original name of this property.'''

        return self.wrapped.VehicleSpeedToUnlock

    @vehicle_speed_to_unlock.setter
    def vehicle_speed_to_unlock(self, value: 'float'):
        self.wrapped.VehicleSpeedToUnlock = float(value) if value else 0.0

    @property
    def transient_time_to_change_locking_status(self) -> 'float':
        '''float: 'TransientTimeToChangeLockingStatus' is the original name of this property.'''

        return self.wrapped.TransientTimeToChangeLockingStatus

    @transient_time_to_change_locking_status.setter
    def transient_time_to_change_locking_status(self, value: 'float'):
        self.wrapped.TransientTimeToChangeLockingStatus = float(value) if value else 0.0

    @property
    def initial_lock_up_clutch_temperature(self) -> 'float':
        '''float: 'InitialLockUpClutchTemperature' is the original name of this property.'''

        return self.wrapped.InitialLockUpClutchTemperature

    @initial_lock_up_clutch_temperature.setter
    def initial_lock_up_clutch_temperature(self, value: 'float'):
        self.wrapped.InitialLockUpClutchTemperature = float(value) if value else 0.0

    @property
    def assembly_design(self) -> '_1991.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1991.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
