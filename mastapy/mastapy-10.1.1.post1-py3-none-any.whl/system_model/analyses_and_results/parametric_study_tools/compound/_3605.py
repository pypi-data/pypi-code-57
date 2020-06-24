'''_3605.py

AssemblyCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _1980
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3468
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
    _3606, _3608, _3611, _3617,
    _3618, _3619, _3624, _3629,
    _3639, _3643, _3649, _3650,
    _3657, _3658, _3665, _3668,
    _3669, _3670, _3672, _3674,
    _3679, _3680, _3681, _3688,
    _3683, _3687, _3693, _3694,
    _3699, _3702, _3705, _3709,
    _3713, _3717, _3720, _3600
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'AssemblyCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundParametricStudyTool',)


class AssemblyCompoundParametricStudyTool(_3600.AbstractAssemblyCompoundParametricStudyTool):
    '''AssemblyCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundParametricStudyTool.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_3468.AssemblyParametricStudyTool]':
        '''List[AssemblyParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3468.AssemblyParametricStudyTool))
        return value

    @property
    def assembly_parametric_study_tool_load_cases(self) -> 'List[_3468.AssemblyParametricStudyTool]':
        '''List[AssemblyParametricStudyTool]: 'AssemblyParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyParametricStudyToolLoadCases, constructor.new(_3468.AssemblyParametricStudyTool))
        return value

    @property
    def bearings(self) -> 'List[_3606.BearingCompoundParametricStudyTool]':
        '''List[BearingCompoundParametricStudyTool]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3606.BearingCompoundParametricStudyTool))
        return value

    @property
    def belt_drives(self) -> 'List[_3608.BeltDriveCompoundParametricStudyTool]':
        '''List[BeltDriveCompoundParametricStudyTool]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3608.BeltDriveCompoundParametricStudyTool))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3611.BevelDifferentialGearSetCompoundParametricStudyTool]':
        '''List[BevelDifferentialGearSetCompoundParametricStudyTool]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3611.BevelDifferentialGearSetCompoundParametricStudyTool))
        return value

    @property
    def bolts(self) -> 'List[_3617.BoltCompoundParametricStudyTool]':
        '''List[BoltCompoundParametricStudyTool]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3617.BoltCompoundParametricStudyTool))
        return value

    @property
    def bolted_joints(self) -> 'List[_3618.BoltedJointCompoundParametricStudyTool]':
        '''List[BoltedJointCompoundParametricStudyTool]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3618.BoltedJointCompoundParametricStudyTool))
        return value

    @property
    def clutches(self) -> 'List[_3619.ClutchCompoundParametricStudyTool]':
        '''List[ClutchCompoundParametricStudyTool]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3619.ClutchCompoundParametricStudyTool))
        return value

    @property
    def concept_couplings(self) -> 'List[_3624.ConceptCouplingCompoundParametricStudyTool]':
        '''List[ConceptCouplingCompoundParametricStudyTool]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3624.ConceptCouplingCompoundParametricStudyTool))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3629.ConceptGearSetCompoundParametricStudyTool]':
        '''List[ConceptGearSetCompoundParametricStudyTool]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3629.ConceptGearSetCompoundParametricStudyTool))
        return value

    @property
    def cv_ts(self) -> 'List[_3639.CVTCompoundParametricStudyTool]':
        '''List[CVTCompoundParametricStudyTool]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3639.CVTCompoundParametricStudyTool))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3643.CylindricalGearSetCompoundParametricStudyTool]':
        '''List[CylindricalGearSetCompoundParametricStudyTool]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3643.CylindricalGearSetCompoundParametricStudyTool))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3649.FaceGearSetCompoundParametricStudyTool]':
        '''List[FaceGearSetCompoundParametricStudyTool]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3649.FaceGearSetCompoundParametricStudyTool))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3650.FlexiblePinAssemblyCompoundParametricStudyTool]':
        '''List[FlexiblePinAssemblyCompoundParametricStudyTool]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3650.FlexiblePinAssemblyCompoundParametricStudyTool))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3657.HypoidGearSetCompoundParametricStudyTool]':
        '''List[HypoidGearSetCompoundParametricStudyTool]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3657.HypoidGearSetCompoundParametricStudyTool))
        return value

    @property
    def imported_fe_components(self) -> 'List[_3658.ImportedFEComponentCompoundParametricStudyTool]':
        '''List[ImportedFEComponentCompoundParametricStudyTool]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_3658.ImportedFEComponentCompoundParametricStudyTool))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3665.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3665.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3668.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3668.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool))
        return value

    @property
    def mass_discs(self) -> 'List[_3669.MassDiscCompoundParametricStudyTool]':
        '''List[MassDiscCompoundParametricStudyTool]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3669.MassDiscCompoundParametricStudyTool))
        return value

    @property
    def measurement_components(self) -> 'List[_3670.MeasurementComponentCompoundParametricStudyTool]':
        '''List[MeasurementComponentCompoundParametricStudyTool]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3670.MeasurementComponentCompoundParametricStudyTool))
        return value

    @property
    def oil_seals(self) -> 'List[_3672.OilSealCompoundParametricStudyTool]':
        '''List[OilSealCompoundParametricStudyTool]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3672.OilSealCompoundParametricStudyTool))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3674.PartToPartShearCouplingCompoundParametricStudyTool]':
        '''List[PartToPartShearCouplingCompoundParametricStudyTool]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3674.PartToPartShearCouplingCompoundParametricStudyTool))
        return value

    @property
    def planet_carriers(self) -> 'List[_3679.PlanetCarrierCompoundParametricStudyTool]':
        '''List[PlanetCarrierCompoundParametricStudyTool]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3679.PlanetCarrierCompoundParametricStudyTool))
        return value

    @property
    def point_loads(self) -> 'List[_3680.PointLoadCompoundParametricStudyTool]':
        '''List[PointLoadCompoundParametricStudyTool]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3680.PointLoadCompoundParametricStudyTool))
        return value

    @property
    def power_loads(self) -> 'List[_3681.PowerLoadCompoundParametricStudyTool]':
        '''List[PowerLoadCompoundParametricStudyTool]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3681.PowerLoadCompoundParametricStudyTool))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3688.ShaftHubConnectionCompoundParametricStudyTool]':
        '''List[ShaftHubConnectionCompoundParametricStudyTool]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3688.ShaftHubConnectionCompoundParametricStudyTool))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3683.RollingRingAssemblyCompoundParametricStudyTool]':
        '''List[RollingRingAssemblyCompoundParametricStudyTool]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3683.RollingRingAssemblyCompoundParametricStudyTool))
        return value

    @property
    def shafts(self) -> 'List[_3687.ShaftCompoundParametricStudyTool]':
        '''List[ShaftCompoundParametricStudyTool]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3687.ShaftCompoundParametricStudyTool))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3693.SpiralBevelGearSetCompoundParametricStudyTool]':
        '''List[SpiralBevelGearSetCompoundParametricStudyTool]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3693.SpiralBevelGearSetCompoundParametricStudyTool))
        return value

    @property
    def spring_dampers(self) -> 'List[_3694.SpringDamperCompoundParametricStudyTool]':
        '''List[SpringDamperCompoundParametricStudyTool]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3694.SpringDamperCompoundParametricStudyTool))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3699.StraightBevelDiffGearSetCompoundParametricStudyTool]':
        '''List[StraightBevelDiffGearSetCompoundParametricStudyTool]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3699.StraightBevelDiffGearSetCompoundParametricStudyTool))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3702.StraightBevelGearSetCompoundParametricStudyTool]':
        '''List[StraightBevelGearSetCompoundParametricStudyTool]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3702.StraightBevelGearSetCompoundParametricStudyTool))
        return value

    @property
    def synchronisers(self) -> 'List[_3705.SynchroniserCompoundParametricStudyTool]':
        '''List[SynchroniserCompoundParametricStudyTool]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3705.SynchroniserCompoundParametricStudyTool))
        return value

    @property
    def torque_converters(self) -> 'List[_3709.TorqueConverterCompoundParametricStudyTool]':
        '''List[TorqueConverterCompoundParametricStudyTool]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3709.TorqueConverterCompoundParametricStudyTool))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3713.UnbalancedMassCompoundParametricStudyTool]':
        '''List[UnbalancedMassCompoundParametricStudyTool]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3713.UnbalancedMassCompoundParametricStudyTool))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3717.WormGearSetCompoundParametricStudyTool]':
        '''List[WormGearSetCompoundParametricStudyTool]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3717.WormGearSetCompoundParametricStudyTool))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3720.ZerolBevelGearSetCompoundParametricStudyTool]':
        '''List[ZerolBevelGearSetCompoundParametricStudyTool]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3720.ZerolBevelGearSetCompoundParametricStudyTool))
        return value
