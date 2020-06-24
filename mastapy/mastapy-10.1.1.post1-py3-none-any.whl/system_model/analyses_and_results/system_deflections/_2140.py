'''_2140.py

AssemblySystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _1904
from mastapy.system_model.analyses_and_results.static_loads import _2277
from mastapy.nodal_analysis import _24
from mastapy.shafts import _26
from mastapy.gears.analysis import _1123
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2141, _2143, _2145, _2153,
    _2152, _2156, _2162, _2164,
    _2181, _2374, _2311, _2275,
    _2337, _2280, _2345, _2349,
    _2282, _2284, _2288, _2292,
    _2294, _2296, _2187, _2191,
    _2066, _2354, _2193, _2358,
    _2362, _2197, _2205, _2302,
    _2167, _2170, _2136, _2215,
    _2158, _2286, _2261, _2135
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'AssemblySystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblySystemDeflection',)


class AssemblySystemDeflection(_2135.AbstractAssemblySystemDeflection):
    '''AssemblySystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblySystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def overall_bearing_reliability(self) -> 'float':
        '''float: 'OverallBearingReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallBearingReliability

    @property
    def overall_shaft_reliability(self) -> 'float':
        '''float: 'OverallShaftReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallShaftReliability

    @property
    def overall_gear_reliability(self) -> 'float':
        '''float: 'OverallGearReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallGearReliability

    @property
    def overall_oil_seal_reliability(self) -> 'float':
        '''float: 'OverallOilSealReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallOilSealReliability

    @property
    def overall_system_reliability(self) -> 'float':
        '''float: 'OverallSystemReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallSystemReliability

    @property
    def assembly_design(self) -> '_1904.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1904.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2277.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2277.AssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def analysis_settings(self) -> '_24.AnalysisSettings':
        '''AnalysisSettings: 'AnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_24.AnalysisSettings)(self.wrapped.AnalysisSettings) if self.wrapped.AnalysisSettings else None

    @property
    def shaft_settings(self) -> '_26.ShaftSettings':
        '''ShaftSettings: 'ShaftSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_26.ShaftSettings)(self.wrapped.ShaftSettings) if self.wrapped.ShaftSettings else None

    @property
    def rating_for_all_gear_sets(self) -> '_1123.GearSetGroupDutyCycle':
        '''GearSetGroupDutyCycle: 'RatingForAllGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1123.GearSetGroupDutyCycle)(self.wrapped.RatingForAllGearSets) if self.wrapped.RatingForAllGearSets else None

    @property
    def bearings(self) -> 'List[_2141.BearingSystemDeflection]':
        '''List[BearingSystemDeflection]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_2141.BearingSystemDeflection))
        return value

    @property
    def belt_drives(self) -> 'List[_2143.BeltDriveSystemDeflection]':
        '''List[BeltDriveSystemDeflection]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_2143.BeltDriveSystemDeflection))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_2145.BevelDifferentialGearSetSystemDeflection]':
        '''List[BevelDifferentialGearSetSystemDeflection]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_2145.BevelDifferentialGearSetSystemDeflection))
        return value

    @property
    def bolts(self) -> 'List[_2153.BoltSystemDeflection]':
        '''List[BoltSystemDeflection]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_2153.BoltSystemDeflection))
        return value

    @property
    def bolted_joints(self) -> 'List[_2152.BoltedJointSystemDeflection]':
        '''List[BoltedJointSystemDeflection]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_2152.BoltedJointSystemDeflection))
        return value

    @property
    def clutches(self) -> 'List[_2156.ClutchSystemDeflection]':
        '''List[ClutchSystemDeflection]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_2156.ClutchSystemDeflection))
        return value

    @property
    def concept_couplings(self) -> 'List[_2162.ConceptCouplingSystemDeflection]':
        '''List[ConceptCouplingSystemDeflection]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_2162.ConceptCouplingSystemDeflection))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_2164.ConceptGearSetSystemDeflection]':
        '''List[ConceptGearSetSystemDeflection]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_2164.ConceptGearSetSystemDeflection))
        return value

    @property
    def cv_ts(self) -> 'List[_2181.CVTSystemDeflection]':
        '''List[CVTSystemDeflection]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_2181.CVTSystemDeflection))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_2374.CylindricalGearSetSystemDeflection]':
        '''List[CylindricalGearSetSystemDeflection]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_2374.CylindricalGearSetSystemDeflection))
        return value

    @property
    def face_gear_sets(self) -> 'List[_2311.FaceGearSetSystemDeflection]':
        '''List[FaceGearSetSystemDeflection]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_2311.FaceGearSetSystemDeflection))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_2275.FlexiblePinAssemblySystemDeflection]':
        '''List[FlexiblePinAssemblySystemDeflection]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_2275.FlexiblePinAssemblySystemDeflection))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_2337.HypoidGearSetSystemDeflection]':
        '''List[HypoidGearSetSystemDeflection]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_2337.HypoidGearSetSystemDeflection))
        return value

    @property
    def imported_fe_components(self) -> 'List[_2280.ImportedFEComponentSystemDeflection]':
        '''List[ImportedFEComponentSystemDeflection]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_2280.ImportedFEComponentSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_2345.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetSystemDeflection]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_2345.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_2349.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_2349.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection))
        return value

    @property
    def mass_discs(self) -> 'List[_2282.MassDiscSystemDeflection]':
        '''List[MassDiscSystemDeflection]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_2282.MassDiscSystemDeflection))
        return value

    @property
    def measurement_components(self) -> 'List[_2284.MeasurementComponentSystemDeflection]':
        '''List[MeasurementComponentSystemDeflection]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_2284.MeasurementComponentSystemDeflection))
        return value

    @property
    def oil_seals(self) -> 'List[_2288.OilSealSystemDeflection]':
        '''List[OilSealSystemDeflection]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_2288.OilSealSystemDeflection))
        return value

    @property
    def planet_carriers(self) -> 'List[_2292.PlanetCarrierSystemDeflection]':
        '''List[PlanetCarrierSystemDeflection]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_2292.PlanetCarrierSystemDeflection))
        return value

    @property
    def point_loads(self) -> 'List[_2294.PointLoadSystemDeflection]':
        '''List[PointLoadSystemDeflection]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_2294.PointLoadSystemDeflection))
        return value

    @property
    def power_loads(self) -> 'List[_2296.PowerLoadSystemDeflection]':
        '''List[PowerLoadSystemDeflection]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_2296.PowerLoadSystemDeflection))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_2187.ShaftHubConnectionSystemDeflection]':
        '''List[ShaftHubConnectionSystemDeflection]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_2187.ShaftHubConnectionSystemDeflection))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_2191.RollingRingAssemblySystemDeflection]':
        '''List[RollingRingAssemblySystemDeflection]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_2191.RollingRingAssemblySystemDeflection))
        return value

    @property
    def shafts(self) -> 'List[_2066.ShaftSystemDeflection]':
        '''List[ShaftSystemDeflection]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_2066.ShaftSystemDeflection))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_2354.SpiralBevelGearSetSystemDeflection]':
        '''List[SpiralBevelGearSetSystemDeflection]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_2354.SpiralBevelGearSetSystemDeflection))
        return value

    @property
    def spring_dampers(self) -> 'List[_2193.SpringDamperSystemDeflection]':
        '''List[SpringDamperSystemDeflection]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_2193.SpringDamperSystemDeflection))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_2358.StraightBevelDiffGearSetSystemDeflection]':
        '''List[StraightBevelDiffGearSetSystemDeflection]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_2358.StraightBevelDiffGearSetSystemDeflection))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_2362.StraightBevelGearSetSystemDeflection]':
        '''List[StraightBevelGearSetSystemDeflection]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_2362.StraightBevelGearSetSystemDeflection))
        return value

    @property
    def synchronisers(self) -> 'List[_2197.SynchroniserSystemDeflection]':
        '''List[SynchroniserSystemDeflection]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_2197.SynchroniserSystemDeflection))
        return value

    @property
    def torque_converters(self) -> 'List[_2205.TorqueConverterSystemDeflection]':
        '''List[TorqueConverterSystemDeflection]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_2205.TorqueConverterSystemDeflection))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_2302.UnbalancedMassSystemDeflection]':
        '''List[UnbalancedMassSystemDeflection]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_2302.UnbalancedMassSystemDeflection))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_2167.WormGearSetSystemDeflection]':
        '''List[WormGearSetSystemDeflection]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_2167.WormGearSetSystemDeflection))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_2170.ZerolBevelGearSetSystemDeflection]':
        '''List[ZerolBevelGearSetSystemDeflection]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_2170.ZerolBevelGearSetSystemDeflection))
        return value

    @property
    def shafts_and_housings(self) -> 'List[_2136.AbstractShaftOrHousingSystemDeflection]':
        '''List[AbstractShaftOrHousingSystemDeflection]: 'ShaftsAndHousings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftsAndHousings, constructor.new(_2136.AbstractShaftOrHousingSystemDeflection))
        return value

    @property
    def supercharger_rotor_sets(self) -> 'List[_2374.CylindricalGearSetSystemDeflection]':
        '''List[CylindricalGearSetSystemDeflection]: 'SuperchargerRotorSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SuperchargerRotorSets, constructor.new(_2374.CylindricalGearSetSystemDeflection))
        return value

    @property
    def rolling_bearings(self) -> 'List[_2141.BearingSystemDeflection]':
        '''List[BearingSystemDeflection]: 'RollingBearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingBearings, constructor.new(_2141.BearingSystemDeflection))
        return value

    @property
    def connection_details(self) -> 'List[_2215.ConnectionSystemDeflection]':
        '''List[ConnectionSystemDeflection]: 'ConnectionDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionDetails, constructor.new(_2215.ConnectionSystemDeflection))
        return value

    @property
    def sorted_converged_connection_details(self) -> 'List[_2215.ConnectionSystemDeflection]':
        '''List[ConnectionSystemDeflection]: 'SortedConvergedConnectionDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SortedConvergedConnectionDetails, constructor.new(_2215.ConnectionSystemDeflection))
        return value

    @property
    def sorted_unconverged_connection_details(self) -> 'List[_2215.ConnectionSystemDeflection]':
        '''List[ConnectionSystemDeflection]: 'SortedUnconvergedConnectionDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SortedUnconvergedConnectionDetails, constructor.new(_2215.ConnectionSystemDeflection))
        return value

    @property
    def component_details(self) -> 'List[_2158.ComponentSystemDeflection]':
        '''List[ComponentSystemDeflection]: 'ComponentDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDetails, constructor.new(_2158.ComponentSystemDeflection))
        return value

    @property
    def mountable_component_details(self) -> 'List[_2286.MountableComponentSystemDeflection]':
        '''List[MountableComponentSystemDeflection]: 'MountableComponentDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MountableComponentDetails, constructor.new(_2286.MountableComponentSystemDeflection))
        return value

    @property
    def sorted_converged_component_details(self) -> 'List[_2158.ComponentSystemDeflection]':
        '''List[ComponentSystemDeflection]: 'SortedConvergedComponentDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SortedConvergedComponentDetails, constructor.new(_2158.ComponentSystemDeflection))
        return value

    @property
    def sorted_unconverged_component_details(self) -> 'List[_2158.ComponentSystemDeflection]':
        '''List[ComponentSystemDeflection]: 'SortedUnconvergedComponentDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SortedUnconvergedComponentDetails, constructor.new(_2158.ComponentSystemDeflection))
        return value

    @property
    def unconverged_bearings_sorted_by_load(self) -> 'List[_2141.BearingSystemDeflection]':
        '''List[BearingSystemDeflection]: 'UnconvergedBearingsSortedByLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnconvergedBearingsSortedByLoad, constructor.new(_2141.BearingSystemDeflection))
        return value

    @property
    def unconverged_gear_meshes_sorted_by_power(self) -> 'List[_2261.GearMeshSystemDeflection]':
        '''List[GearMeshSystemDeflection]: 'UnconvergedGearMeshesSortedByPower' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnconvergedGearMeshesSortedByPower, constructor.new(_2261.GearMeshSystemDeflection))
        return value
