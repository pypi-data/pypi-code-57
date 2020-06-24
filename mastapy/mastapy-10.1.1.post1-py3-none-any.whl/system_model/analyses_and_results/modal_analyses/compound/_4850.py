'''_4850.py

AssemblyCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1980
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4704
from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
    _4851, _4853, _4856, _4862,
    _4863, _4864, _4869, _4874,
    _4884, _4888, _4894, _4895,
    _4902, _4903, _4910, _4913,
    _4914, _4915, _4917, _4919,
    _4924, _4925, _4926, _4933,
    _4928, _4932, _4938, _4939,
    _4944, _4947, _4950, _4954,
    _4958, _4962, _4965, _4845
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'AssemblyCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundModalAnalysis',)


class AssemblyCompoundModalAnalysis(_4845.AbstractAssemblyCompoundModalAnalysis):
    '''AssemblyCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundModalAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_4704.AssemblyModalAnalysis]':
        '''List[AssemblyModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4704.AssemblyModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_4704.AssemblyModalAnalysis]':
        '''List[AssemblyModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_4704.AssemblyModalAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_4851.BearingCompoundModalAnalysis]':
        '''List[BearingCompoundModalAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4851.BearingCompoundModalAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_4853.BeltDriveCompoundModalAnalysis]':
        '''List[BeltDriveCompoundModalAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4853.BeltDriveCompoundModalAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4856.BevelDifferentialGearSetCompoundModalAnalysis]':
        '''List[BevelDifferentialGearSetCompoundModalAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4856.BevelDifferentialGearSetCompoundModalAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_4862.BoltCompoundModalAnalysis]':
        '''List[BoltCompoundModalAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4862.BoltCompoundModalAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_4863.BoltedJointCompoundModalAnalysis]':
        '''List[BoltedJointCompoundModalAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4863.BoltedJointCompoundModalAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_4864.ClutchCompoundModalAnalysis]':
        '''List[ClutchCompoundModalAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4864.ClutchCompoundModalAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_4869.ConceptCouplingCompoundModalAnalysis]':
        '''List[ConceptCouplingCompoundModalAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4869.ConceptCouplingCompoundModalAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4874.ConceptGearSetCompoundModalAnalysis]':
        '''List[ConceptGearSetCompoundModalAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4874.ConceptGearSetCompoundModalAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_4884.CVTCompoundModalAnalysis]':
        '''List[CVTCompoundModalAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4884.CVTCompoundModalAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4888.CylindricalGearSetCompoundModalAnalysis]':
        '''List[CylindricalGearSetCompoundModalAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4888.CylindricalGearSetCompoundModalAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4894.FaceGearSetCompoundModalAnalysis]':
        '''List[FaceGearSetCompoundModalAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4894.FaceGearSetCompoundModalAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4895.FlexiblePinAssemblyCompoundModalAnalysis]':
        '''List[FlexiblePinAssemblyCompoundModalAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4895.FlexiblePinAssemblyCompoundModalAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4902.HypoidGearSetCompoundModalAnalysis]':
        '''List[HypoidGearSetCompoundModalAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4902.HypoidGearSetCompoundModalAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_4903.ImportedFEComponentCompoundModalAnalysis]':
        '''List[ImportedFEComponentCompoundModalAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_4903.ImportedFEComponentCompoundModalAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4910.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4910.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4913.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4913.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_4914.MassDiscCompoundModalAnalysis]':
        '''List[MassDiscCompoundModalAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4914.MassDiscCompoundModalAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_4915.MeasurementComponentCompoundModalAnalysis]':
        '''List[MeasurementComponentCompoundModalAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4915.MeasurementComponentCompoundModalAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_4917.OilSealCompoundModalAnalysis]':
        '''List[OilSealCompoundModalAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4917.OilSealCompoundModalAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4919.PartToPartShearCouplingCompoundModalAnalysis]':
        '''List[PartToPartShearCouplingCompoundModalAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4919.PartToPartShearCouplingCompoundModalAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_4924.PlanetCarrierCompoundModalAnalysis]':
        '''List[PlanetCarrierCompoundModalAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4924.PlanetCarrierCompoundModalAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_4925.PointLoadCompoundModalAnalysis]':
        '''List[PointLoadCompoundModalAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4925.PointLoadCompoundModalAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_4926.PowerLoadCompoundModalAnalysis]':
        '''List[PowerLoadCompoundModalAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4926.PowerLoadCompoundModalAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4933.ShaftHubConnectionCompoundModalAnalysis]':
        '''List[ShaftHubConnectionCompoundModalAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4933.ShaftHubConnectionCompoundModalAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4928.RollingRingAssemblyCompoundModalAnalysis]':
        '''List[RollingRingAssemblyCompoundModalAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4928.RollingRingAssemblyCompoundModalAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_4932.ShaftCompoundModalAnalysis]':
        '''List[ShaftCompoundModalAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4932.ShaftCompoundModalAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4938.SpiralBevelGearSetCompoundModalAnalysis]':
        '''List[SpiralBevelGearSetCompoundModalAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4938.SpiralBevelGearSetCompoundModalAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_4939.SpringDamperCompoundModalAnalysis]':
        '''List[SpringDamperCompoundModalAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4939.SpringDamperCompoundModalAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4944.StraightBevelDiffGearSetCompoundModalAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundModalAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4944.StraightBevelDiffGearSetCompoundModalAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4947.StraightBevelGearSetCompoundModalAnalysis]':
        '''List[StraightBevelGearSetCompoundModalAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4947.StraightBevelGearSetCompoundModalAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_4950.SynchroniserCompoundModalAnalysis]':
        '''List[SynchroniserCompoundModalAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4950.SynchroniserCompoundModalAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_4954.TorqueConverterCompoundModalAnalysis]':
        '''List[TorqueConverterCompoundModalAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4954.TorqueConverterCompoundModalAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4958.UnbalancedMassCompoundModalAnalysis]':
        '''List[UnbalancedMassCompoundModalAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4958.UnbalancedMassCompoundModalAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4962.WormGearSetCompoundModalAnalysis]':
        '''List[WormGearSetCompoundModalAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4962.WormGearSetCompoundModalAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4965.ZerolBevelGearSetCompoundModalAnalysis]':
        '''List[ZerolBevelGearSetCompoundModalAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4965.ZerolBevelGearSetCompoundModalAnalysis))
        return value
