'''_5090.py

TorqueConverterConnectionMultiBodyDynamicsAnalysis
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5094, _5004
from mastapy.system_model.connections_and_sockets.couplings import _1904
from mastapy.system_model.analyses_and_results.static_loads import _6199
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'TorqueConverterConnectionMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionMultiBodyDynamicsAnalysis',)


class TorqueConverterConnectionMultiBodyDynamicsAnalysis(_5004.CouplingConnectionMultiBodyDynamicsAnalysis):
    '''TorqueConverterConnectionMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def pump_torque(self) -> 'float':
        '''float: 'PumpTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PumpTorque

    @property
    def turbine_torque(self) -> 'float':
        '''float: 'TurbineTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TurbineTorque

    @property
    def speed_ratio(self) -> 'float':
        '''float: 'SpeedRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpeedRatio

    @property
    def torque_ratio(self) -> 'float':
        '''float: 'TorqueRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TorqueRatio

    @property
    def capacity_factor_k(self) -> 'float':
        '''float: 'CapacityFactorK' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CapacityFactorK

    @property
    def inverse_capacity_factor_1k(self) -> 'float':
        '''float: 'InverseCapacityFactor1K' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InverseCapacityFactor1K

    @property
    def locked_torque(self) -> 'float':
        '''float: 'LockedTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LockedTorque

    @property
    def lock_up_viscous_torque(self) -> 'float':
        '''float: 'LockUpViscousTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LockUpViscousTorque

    @property
    def is_locked(self) -> 'bool':
        '''bool: 'IsLocked' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsLocked

    @property
    def percentage_applied_pressure(self) -> 'float':
        '''float: 'PercentageAppliedPressure' is the original name of this property.'''

        return self.wrapped.PercentageAppliedPressure

    @percentage_applied_pressure.setter
    def percentage_applied_pressure(self, value: 'float'):
        self.wrapped.PercentageAppliedPressure = float(value) if value else 0.0

    @property
    def locking_status(self) -> '_5094.TorqueConverterStatus':
        '''TorqueConverterStatus: 'LockingStatus' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.LockingStatus)
        return constructor.new(_5094.TorqueConverterStatus)(value) if value else None

    @property
    def lock_up_clutch_temperature(self) -> 'float':
        '''float: 'LockUpClutchTemperature' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LockUpClutchTemperature

    @property
    def power_loss(self) -> 'float':
        '''float: 'PowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PowerLoss

    @property
    def connection_design(self) -> '_1904.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1904.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6199.TorqueConverterConnectionLoadCase':
        '''TorqueConverterConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6199.TorqueConverterConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
