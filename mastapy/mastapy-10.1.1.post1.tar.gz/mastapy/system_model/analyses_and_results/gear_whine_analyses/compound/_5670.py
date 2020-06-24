'''_5670.py

AssemblyCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1980
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5258
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import (
    _5671, _5673, _5676, _5682,
    _5683, _5684, _5689, _5694,
    _5704, _5708, _5714, _5715,
    _5722, _5723, _5730, _5733,
    _5734, _5735, _5737, _5739,
    _5744, _5745, _5746, _5753,
    _5748, _5752, _5758, _5759,
    _5764, _5767, _5770, _5774,
    _5778, _5782, _5785, _5665
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'AssemblyCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundGearWhineAnalysis',)


class AssemblyCompoundGearWhineAnalysis(_5665.AbstractAssemblyCompoundGearWhineAnalysis):
    '''AssemblyCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1980.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1980.Assembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1980.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1980.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5258.AssemblyGearWhineAnalysis]':
        '''List[AssemblyGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5258.AssemblyGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_5258.AssemblyGearWhineAnalysis]':
        '''List[AssemblyGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_5258.AssemblyGearWhineAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5671.BearingCompoundGearWhineAnalysis]':
        '''List[BearingCompoundGearWhineAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5671.BearingCompoundGearWhineAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5673.BeltDriveCompoundGearWhineAnalysis]':
        '''List[BeltDriveCompoundGearWhineAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5673.BeltDriveCompoundGearWhineAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5676.BevelDifferentialGearSetCompoundGearWhineAnalysis]':
        '''List[BevelDifferentialGearSetCompoundGearWhineAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5676.BevelDifferentialGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5682.BoltCompoundGearWhineAnalysis]':
        '''List[BoltCompoundGearWhineAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5682.BoltCompoundGearWhineAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5683.BoltedJointCompoundGearWhineAnalysis]':
        '''List[BoltedJointCompoundGearWhineAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5683.BoltedJointCompoundGearWhineAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5684.ClutchCompoundGearWhineAnalysis]':
        '''List[ClutchCompoundGearWhineAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5684.ClutchCompoundGearWhineAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5689.ConceptCouplingCompoundGearWhineAnalysis]':
        '''List[ConceptCouplingCompoundGearWhineAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5689.ConceptCouplingCompoundGearWhineAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5694.ConceptGearSetCompoundGearWhineAnalysis]':
        '''List[ConceptGearSetCompoundGearWhineAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5694.ConceptGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5704.CVTCompoundGearWhineAnalysis]':
        '''List[CVTCompoundGearWhineAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5704.CVTCompoundGearWhineAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5708.CylindricalGearSetCompoundGearWhineAnalysis]':
        '''List[CylindricalGearSetCompoundGearWhineAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5708.CylindricalGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5714.FaceGearSetCompoundGearWhineAnalysis]':
        '''List[FaceGearSetCompoundGearWhineAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5714.FaceGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5715.FlexiblePinAssemblyCompoundGearWhineAnalysis]':
        '''List[FlexiblePinAssemblyCompoundGearWhineAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5715.FlexiblePinAssemblyCompoundGearWhineAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5722.HypoidGearSetCompoundGearWhineAnalysis]':
        '''List[HypoidGearSetCompoundGearWhineAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5722.HypoidGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_5723.ImportedFEComponentCompoundGearWhineAnalysis]':
        '''List[ImportedFEComponentCompoundGearWhineAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_5723.ImportedFEComponentCompoundGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5730.KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5730.KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5733.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5733.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5734.MassDiscCompoundGearWhineAnalysis]':
        '''List[MassDiscCompoundGearWhineAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5734.MassDiscCompoundGearWhineAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5735.MeasurementComponentCompoundGearWhineAnalysis]':
        '''List[MeasurementComponentCompoundGearWhineAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5735.MeasurementComponentCompoundGearWhineAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5737.OilSealCompoundGearWhineAnalysis]':
        '''List[OilSealCompoundGearWhineAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5737.OilSealCompoundGearWhineAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5739.PartToPartShearCouplingCompoundGearWhineAnalysis]':
        '''List[PartToPartShearCouplingCompoundGearWhineAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5739.PartToPartShearCouplingCompoundGearWhineAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5744.PlanetCarrierCompoundGearWhineAnalysis]':
        '''List[PlanetCarrierCompoundGearWhineAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5744.PlanetCarrierCompoundGearWhineAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5745.PointLoadCompoundGearWhineAnalysis]':
        '''List[PointLoadCompoundGearWhineAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5745.PointLoadCompoundGearWhineAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5746.PowerLoadCompoundGearWhineAnalysis]':
        '''List[PowerLoadCompoundGearWhineAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5746.PowerLoadCompoundGearWhineAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5753.ShaftHubConnectionCompoundGearWhineAnalysis]':
        '''List[ShaftHubConnectionCompoundGearWhineAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5753.ShaftHubConnectionCompoundGearWhineAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5748.RollingRingAssemblyCompoundGearWhineAnalysis]':
        '''List[RollingRingAssemblyCompoundGearWhineAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5748.RollingRingAssemblyCompoundGearWhineAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5752.ShaftCompoundGearWhineAnalysis]':
        '''List[ShaftCompoundGearWhineAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5752.ShaftCompoundGearWhineAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5758.SpiralBevelGearSetCompoundGearWhineAnalysis]':
        '''List[SpiralBevelGearSetCompoundGearWhineAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5758.SpiralBevelGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5759.SpringDamperCompoundGearWhineAnalysis]':
        '''List[SpringDamperCompoundGearWhineAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5759.SpringDamperCompoundGearWhineAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5764.StraightBevelDiffGearSetCompoundGearWhineAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundGearWhineAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5764.StraightBevelDiffGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5767.StraightBevelGearSetCompoundGearWhineAnalysis]':
        '''List[StraightBevelGearSetCompoundGearWhineAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5767.StraightBevelGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5770.SynchroniserCompoundGearWhineAnalysis]':
        '''List[SynchroniserCompoundGearWhineAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5770.SynchroniserCompoundGearWhineAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5774.TorqueConverterCompoundGearWhineAnalysis]':
        '''List[TorqueConverterCompoundGearWhineAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5774.TorqueConverterCompoundGearWhineAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5778.UnbalancedMassCompoundGearWhineAnalysis]':
        '''List[UnbalancedMassCompoundGearWhineAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5778.UnbalancedMassCompoundGearWhineAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5782.WormGearSetCompoundGearWhineAnalysis]':
        '''List[WormGearSetCompoundGearWhineAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5782.WormGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5785.ZerolBevelGearSetCompoundGearWhineAnalysis]':
        '''List[ZerolBevelGearSetCompoundGearWhineAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5785.ZerolBevelGearSetCompoundGearWhineAnalysis))
        return value
