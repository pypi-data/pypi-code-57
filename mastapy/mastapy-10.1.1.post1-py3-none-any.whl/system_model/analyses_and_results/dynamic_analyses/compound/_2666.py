'''_2666.py

AssemblyCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1904
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3683
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import (
    _2658, _2722, _2689, _2659,
    _2660, _2723, _2725, _2683,
    _2729, _2697, _2685, _2665,
    _2702, _2668, _2706, _2708,
    _2669, _2670, _2672, _2674,
    _2675, _2676, _2732, _2734,
    _2681, _2711, _2735, _2713,
    _2715, _2737, _2741, _2679,
    _2719, _2721, _2656
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'AssemblyCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundDynamicAnalysis',)


class AssemblyCompoundDynamicAnalysis(_2656.AbstractAssemblyCompoundDynamicAnalysis):
    '''AssemblyCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1904.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1904.Assembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1904.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1904.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3683.AssemblyDynamicAnalysis]':
        '''List[AssemblyDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3683.AssemblyDynamicAnalysis))
        return value

    @property
    def assembly_dynamic_analysis_load_cases(self) -> 'List[_3683.AssemblyDynamicAnalysis]':
        '''List[AssemblyDynamicAnalysis]: 'AssemblyDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyDynamicAnalysisLoadCases, constructor.new(_3683.AssemblyDynamicAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_2658.BearingCompoundDynamicAnalysis]':
        '''List[BearingCompoundDynamicAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_2658.BearingCompoundDynamicAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_2722.BeltDriveCompoundDynamicAnalysis]':
        '''List[BeltDriveCompoundDynamicAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_2722.BeltDriveCompoundDynamicAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_2689.BevelDifferentialGearSetCompoundDynamicAnalysis]':
        '''List[BevelDifferentialGearSetCompoundDynamicAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_2689.BevelDifferentialGearSetCompoundDynamicAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_2659.BoltCompoundDynamicAnalysis]':
        '''List[BoltCompoundDynamicAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_2659.BoltCompoundDynamicAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_2660.BoltedJointCompoundDynamicAnalysis]':
        '''List[BoltedJointCompoundDynamicAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_2660.BoltedJointCompoundDynamicAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_2723.ClutchCompoundDynamicAnalysis]':
        '''List[ClutchCompoundDynamicAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_2723.ClutchCompoundDynamicAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_2725.ConceptCouplingCompoundDynamicAnalysis]':
        '''List[ConceptCouplingCompoundDynamicAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_2725.ConceptCouplingCompoundDynamicAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_2683.ConceptGearSetCompoundDynamicAnalysis]':
        '''List[ConceptGearSetCompoundDynamicAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_2683.ConceptGearSetCompoundDynamicAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_2729.CVTCompoundDynamicAnalysis]':
        '''List[CVTCompoundDynamicAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_2729.CVTCompoundDynamicAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_2697.CylindricalGearSetCompoundDynamicAnalysis]':
        '''List[CylindricalGearSetCompoundDynamicAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_2697.CylindricalGearSetCompoundDynamicAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_2685.FaceGearSetCompoundDynamicAnalysis]':
        '''List[FaceGearSetCompoundDynamicAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_2685.FaceGearSetCompoundDynamicAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_2665.FlexiblePinAssemblyCompoundDynamicAnalysis]':
        '''List[FlexiblePinAssemblyCompoundDynamicAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_2665.FlexiblePinAssemblyCompoundDynamicAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_2702.HypoidGearSetCompoundDynamicAnalysis]':
        '''List[HypoidGearSetCompoundDynamicAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_2702.HypoidGearSetCompoundDynamicAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_2668.ImportedFEComponentCompoundDynamicAnalysis]':
        '''List[ImportedFEComponentCompoundDynamicAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_2668.ImportedFEComponentCompoundDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_2706.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_2706.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_2708.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_2708.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_2669.MassDiscCompoundDynamicAnalysis]':
        '''List[MassDiscCompoundDynamicAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_2669.MassDiscCompoundDynamicAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_2670.MeasurementComponentCompoundDynamicAnalysis]':
        '''List[MeasurementComponentCompoundDynamicAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_2670.MeasurementComponentCompoundDynamicAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_2672.OilSealCompoundDynamicAnalysis]':
        '''List[OilSealCompoundDynamicAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_2672.OilSealCompoundDynamicAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_2674.PlanetCarrierCompoundDynamicAnalysis]':
        '''List[PlanetCarrierCompoundDynamicAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_2674.PlanetCarrierCompoundDynamicAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_2675.PointLoadCompoundDynamicAnalysis]':
        '''List[PointLoadCompoundDynamicAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_2675.PointLoadCompoundDynamicAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_2676.PowerLoadCompoundDynamicAnalysis]':
        '''List[PowerLoadCompoundDynamicAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_2676.PowerLoadCompoundDynamicAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_2732.ShaftHubConnectionCompoundDynamicAnalysis]':
        '''List[ShaftHubConnectionCompoundDynamicAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_2732.ShaftHubConnectionCompoundDynamicAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_2734.RollingRingAssemblyCompoundDynamicAnalysis]':
        '''List[RollingRingAssemblyCompoundDynamicAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_2734.RollingRingAssemblyCompoundDynamicAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_2681.ShaftCompoundDynamicAnalysis]':
        '''List[ShaftCompoundDynamicAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_2681.ShaftCompoundDynamicAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_2711.SpiralBevelGearSetCompoundDynamicAnalysis]':
        '''List[SpiralBevelGearSetCompoundDynamicAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_2711.SpiralBevelGearSetCompoundDynamicAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_2735.SpringDamperCompoundDynamicAnalysis]':
        '''List[SpringDamperCompoundDynamicAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_2735.SpringDamperCompoundDynamicAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_2713.StraightBevelDiffGearSetCompoundDynamicAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundDynamicAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_2713.StraightBevelDiffGearSetCompoundDynamicAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_2715.StraightBevelGearSetCompoundDynamicAnalysis]':
        '''List[StraightBevelGearSetCompoundDynamicAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_2715.StraightBevelGearSetCompoundDynamicAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_2737.SynchroniserCompoundDynamicAnalysis]':
        '''List[SynchroniserCompoundDynamicAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_2737.SynchroniserCompoundDynamicAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_2741.TorqueConverterCompoundDynamicAnalysis]':
        '''List[TorqueConverterCompoundDynamicAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_2741.TorqueConverterCompoundDynamicAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_2679.UnbalancedMassCompoundDynamicAnalysis]':
        '''List[UnbalancedMassCompoundDynamicAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_2679.UnbalancedMassCompoundDynamicAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_2719.WormGearSetCompoundDynamicAnalysis]':
        '''List[WormGearSetCompoundDynamicAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_2719.WormGearSetCompoundDynamicAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_2721.ZerolBevelGearSetCompoundDynamicAnalysis]':
        '''List[ZerolBevelGearSetCompoundDynamicAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_2721.ZerolBevelGearSetCompoundDynamicAnalysis))
        return value
