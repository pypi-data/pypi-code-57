'''_6240.py

AssemblyAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _1980
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6053
from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
    _6241, _6243, _6246, _6252,
    _6253, _6254, _6259, _6264,
    _6273, _6278, _6285, _6286,
    _6293, _6294, _6301, _6304,
    _6306, _6307, _6309, _6311,
    _6316, _6317, _6318, _6325,
    _6321, _6324, _6330, _6331,
    _6336, _6339, _6342, _6346,
    _6351, _6356, _6359, _6232
)
from mastapy.system_model.analyses_and_results.system_deflections import _2212
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'AssemblyAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyAdvancedSystemDeflection',)


class AssemblyAdvancedSystemDeflection(_6232.AbstractAssemblyAdvancedSystemDeflection):
    '''AssemblyAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1980.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1980.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6053.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6053.AssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bearings(self) -> 'List[_6241.BearingAdvancedSystemDeflection]':
        '''List[BearingAdvancedSystemDeflection]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6241.BearingAdvancedSystemDeflection))
        return value

    @property
    def belt_drives(self) -> 'List[_6243.BeltDriveAdvancedSystemDeflection]':
        '''List[BeltDriveAdvancedSystemDeflection]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6243.BeltDriveAdvancedSystemDeflection))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6246.BevelDifferentialGearSetAdvancedSystemDeflection]':
        '''List[BevelDifferentialGearSetAdvancedSystemDeflection]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6246.BevelDifferentialGearSetAdvancedSystemDeflection))
        return value

    @property
    def bolts(self) -> 'List[_6252.BoltAdvancedSystemDeflection]':
        '''List[BoltAdvancedSystemDeflection]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6252.BoltAdvancedSystemDeflection))
        return value

    @property
    def bolted_joints(self) -> 'List[_6253.BoltedJointAdvancedSystemDeflection]':
        '''List[BoltedJointAdvancedSystemDeflection]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6253.BoltedJointAdvancedSystemDeflection))
        return value

    @property
    def clutches(self) -> 'List[_6254.ClutchAdvancedSystemDeflection]':
        '''List[ClutchAdvancedSystemDeflection]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6254.ClutchAdvancedSystemDeflection))
        return value

    @property
    def concept_couplings(self) -> 'List[_6259.ConceptCouplingAdvancedSystemDeflection]':
        '''List[ConceptCouplingAdvancedSystemDeflection]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6259.ConceptCouplingAdvancedSystemDeflection))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6264.ConceptGearSetAdvancedSystemDeflection]':
        '''List[ConceptGearSetAdvancedSystemDeflection]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6264.ConceptGearSetAdvancedSystemDeflection))
        return value

    @property
    def cv_ts(self) -> 'List[_6273.CVTAdvancedSystemDeflection]':
        '''List[CVTAdvancedSystemDeflection]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6273.CVTAdvancedSystemDeflection))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6278.CylindricalGearSetAdvancedSystemDeflection]':
        '''List[CylindricalGearSetAdvancedSystemDeflection]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6278.CylindricalGearSetAdvancedSystemDeflection))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6285.FaceGearSetAdvancedSystemDeflection]':
        '''List[FaceGearSetAdvancedSystemDeflection]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6285.FaceGearSetAdvancedSystemDeflection))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6286.FlexiblePinAssemblyAdvancedSystemDeflection]':
        '''List[FlexiblePinAssemblyAdvancedSystemDeflection]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6286.FlexiblePinAssemblyAdvancedSystemDeflection))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6293.HypoidGearSetAdvancedSystemDeflection]':
        '''List[HypoidGearSetAdvancedSystemDeflection]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6293.HypoidGearSetAdvancedSystemDeflection))
        return value

    @property
    def imported_fe_components(self) -> 'List[_6294.ImportedFEComponentAdvancedSystemDeflection]':
        '''List[ImportedFEComponentAdvancedSystemDeflection]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_6294.ImportedFEComponentAdvancedSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6301.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6301.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6304.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6304.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection))
        return value

    @property
    def mass_discs(self) -> 'List[_6306.MassDiscAdvancedSystemDeflection]':
        '''List[MassDiscAdvancedSystemDeflection]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6306.MassDiscAdvancedSystemDeflection))
        return value

    @property
    def measurement_components(self) -> 'List[_6307.MeasurementComponentAdvancedSystemDeflection]':
        '''List[MeasurementComponentAdvancedSystemDeflection]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6307.MeasurementComponentAdvancedSystemDeflection))
        return value

    @property
    def oil_seals(self) -> 'List[_6309.OilSealAdvancedSystemDeflection]':
        '''List[OilSealAdvancedSystemDeflection]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6309.OilSealAdvancedSystemDeflection))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6311.PartToPartShearCouplingAdvancedSystemDeflection]':
        '''List[PartToPartShearCouplingAdvancedSystemDeflection]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6311.PartToPartShearCouplingAdvancedSystemDeflection))
        return value

    @property
    def planet_carriers(self) -> 'List[_6316.PlanetCarrierAdvancedSystemDeflection]':
        '''List[PlanetCarrierAdvancedSystemDeflection]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6316.PlanetCarrierAdvancedSystemDeflection))
        return value

    @property
    def point_loads(self) -> 'List[_6317.PointLoadAdvancedSystemDeflection]':
        '''List[PointLoadAdvancedSystemDeflection]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6317.PointLoadAdvancedSystemDeflection))
        return value

    @property
    def power_loads(self) -> 'List[_6318.PowerLoadAdvancedSystemDeflection]':
        '''List[PowerLoadAdvancedSystemDeflection]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6318.PowerLoadAdvancedSystemDeflection))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6325.ShaftHubConnectionAdvancedSystemDeflection]':
        '''List[ShaftHubConnectionAdvancedSystemDeflection]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6325.ShaftHubConnectionAdvancedSystemDeflection))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6321.RollingRingAssemblyAdvancedSystemDeflection]':
        '''List[RollingRingAssemblyAdvancedSystemDeflection]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6321.RollingRingAssemblyAdvancedSystemDeflection))
        return value

    @property
    def shafts(self) -> 'List[_6324.ShaftAdvancedSystemDeflection]':
        '''List[ShaftAdvancedSystemDeflection]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6324.ShaftAdvancedSystemDeflection))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6330.SpiralBevelGearSetAdvancedSystemDeflection]':
        '''List[SpiralBevelGearSetAdvancedSystemDeflection]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6330.SpiralBevelGearSetAdvancedSystemDeflection))
        return value

    @property
    def spring_dampers(self) -> 'List[_6331.SpringDamperAdvancedSystemDeflection]':
        '''List[SpringDamperAdvancedSystemDeflection]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6331.SpringDamperAdvancedSystemDeflection))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6336.StraightBevelDiffGearSetAdvancedSystemDeflection]':
        '''List[StraightBevelDiffGearSetAdvancedSystemDeflection]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6336.StraightBevelDiffGearSetAdvancedSystemDeflection))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6339.StraightBevelGearSetAdvancedSystemDeflection]':
        '''List[StraightBevelGearSetAdvancedSystemDeflection]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6339.StraightBevelGearSetAdvancedSystemDeflection))
        return value

    @property
    def synchronisers(self) -> 'List[_6342.SynchroniserAdvancedSystemDeflection]':
        '''List[SynchroniserAdvancedSystemDeflection]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6342.SynchroniserAdvancedSystemDeflection))
        return value

    @property
    def torque_converters(self) -> 'List[_6346.TorqueConverterAdvancedSystemDeflection]':
        '''List[TorqueConverterAdvancedSystemDeflection]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6346.TorqueConverterAdvancedSystemDeflection))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6351.UnbalancedMassAdvancedSystemDeflection]':
        '''List[UnbalancedMassAdvancedSystemDeflection]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6351.UnbalancedMassAdvancedSystemDeflection))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6356.WormGearSetAdvancedSystemDeflection]':
        '''List[WormGearSetAdvancedSystemDeflection]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6356.WormGearSetAdvancedSystemDeflection))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6359.ZerolBevelGearSetAdvancedSystemDeflection]':
        '''List[ZerolBevelGearSetAdvancedSystemDeflection]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6359.ZerolBevelGearSetAdvancedSystemDeflection))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2212.AssemblySystemDeflection]':
        '''List[AssemblySystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2212.AssemblySystemDeflection))
        return value
