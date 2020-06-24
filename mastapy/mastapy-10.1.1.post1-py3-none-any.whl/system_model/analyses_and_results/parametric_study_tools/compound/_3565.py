'''_3565.py

AssemblyCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _1904
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4040
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
    _3557, _3503, _3588, _3558,
    _3559, _3504, _3506, _3582,
    _3510, _3596, _3584, _3564,
    _3601, _3567, _3605, _3607,
    _3568, _3569, _3571, _3573,
    _3574, _3575, _3513, _3515,
    _3580, _3610, _3516, _3612,
    _3614, _3518, _3522, _3578,
    _3500, _3502, _3555
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'AssemblyCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundParametricStudyTool',)


class AssemblyCompoundParametricStudyTool(_3555.AbstractAssemblyCompoundParametricStudyTool):
    '''AssemblyCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundParametricStudyTool.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_4040.AssemblyParametricStudyTool]':
        '''List[AssemblyParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4040.AssemblyParametricStudyTool))
        return value

    @property
    def assembly_parametric_study_tool_load_cases(self) -> 'List[_4040.AssemblyParametricStudyTool]':
        '''List[AssemblyParametricStudyTool]: 'AssemblyParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyParametricStudyToolLoadCases, constructor.new(_4040.AssemblyParametricStudyTool))
        return value

    @property
    def bearings(self) -> 'List[_3557.BearingCompoundParametricStudyTool]':
        '''List[BearingCompoundParametricStudyTool]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3557.BearingCompoundParametricStudyTool))
        return value

    @property
    def belt_drives(self) -> 'List[_3503.BeltDriveCompoundParametricStudyTool]':
        '''List[BeltDriveCompoundParametricStudyTool]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3503.BeltDriveCompoundParametricStudyTool))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3588.BevelDifferentialGearSetCompoundParametricStudyTool]':
        '''List[BevelDifferentialGearSetCompoundParametricStudyTool]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3588.BevelDifferentialGearSetCompoundParametricStudyTool))
        return value

    @property
    def bolts(self) -> 'List[_3558.BoltCompoundParametricStudyTool]':
        '''List[BoltCompoundParametricStudyTool]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3558.BoltCompoundParametricStudyTool))
        return value

    @property
    def bolted_joints(self) -> 'List[_3559.BoltedJointCompoundParametricStudyTool]':
        '''List[BoltedJointCompoundParametricStudyTool]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3559.BoltedJointCompoundParametricStudyTool))
        return value

    @property
    def clutches(self) -> 'List[_3504.ClutchCompoundParametricStudyTool]':
        '''List[ClutchCompoundParametricStudyTool]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3504.ClutchCompoundParametricStudyTool))
        return value

    @property
    def concept_couplings(self) -> 'List[_3506.ConceptCouplingCompoundParametricStudyTool]':
        '''List[ConceptCouplingCompoundParametricStudyTool]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3506.ConceptCouplingCompoundParametricStudyTool))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3582.ConceptGearSetCompoundParametricStudyTool]':
        '''List[ConceptGearSetCompoundParametricStudyTool]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3582.ConceptGearSetCompoundParametricStudyTool))
        return value

    @property
    def cv_ts(self) -> 'List[_3510.CVTCompoundParametricStudyTool]':
        '''List[CVTCompoundParametricStudyTool]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3510.CVTCompoundParametricStudyTool))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3596.CylindricalGearSetCompoundParametricStudyTool]':
        '''List[CylindricalGearSetCompoundParametricStudyTool]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3596.CylindricalGearSetCompoundParametricStudyTool))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3584.FaceGearSetCompoundParametricStudyTool]':
        '''List[FaceGearSetCompoundParametricStudyTool]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3584.FaceGearSetCompoundParametricStudyTool))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3564.FlexiblePinAssemblyCompoundParametricStudyTool]':
        '''List[FlexiblePinAssemblyCompoundParametricStudyTool]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3564.FlexiblePinAssemblyCompoundParametricStudyTool))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3601.HypoidGearSetCompoundParametricStudyTool]':
        '''List[HypoidGearSetCompoundParametricStudyTool]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3601.HypoidGearSetCompoundParametricStudyTool))
        return value

    @property
    def imported_fe_components(self) -> 'List[_3567.ImportedFEComponentCompoundParametricStudyTool]':
        '''List[ImportedFEComponentCompoundParametricStudyTool]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_3567.ImportedFEComponentCompoundParametricStudyTool))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3605.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3605.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3607.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3607.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool))
        return value

    @property
    def mass_discs(self) -> 'List[_3568.MassDiscCompoundParametricStudyTool]':
        '''List[MassDiscCompoundParametricStudyTool]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3568.MassDiscCompoundParametricStudyTool))
        return value

    @property
    def measurement_components(self) -> 'List[_3569.MeasurementComponentCompoundParametricStudyTool]':
        '''List[MeasurementComponentCompoundParametricStudyTool]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3569.MeasurementComponentCompoundParametricStudyTool))
        return value

    @property
    def oil_seals(self) -> 'List[_3571.OilSealCompoundParametricStudyTool]':
        '''List[OilSealCompoundParametricStudyTool]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3571.OilSealCompoundParametricStudyTool))
        return value

    @property
    def planet_carriers(self) -> 'List[_3573.PlanetCarrierCompoundParametricStudyTool]':
        '''List[PlanetCarrierCompoundParametricStudyTool]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3573.PlanetCarrierCompoundParametricStudyTool))
        return value

    @property
    def point_loads(self) -> 'List[_3574.PointLoadCompoundParametricStudyTool]':
        '''List[PointLoadCompoundParametricStudyTool]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3574.PointLoadCompoundParametricStudyTool))
        return value

    @property
    def power_loads(self) -> 'List[_3575.PowerLoadCompoundParametricStudyTool]':
        '''List[PowerLoadCompoundParametricStudyTool]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3575.PowerLoadCompoundParametricStudyTool))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3513.ShaftHubConnectionCompoundParametricStudyTool]':
        '''List[ShaftHubConnectionCompoundParametricStudyTool]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3513.ShaftHubConnectionCompoundParametricStudyTool))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3515.RollingRingAssemblyCompoundParametricStudyTool]':
        '''List[RollingRingAssemblyCompoundParametricStudyTool]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3515.RollingRingAssemblyCompoundParametricStudyTool))
        return value

    @property
    def shafts(self) -> 'List[_3580.ShaftCompoundParametricStudyTool]':
        '''List[ShaftCompoundParametricStudyTool]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3580.ShaftCompoundParametricStudyTool))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3610.SpiralBevelGearSetCompoundParametricStudyTool]':
        '''List[SpiralBevelGearSetCompoundParametricStudyTool]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3610.SpiralBevelGearSetCompoundParametricStudyTool))
        return value

    @property
    def spring_dampers(self) -> 'List[_3516.SpringDamperCompoundParametricStudyTool]':
        '''List[SpringDamperCompoundParametricStudyTool]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3516.SpringDamperCompoundParametricStudyTool))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3612.StraightBevelDiffGearSetCompoundParametricStudyTool]':
        '''List[StraightBevelDiffGearSetCompoundParametricStudyTool]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3612.StraightBevelDiffGearSetCompoundParametricStudyTool))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3614.StraightBevelGearSetCompoundParametricStudyTool]':
        '''List[StraightBevelGearSetCompoundParametricStudyTool]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3614.StraightBevelGearSetCompoundParametricStudyTool))
        return value

    @property
    def synchronisers(self) -> 'List[_3518.SynchroniserCompoundParametricStudyTool]':
        '''List[SynchroniserCompoundParametricStudyTool]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3518.SynchroniserCompoundParametricStudyTool))
        return value

    @property
    def torque_converters(self) -> 'List[_3522.TorqueConverterCompoundParametricStudyTool]':
        '''List[TorqueConverterCompoundParametricStudyTool]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3522.TorqueConverterCompoundParametricStudyTool))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3578.UnbalancedMassCompoundParametricStudyTool]':
        '''List[UnbalancedMassCompoundParametricStudyTool]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3578.UnbalancedMassCompoundParametricStudyTool))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3500.WormGearSetCompoundParametricStudyTool]':
        '''List[WormGearSetCompoundParametricStudyTool]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3500.WormGearSetCompoundParametricStudyTool))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3502.ZerolBevelGearSetCompoundParametricStudyTool]':
        '''List[ZerolBevelGearSetCompoundParametricStudyTool]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3502.ZerolBevelGearSetCompoundParametricStudyTool))
        return value
