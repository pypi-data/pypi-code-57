'''_4184.py

AssemblyPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _1904
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2277
from mastapy.gears.analysis import _1123
from mastapy.system_model.analyses_and_results.power_flows import (
    _4176, _4122, _4207, _4177,
    _4178, _4123, _4125, _4201,
    _4129, _4215, _4203, _4183,
    _4220, _4186, _4224, _4226,
    _4187, _4188, _4190, _4192,
    _4193, _4194, _4132, _4134,
    _4199, _4229, _4135, _4231,
    _4233, _4137, _4141, _4197,
    _4119, _4121, _4174
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'AssemblyPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyPowerFlow',)


class AssemblyPowerFlow(_4174.AbstractAssemblyPowerFlow):
    '''AssemblyPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

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
    def rating_for_all_gear_sets(self) -> '_1123.GearSetGroupDutyCycle':
        '''GearSetGroupDutyCycle: 'RatingForAllGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1123.GearSetGroupDutyCycle)(self.wrapped.RatingForAllGearSets) if self.wrapped.RatingForAllGearSets else None

    @property
    def bearings(self) -> 'List[_4176.BearingPowerFlow]':
        '''List[BearingPowerFlow]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4176.BearingPowerFlow))
        return value

    @property
    def belt_drives(self) -> 'List[_4122.BeltDrivePowerFlow]':
        '''List[BeltDrivePowerFlow]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4122.BeltDrivePowerFlow))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4207.BevelDifferentialGearSetPowerFlow]':
        '''List[BevelDifferentialGearSetPowerFlow]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4207.BevelDifferentialGearSetPowerFlow))
        return value

    @property
    def bolts(self) -> 'List[_4177.BoltPowerFlow]':
        '''List[BoltPowerFlow]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4177.BoltPowerFlow))
        return value

    @property
    def bolted_joints(self) -> 'List[_4178.BoltedJointPowerFlow]':
        '''List[BoltedJointPowerFlow]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4178.BoltedJointPowerFlow))
        return value

    @property
    def clutches(self) -> 'List[_4123.ClutchPowerFlow]':
        '''List[ClutchPowerFlow]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4123.ClutchPowerFlow))
        return value

    @property
    def concept_couplings(self) -> 'List[_4125.ConceptCouplingPowerFlow]':
        '''List[ConceptCouplingPowerFlow]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4125.ConceptCouplingPowerFlow))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4201.ConceptGearSetPowerFlow]':
        '''List[ConceptGearSetPowerFlow]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4201.ConceptGearSetPowerFlow))
        return value

    @property
    def cv_ts(self) -> 'List[_4129.CVTPowerFlow]':
        '''List[CVTPowerFlow]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4129.CVTPowerFlow))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4215.CylindricalGearSetPowerFlow]':
        '''List[CylindricalGearSetPowerFlow]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4215.CylindricalGearSetPowerFlow))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4203.FaceGearSetPowerFlow]':
        '''List[FaceGearSetPowerFlow]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4203.FaceGearSetPowerFlow))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4183.FlexiblePinAssemblyPowerFlow]':
        '''List[FlexiblePinAssemblyPowerFlow]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4183.FlexiblePinAssemblyPowerFlow))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4220.HypoidGearSetPowerFlow]':
        '''List[HypoidGearSetPowerFlow]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4220.HypoidGearSetPowerFlow))
        return value

    @property
    def imported_fe_components(self) -> 'List[_4186.ImportedFEComponentPowerFlow]':
        '''List[ImportedFEComponentPowerFlow]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_4186.ImportedFEComponentPowerFlow))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4224.KlingelnbergCycloPalloidHypoidGearSetPowerFlow]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetPowerFlow]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4224.KlingelnbergCycloPalloidHypoidGearSetPowerFlow))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4226.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4226.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow))
        return value

    @property
    def mass_discs(self) -> 'List[_4187.MassDiscPowerFlow]':
        '''List[MassDiscPowerFlow]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4187.MassDiscPowerFlow))
        return value

    @property
    def measurement_components(self) -> 'List[_4188.MeasurementComponentPowerFlow]':
        '''List[MeasurementComponentPowerFlow]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4188.MeasurementComponentPowerFlow))
        return value

    @property
    def oil_seals(self) -> 'List[_4190.OilSealPowerFlow]':
        '''List[OilSealPowerFlow]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4190.OilSealPowerFlow))
        return value

    @property
    def planet_carriers(self) -> 'List[_4192.PlanetCarrierPowerFlow]':
        '''List[PlanetCarrierPowerFlow]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4192.PlanetCarrierPowerFlow))
        return value

    @property
    def point_loads(self) -> 'List[_4193.PointLoadPowerFlow]':
        '''List[PointLoadPowerFlow]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4193.PointLoadPowerFlow))
        return value

    @property
    def power_loads(self) -> 'List[_4194.PowerLoadPowerFlow]':
        '''List[PowerLoadPowerFlow]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4194.PowerLoadPowerFlow))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4132.ShaftHubConnectionPowerFlow]':
        '''List[ShaftHubConnectionPowerFlow]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4132.ShaftHubConnectionPowerFlow))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4134.RollingRingAssemblyPowerFlow]':
        '''List[RollingRingAssemblyPowerFlow]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4134.RollingRingAssemblyPowerFlow))
        return value

    @property
    def shafts(self) -> 'List[_4199.ShaftPowerFlow]':
        '''List[ShaftPowerFlow]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4199.ShaftPowerFlow))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4229.SpiralBevelGearSetPowerFlow]':
        '''List[SpiralBevelGearSetPowerFlow]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4229.SpiralBevelGearSetPowerFlow))
        return value

    @property
    def spring_dampers(self) -> 'List[_4135.SpringDamperPowerFlow]':
        '''List[SpringDamperPowerFlow]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4135.SpringDamperPowerFlow))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4231.StraightBevelDiffGearSetPowerFlow]':
        '''List[StraightBevelDiffGearSetPowerFlow]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4231.StraightBevelDiffGearSetPowerFlow))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4233.StraightBevelGearSetPowerFlow]':
        '''List[StraightBevelGearSetPowerFlow]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4233.StraightBevelGearSetPowerFlow))
        return value

    @property
    def synchronisers(self) -> 'List[_4137.SynchroniserPowerFlow]':
        '''List[SynchroniserPowerFlow]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4137.SynchroniserPowerFlow))
        return value

    @property
    def torque_converters(self) -> 'List[_4141.TorqueConverterPowerFlow]':
        '''List[TorqueConverterPowerFlow]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4141.TorqueConverterPowerFlow))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4197.UnbalancedMassPowerFlow]':
        '''List[UnbalancedMassPowerFlow]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4197.UnbalancedMassPowerFlow))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4119.WormGearSetPowerFlow]':
        '''List[WormGearSetPowerFlow]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4119.WormGearSetPowerFlow))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4121.ZerolBevelGearSetPowerFlow]':
        '''List[ZerolBevelGearSetPowerFlow]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4121.ZerolBevelGearSetPowerFlow))
        return value
