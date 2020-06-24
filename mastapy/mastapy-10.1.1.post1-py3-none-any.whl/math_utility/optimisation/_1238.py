'''_1238.py

OptimizationVariable
'''


from typing import List

from mastapy.utility.units_and_measurements import _1035
from mastapy._internal import constructor, conversion
from mastapy.utility.units_and_measurements.measurements import (
    _1280, _1281, _1282, _1283,
    _1284, _1285, _1286, _1287,
    _1288, _1289, _1290, _1291,
    _1292, _1293, _1294, _1295,
    _1296, _1297, _1298, _1299,
    _1300, _1301, _1302, _1303,
    _1304, _1305, _1306, _1307,
    _1308, _1309, _1310, _1311,
    _1312, _1313, _1314, _1315,
    _1316, _1317, _1318, _1319,
    _1320, _1321, _1322, _1323,
    _1071, _1324, _1325, _1326,
    _1327, _1328, _1329, _1330,
    _1331, _1332, _1333, _1334,
    _1335, _1336, _1337, _1338,
    _1072, _1339, _1340, _1341,
    _1342, _1343, _1344, _1345,
    _1346, _1347, _1348, _1349,
    _1350, _1351, _1352, _1353,
    _1354, _1355, _1356, _1357,
    _1358, _1359, _1360, _1361,
    _1362, _1363, _1364, _1365,
    _1366, _1367, _1368, _1369,
    _1370, _1371, _1372, _1373,
    _1374, _1375, _1376, _1377,
    _1378, _1379
)
from mastapy._internal.cast_exception import CastException
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_OPTIMIZATION_VARIABLE = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'OptimizationVariable')


__docformat__ = 'restructuredtext en'
__all__ = ('OptimizationVariable',)


class OptimizationVariable(_1.APIBase):
    '''OptimizationVariable

    This is a mastapy class.
    '''

    TYPE = _OPTIMIZATION_VARIABLE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'OptimizationVariable.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def measurement(self) -> '_1035.MeasurementBase':
        '''MeasurementBase: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1035.MeasurementBase)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_acceleration(self) -> '_1280.Acceleration':
        '''Acceleration: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Acceleration':
            raise CastException('Failed to cast measurement to Acceleration. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1280.Acceleration)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angle(self) -> '_1281.Angle':
        '''Angle: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Angle':
            raise CastException('Failed to cast measurement to Angle. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1281.Angle)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angle_per_unit_temperature(self) -> '_1282.AnglePerUnitTemperature':
        '''AnglePerUnitTemperature: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'AnglePerUnitTemperature':
            raise CastException('Failed to cast measurement to AnglePerUnitTemperature. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1282.AnglePerUnitTemperature)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angle_small(self) -> '_1283.AngleSmall':
        '''AngleSmall: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'AngleSmall':
            raise CastException('Failed to cast measurement to AngleSmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1283.AngleSmall)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angle_very_small(self) -> '_1284.AngleVerySmall':
        '''AngleVerySmall: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'AngleVerySmall':
            raise CastException('Failed to cast measurement to AngleVerySmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1284.AngleVerySmall)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angular_acceleration(self) -> '_1285.AngularAcceleration':
        '''AngularAcceleration: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'AngularAcceleration':
            raise CastException('Failed to cast measurement to AngularAcceleration. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1285.AngularAcceleration)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angular_compliance(self) -> '_1286.AngularCompliance':
        '''AngularCompliance: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'AngularCompliance':
            raise CastException('Failed to cast measurement to AngularCompliance. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1286.AngularCompliance)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angular_jerk(self) -> '_1287.AngularJerk':
        '''AngularJerk: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'AngularJerk':
            raise CastException('Failed to cast measurement to AngularJerk. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1287.AngularJerk)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angular_stiffness(self) -> '_1288.AngularStiffness':
        '''AngularStiffness: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'AngularStiffness':
            raise CastException('Failed to cast measurement to AngularStiffness. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1288.AngularStiffness)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angular_velocity(self) -> '_1289.AngularVelocity':
        '''AngularVelocity: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'AngularVelocity':
            raise CastException('Failed to cast measurement to AngularVelocity. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1289.AngularVelocity)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_area(self) -> '_1290.Area':
        '''Area: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Area':
            raise CastException('Failed to cast measurement to Area. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1290.Area)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_area_small(self) -> '_1291.AreaSmall':
        '''AreaSmall: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'AreaSmall':
            raise CastException('Failed to cast measurement to AreaSmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1291.AreaSmall)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_cycles(self) -> '_1292.Cycles':
        '''Cycles: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Cycles':
            raise CastException('Failed to cast measurement to Cycles. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1292.Cycles)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_damage_rate(self) -> '_1293.DamageRate':
        '''DamageRate: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'DamageRate':
            raise CastException('Failed to cast measurement to DamageRate. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1293.DamageRate)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_decibel(self) -> '_1294.Decibel':
        '''Decibel: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Decibel':
            raise CastException('Failed to cast measurement to Decibel. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1294.Decibel)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_density(self) -> '_1295.Density':
        '''Density: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Density':
            raise CastException('Failed to cast measurement to Density. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1295.Density)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_energy(self) -> '_1296.Energy':
        '''Energy: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Energy':
            raise CastException('Failed to cast measurement to Energy. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1296.Energy)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_energy_per_unit_area(self) -> '_1297.EnergyPerUnitArea':
        '''EnergyPerUnitArea: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'EnergyPerUnitArea':
            raise CastException('Failed to cast measurement to EnergyPerUnitArea. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1297.EnergyPerUnitArea)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_energy_per_unit_area_small(self) -> '_1298.EnergyPerUnitAreaSmall':
        '''EnergyPerUnitAreaSmall: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'EnergyPerUnitAreaSmall':
            raise CastException('Failed to cast measurement to EnergyPerUnitAreaSmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1298.EnergyPerUnitAreaSmall)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_energy_small(self) -> '_1299.EnergySmall':
        '''EnergySmall: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'EnergySmall':
            raise CastException('Failed to cast measurement to EnergySmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1299.EnergySmall)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_enum(self) -> '_1300.Enum':
        '''Enum: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Enum':
            raise CastException('Failed to cast measurement to Enum. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1300.Enum)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_flow_rate(self) -> '_1301.FlowRate':
        '''FlowRate: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'FlowRate':
            raise CastException('Failed to cast measurement to FlowRate. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1301.FlowRate)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_force(self) -> '_1302.Force':
        '''Force: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Force':
            raise CastException('Failed to cast measurement to Force. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1302.Force)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_force_per_unit_length(self) -> '_1303.ForcePerUnitLength':
        '''ForcePerUnitLength: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'ForcePerUnitLength':
            raise CastException('Failed to cast measurement to ForcePerUnitLength. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1303.ForcePerUnitLength)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_force_per_unit_pressure(self) -> '_1304.ForcePerUnitPressure':
        '''ForcePerUnitPressure: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'ForcePerUnitPressure':
            raise CastException('Failed to cast measurement to ForcePerUnitPressure. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1304.ForcePerUnitPressure)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_force_per_unit_temperature(self) -> '_1305.ForcePerUnitTemperature':
        '''ForcePerUnitTemperature: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'ForcePerUnitTemperature':
            raise CastException('Failed to cast measurement to ForcePerUnitTemperature. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1305.ForcePerUnitTemperature)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_frequency(self) -> '_1306.Frequency':
        '''Frequency: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Frequency':
            raise CastException('Failed to cast measurement to Frequency. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1306.Frequency)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_fuel_consumption_engine(self) -> '_1307.FuelConsumptionEngine':
        '''FuelConsumptionEngine: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'FuelConsumptionEngine':
            raise CastException('Failed to cast measurement to FuelConsumptionEngine. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1307.FuelConsumptionEngine)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_fuel_efficiency_vehicle(self) -> '_1308.FuelEfficiencyVehicle':
        '''FuelEfficiencyVehicle: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'FuelEfficiencyVehicle':
            raise CastException('Failed to cast measurement to FuelEfficiencyVehicle. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1308.FuelEfficiencyVehicle)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_gradient(self) -> '_1309.Gradient':
        '''Gradient: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Gradient':
            raise CastException('Failed to cast measurement to Gradient. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1309.Gradient)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_heat_conductivity(self) -> '_1310.HeatConductivity':
        '''HeatConductivity: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'HeatConductivity':
            raise CastException('Failed to cast measurement to HeatConductivity. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1310.HeatConductivity)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_heat_transfer(self) -> '_1311.HeatTransfer':
        '''HeatTransfer: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'HeatTransfer':
            raise CastException('Failed to cast measurement to HeatTransfer. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1311.HeatTransfer)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_heat_transfer_coefficient_for_plastic_gear_tooth(self) -> '_1312.HeatTransferCoefficientForPlasticGearTooth':
        '''HeatTransferCoefficientForPlasticGearTooth: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'HeatTransferCoefficientForPlasticGearTooth':
            raise CastException('Failed to cast measurement to HeatTransferCoefficientForPlasticGearTooth. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1312.HeatTransferCoefficientForPlasticGearTooth)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_heat_transfer_resistance(self) -> '_1313.HeatTransferResistance':
        '''HeatTransferResistance: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'HeatTransferResistance':
            raise CastException('Failed to cast measurement to HeatTransferResistance. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1313.HeatTransferResistance)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_impulse(self) -> '_1314.Impulse':
        '''Impulse: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Impulse':
            raise CastException('Failed to cast measurement to Impulse. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1314.Impulse)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_index(self) -> '_1315.Index':
        '''Index: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Index':
            raise CastException('Failed to cast measurement to Index. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1315.Index)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_integer(self) -> '_1316.Integer':
        '''Integer: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Integer':
            raise CastException('Failed to cast measurement to Integer. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1316.Integer)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_inverse_short_length(self) -> '_1317.InverseShortLength':
        '''InverseShortLength: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'InverseShortLength':
            raise CastException('Failed to cast measurement to InverseShortLength. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1317.InverseShortLength)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_inverse_short_time(self) -> '_1318.InverseShortTime':
        '''InverseShortTime: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'InverseShortTime':
            raise CastException('Failed to cast measurement to InverseShortTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1318.InverseShortTime)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_jerk(self) -> '_1319.Jerk':
        '''Jerk: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Jerk':
            raise CastException('Failed to cast measurement to Jerk. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1319.Jerk)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_kinematic_viscosity(self) -> '_1320.KinematicViscosity':
        '''KinematicViscosity: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'KinematicViscosity':
            raise CastException('Failed to cast measurement to KinematicViscosity. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1320.KinematicViscosity)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_length_long(self) -> '_1321.LengthLong':
        '''LengthLong: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'LengthLong':
            raise CastException('Failed to cast measurement to LengthLong. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1321.LengthLong)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_length_medium(self) -> '_1322.LengthMedium':
        '''LengthMedium: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'LengthMedium':
            raise CastException('Failed to cast measurement to LengthMedium. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1322.LengthMedium)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_length_per_unit_temperature(self) -> '_1323.LengthPerUnitTemperature':
        '''LengthPerUnitTemperature: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'LengthPerUnitTemperature':
            raise CastException('Failed to cast measurement to LengthPerUnitTemperature. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1323.LengthPerUnitTemperature)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_length_short(self) -> '_1071.LengthShort':
        '''LengthShort: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'LengthShort':
            raise CastException('Failed to cast measurement to LengthShort. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1071.LengthShort)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_length_to_the_fourth(self) -> '_1324.LengthToTheFourth':
        '''LengthToTheFourth: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'LengthToTheFourth':
            raise CastException('Failed to cast measurement to LengthToTheFourth. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1324.LengthToTheFourth)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_length_very_long(self) -> '_1325.LengthVeryLong':
        '''LengthVeryLong: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'LengthVeryLong':
            raise CastException('Failed to cast measurement to LengthVeryLong. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1325.LengthVeryLong)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_length_very_short(self) -> '_1326.LengthVeryShort':
        '''LengthVeryShort: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'LengthVeryShort':
            raise CastException('Failed to cast measurement to LengthVeryShort. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1326.LengthVeryShort)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_length_very_short_per_length_short(self) -> '_1327.LengthVeryShortPerLengthShort':
        '''LengthVeryShortPerLengthShort: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'LengthVeryShortPerLengthShort':
            raise CastException('Failed to cast measurement to LengthVeryShortPerLengthShort. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1327.LengthVeryShortPerLengthShort)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_linear_angular_damping(self) -> '_1328.LinearAngularDamping':
        '''LinearAngularDamping: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'LinearAngularDamping':
            raise CastException('Failed to cast measurement to LinearAngularDamping. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1328.LinearAngularDamping)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_linear_angular_stiffness_cross_term(self) -> '_1329.LinearAngularStiffnessCrossTerm':
        '''LinearAngularStiffnessCrossTerm: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'LinearAngularStiffnessCrossTerm':
            raise CastException('Failed to cast measurement to LinearAngularStiffnessCrossTerm. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1329.LinearAngularStiffnessCrossTerm)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_linear_damping(self) -> '_1330.LinearDamping':
        '''LinearDamping: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'LinearDamping':
            raise CastException('Failed to cast measurement to LinearDamping. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1330.LinearDamping)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_linear_flexibility(self) -> '_1331.LinearFlexibility':
        '''LinearFlexibility: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'LinearFlexibility':
            raise CastException('Failed to cast measurement to LinearFlexibility. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1331.LinearFlexibility)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_linear_stiffness(self) -> '_1332.LinearStiffness':
        '''LinearStiffness: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'LinearStiffness':
            raise CastException('Failed to cast measurement to LinearStiffness. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1332.LinearStiffness)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_mass(self) -> '_1333.Mass':
        '''Mass: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Mass':
            raise CastException('Failed to cast measurement to Mass. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1333.Mass)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_mass_per_unit_length(self) -> '_1334.MassPerUnitLength':
        '''MassPerUnitLength: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'MassPerUnitLength':
            raise CastException('Failed to cast measurement to MassPerUnitLength. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1334.MassPerUnitLength)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_mass_per_unit_time(self) -> '_1335.MassPerUnitTime':
        '''MassPerUnitTime: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'MassPerUnitTime':
            raise CastException('Failed to cast measurement to MassPerUnitTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1335.MassPerUnitTime)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_moment_of_inertia(self) -> '_1336.MomentOfInertia':
        '''MomentOfInertia: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'MomentOfInertia':
            raise CastException('Failed to cast measurement to MomentOfInertia. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1336.MomentOfInertia)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_moment_of_inertia_per_unit_length(self) -> '_1337.MomentOfInertiaPerUnitLength':
        '''MomentOfInertiaPerUnitLength: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'MomentOfInertiaPerUnitLength':
            raise CastException('Failed to cast measurement to MomentOfInertiaPerUnitLength. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1337.MomentOfInertiaPerUnitLength)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_moment_per_unit_pressure(self) -> '_1338.MomentPerUnitPressure':
        '''MomentPerUnitPressure: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'MomentPerUnitPressure':
            raise CastException('Failed to cast measurement to MomentPerUnitPressure. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1338.MomentPerUnitPressure)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_number(self) -> '_1072.Number':
        '''Number: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Number':
            raise CastException('Failed to cast measurement to Number. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1072.Number)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_power(self) -> '_1339.Power':
        '''Power: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Power':
            raise CastException('Failed to cast measurement to Power. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1339.Power)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_power_per_small_area(self) -> '_1340.PowerPerSmallArea':
        '''PowerPerSmallArea: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'PowerPerSmallArea':
            raise CastException('Failed to cast measurement to PowerPerSmallArea. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1340.PowerPerSmallArea)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_power_small(self) -> '_1341.PowerSmall':
        '''PowerSmall: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'PowerSmall':
            raise CastException('Failed to cast measurement to PowerSmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1341.PowerSmall)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_power_small_per_unit_time(self) -> '_1342.PowerSmallPerUnitTime':
        '''PowerSmallPerUnitTime: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'PowerSmallPerUnitTime':
            raise CastException('Failed to cast measurement to PowerSmallPerUnitTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1342.PowerSmallPerUnitTime)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_pressure_velocity_product(self) -> '_1343.PressureVelocityProduct':
        '''PressureVelocityProduct: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'PressureVelocityProduct':
            raise CastException('Failed to cast measurement to PressureVelocityProduct. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1343.PressureVelocityProduct)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_pressure_viscosity_coefficient(self) -> '_1344.PressureViscosityCoefficient':
        '''PressureViscosityCoefficient: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'PressureViscosityCoefficient':
            raise CastException('Failed to cast measurement to PressureViscosityCoefficient. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1344.PressureViscosityCoefficient)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_price(self) -> '_1345.Price':
        '''Price: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Price':
            raise CastException('Failed to cast measurement to Price. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1345.Price)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_quadratic_angular_damping(self) -> '_1346.QuadraticAngularDamping':
        '''QuadraticAngularDamping: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'QuadraticAngularDamping':
            raise CastException('Failed to cast measurement to QuadraticAngularDamping. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1346.QuadraticAngularDamping)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_quadratic_drag(self) -> '_1347.QuadraticDrag':
        '''QuadraticDrag: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'QuadraticDrag':
            raise CastException('Failed to cast measurement to QuadraticDrag. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1347.QuadraticDrag)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_rescaled_measurement(self) -> '_1348.RescaledMeasurement':
        '''RescaledMeasurement: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'RescaledMeasurement':
            raise CastException('Failed to cast measurement to RescaledMeasurement. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1348.RescaledMeasurement)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_rotatum(self) -> '_1349.Rotatum':
        '''Rotatum: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Rotatum':
            raise CastException('Failed to cast measurement to Rotatum. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1349.Rotatum)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_safety_factor(self) -> '_1350.SafetyFactor':
        '''SafetyFactor: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'SafetyFactor':
            raise CastException('Failed to cast measurement to SafetyFactor. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1350.SafetyFactor)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_specific_acoustic_impedance(self) -> '_1351.SpecificAcousticImpedance':
        '''SpecificAcousticImpedance: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'SpecificAcousticImpedance':
            raise CastException('Failed to cast measurement to SpecificAcousticImpedance. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1351.SpecificAcousticImpedance)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_specific_heat(self) -> '_1352.SpecificHeat':
        '''SpecificHeat: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'SpecificHeat':
            raise CastException('Failed to cast measurement to SpecificHeat. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1352.SpecificHeat)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_square_root_of_unit_force_per_unit_area(self) -> '_1353.SquareRootOfUnitForcePerUnitArea':
        '''SquareRootOfUnitForcePerUnitArea: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'SquareRootOfUnitForcePerUnitArea':
            raise CastException('Failed to cast measurement to SquareRootOfUnitForcePerUnitArea. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1353.SquareRootOfUnitForcePerUnitArea)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_stiffness_per_unit_face_width(self) -> '_1354.StiffnessPerUnitFaceWidth':
        '''StiffnessPerUnitFaceWidth: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'StiffnessPerUnitFaceWidth':
            raise CastException('Failed to cast measurement to StiffnessPerUnitFaceWidth. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1354.StiffnessPerUnitFaceWidth)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_stress(self) -> '_1355.Stress':
        '''Stress: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Stress':
            raise CastException('Failed to cast measurement to Stress. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1355.Stress)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_temperature(self) -> '_1356.Temperature':
        '''Temperature: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Temperature':
            raise CastException('Failed to cast measurement to Temperature. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1356.Temperature)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_temperature_difference(self) -> '_1357.TemperatureDifference':
        '''TemperatureDifference: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'TemperatureDifference':
            raise CastException('Failed to cast measurement to TemperatureDifference. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1357.TemperatureDifference)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_temperature_per_unit_time(self) -> '_1358.TemperaturePerUnitTime':
        '''TemperaturePerUnitTime: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'TemperaturePerUnitTime':
            raise CastException('Failed to cast measurement to TemperaturePerUnitTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1358.TemperaturePerUnitTime)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_text(self) -> '_1359.Text':
        '''Text: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Text':
            raise CastException('Failed to cast measurement to Text. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1359.Text)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_thermal_contact_coefficient(self) -> '_1360.ThermalContactCoefficient':
        '''ThermalContactCoefficient: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'ThermalContactCoefficient':
            raise CastException('Failed to cast measurement to ThermalContactCoefficient. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1360.ThermalContactCoefficient)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_thermal_expansion_coefficient(self) -> '_1361.ThermalExpansionCoefficient':
        '''ThermalExpansionCoefficient: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'ThermalExpansionCoefficient':
            raise CastException('Failed to cast measurement to ThermalExpansionCoefficient. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1361.ThermalExpansionCoefficient)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_thermo_elastic_factor(self) -> '_1362.ThermoElasticFactor':
        '''ThermoElasticFactor: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'ThermoElasticFactor':
            raise CastException('Failed to cast measurement to ThermoElasticFactor. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1362.ThermoElasticFactor)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_time(self) -> '_1363.Time':
        '''Time: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Time':
            raise CastException('Failed to cast measurement to Time. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1363.Time)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_time_short(self) -> '_1364.TimeShort':
        '''TimeShort: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'TimeShort':
            raise CastException('Failed to cast measurement to TimeShort. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1364.TimeShort)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_time_very_short(self) -> '_1365.TimeVeryShort':
        '''TimeVeryShort: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'TimeVeryShort':
            raise CastException('Failed to cast measurement to TimeVeryShort. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1365.TimeVeryShort)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_torque(self) -> '_1366.Torque':
        '''Torque: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Torque':
            raise CastException('Failed to cast measurement to Torque. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1366.Torque)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_torque_converter_inverse_k(self) -> '_1367.TorqueConverterInverseK':
        '''TorqueConverterInverseK: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'TorqueConverterInverseK':
            raise CastException('Failed to cast measurement to TorqueConverterInverseK. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1367.TorqueConverterInverseK)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_torque_converter_k(self) -> '_1368.TorqueConverterK':
        '''TorqueConverterK: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'TorqueConverterK':
            raise CastException('Failed to cast measurement to TorqueConverterK. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1368.TorqueConverterK)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_torque_per_unit_temperature(self) -> '_1369.TorquePerUnitTemperature':
        '''TorquePerUnitTemperature: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'TorquePerUnitTemperature':
            raise CastException('Failed to cast measurement to TorquePerUnitTemperature. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1369.TorquePerUnitTemperature)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_velocity(self) -> '_1370.Velocity':
        '''Velocity: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Velocity':
            raise CastException('Failed to cast measurement to Velocity. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1370.Velocity)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_velocity_small(self) -> '_1371.VelocitySmall':
        '''VelocitySmall: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'VelocitySmall':
            raise CastException('Failed to cast measurement to VelocitySmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1371.VelocitySmall)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_viscosity(self) -> '_1372.Viscosity':
        '''Viscosity: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Viscosity':
            raise CastException('Failed to cast measurement to Viscosity. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1372.Viscosity)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_voltage(self) -> '_1373.Voltage':
        '''Voltage: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Voltage':
            raise CastException('Failed to cast measurement to Voltage. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1373.Voltage)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_volume(self) -> '_1374.Volume':
        '''Volume: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Volume':
            raise CastException('Failed to cast measurement to Volume. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1374.Volume)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_wear_coefficient(self) -> '_1375.WearCoefficient':
        '''WearCoefficient: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'WearCoefficient':
            raise CastException('Failed to cast measurement to WearCoefficient. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1375.WearCoefficient)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_yank(self) -> '_1376.Yank':
        '''Yank: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Yank':
            raise CastException('Failed to cast measurement to Yank. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1376.Yank)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_damage(self) -> '_1377.Damage':
        '''Damage: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Damage':
            raise CastException('Failed to cast measurement to Damage. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1377.Damage)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_percentage(self) -> '_1378.Percentage':
        '''Percentage: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Percentage':
            raise CastException('Failed to cast measurement to Percentage. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1378.Percentage)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_pressure(self) -> '_1379.Pressure':
        '''Pressure: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Measurement.__class__.__qualname__ != 'Pressure':
            raise CastException('Failed to cast measurement to Pressure. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1379.Pressure)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def results(self) -> 'List[float]':
        '''List[float]: 'Results' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Results, float)
        return value
