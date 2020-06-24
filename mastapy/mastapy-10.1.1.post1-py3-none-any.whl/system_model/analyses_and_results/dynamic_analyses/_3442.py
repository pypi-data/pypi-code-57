'''_3442.py

AssemblyDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1904
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2317
from mastapy.system_model.analyses_and_results.dynamic_analyses import (
    _3434, _3380, _3465, _3435,
    _3436, _3381, _3383, _3459,
    _3387, _3473, _3461, _3441,
    _3478, _3444, _3482, _3484,
    _3445, _3446, _3448, _3450,
    _3451, _3452, _3390, _3392,
    _3457, _3487, _3393, _3489,
    _3491, _3395, _3399, _3455,
    _3377, _3379, _3432
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'AssemblyDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyDynamicAnalysis',)


class AssemblyDynamicAnalysis(_3432.AbstractAssemblyDynamicAnalysis):
    '''AssemblyDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1904.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1904.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2317.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2317.AssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bearings(self) -> 'List[_3434.BearingDynamicAnalysis]':
        '''List[BearingDynamicAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3434.BearingDynamicAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_3380.BeltDriveDynamicAnalysis]':
        '''List[BeltDriveDynamicAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3380.BeltDriveDynamicAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3465.BevelDifferentialGearSetDynamicAnalysis]':
        '''List[BevelDifferentialGearSetDynamicAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3465.BevelDifferentialGearSetDynamicAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_3435.BoltDynamicAnalysis]':
        '''List[BoltDynamicAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3435.BoltDynamicAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_3436.BoltedJointDynamicAnalysis]':
        '''List[BoltedJointDynamicAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3436.BoltedJointDynamicAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_3381.ClutchDynamicAnalysis]':
        '''List[ClutchDynamicAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3381.ClutchDynamicAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_3383.ConceptCouplingDynamicAnalysis]':
        '''List[ConceptCouplingDynamicAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3383.ConceptCouplingDynamicAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3459.ConceptGearSetDynamicAnalysis]':
        '''List[ConceptGearSetDynamicAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3459.ConceptGearSetDynamicAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_3387.CVTDynamicAnalysis]':
        '''List[CVTDynamicAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3387.CVTDynamicAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3473.CylindricalGearSetDynamicAnalysis]':
        '''List[CylindricalGearSetDynamicAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3473.CylindricalGearSetDynamicAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3461.FaceGearSetDynamicAnalysis]':
        '''List[FaceGearSetDynamicAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3461.FaceGearSetDynamicAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3441.FlexiblePinAssemblyDynamicAnalysis]':
        '''List[FlexiblePinAssemblyDynamicAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3441.FlexiblePinAssemblyDynamicAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3478.HypoidGearSetDynamicAnalysis]':
        '''List[HypoidGearSetDynamicAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3478.HypoidGearSetDynamicAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_3444.ImportedFEComponentDynamicAnalysis]':
        '''List[ImportedFEComponentDynamicAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_3444.ImportedFEComponentDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3482.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3482.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3484.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3484.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_3445.MassDiscDynamicAnalysis]':
        '''List[MassDiscDynamicAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3445.MassDiscDynamicAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_3446.MeasurementComponentDynamicAnalysis]':
        '''List[MeasurementComponentDynamicAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3446.MeasurementComponentDynamicAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_3448.OilSealDynamicAnalysis]':
        '''List[OilSealDynamicAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3448.OilSealDynamicAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_3450.PlanetCarrierDynamicAnalysis]':
        '''List[PlanetCarrierDynamicAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3450.PlanetCarrierDynamicAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_3451.PointLoadDynamicAnalysis]':
        '''List[PointLoadDynamicAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3451.PointLoadDynamicAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_3452.PowerLoadDynamicAnalysis]':
        '''List[PowerLoadDynamicAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3452.PowerLoadDynamicAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3390.ShaftHubConnectionDynamicAnalysis]':
        '''List[ShaftHubConnectionDynamicAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3390.ShaftHubConnectionDynamicAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3392.RollingRingAssemblyDynamicAnalysis]':
        '''List[RollingRingAssemblyDynamicAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3392.RollingRingAssemblyDynamicAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_3457.ShaftDynamicAnalysis]':
        '''List[ShaftDynamicAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3457.ShaftDynamicAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3487.SpiralBevelGearSetDynamicAnalysis]':
        '''List[SpiralBevelGearSetDynamicAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3487.SpiralBevelGearSetDynamicAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_3393.SpringDamperDynamicAnalysis]':
        '''List[SpringDamperDynamicAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3393.SpringDamperDynamicAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3489.StraightBevelDiffGearSetDynamicAnalysis]':
        '''List[StraightBevelDiffGearSetDynamicAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3489.StraightBevelDiffGearSetDynamicAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3491.StraightBevelGearSetDynamicAnalysis]':
        '''List[StraightBevelGearSetDynamicAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3491.StraightBevelGearSetDynamicAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_3395.SynchroniserDynamicAnalysis]':
        '''List[SynchroniserDynamicAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3395.SynchroniserDynamicAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_3399.TorqueConverterDynamicAnalysis]':
        '''List[TorqueConverterDynamicAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3399.TorqueConverterDynamicAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3455.UnbalancedMassDynamicAnalysis]':
        '''List[UnbalancedMassDynamicAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3455.UnbalancedMassDynamicAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3377.WormGearSetDynamicAnalysis]':
        '''List[WormGearSetDynamicAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3377.WormGearSetDynamicAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3379.ZerolBevelGearSetDynamicAnalysis]':
        '''List[ZerolBevelGearSetDynamicAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3379.ZerolBevelGearSetDynamicAnalysis))
        return value
