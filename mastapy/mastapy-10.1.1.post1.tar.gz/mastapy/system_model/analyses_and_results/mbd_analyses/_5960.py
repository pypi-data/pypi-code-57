'''_5960.py

GearMeshMultiBodyDynamicsAnalysis
'''


from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis import _94
from mastapy.system_model.connections_and_sockets.gears import (
    _1802, _1794, _1798, _1800,
    _1818, _1804, _1790, _1812,
    _1814, _1816, _1820, _1808,
    _1809
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.mbd_analyses import _5973
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'GearMeshMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshMultiBodyDynamicsAnalysis',)


class GearMeshMultiBodyDynamicsAnalysis(_5973.InterMountableComponentConnectionMultiBodyDynamicsAnalysis):
    '''GearMeshMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def normal_stiffness(self) -> 'float':
        '''float: 'NormalStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalStiffness

    @property
    def normal_stiffness_left_flank(self) -> 'float':
        '''float: 'NormalStiffnessLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalStiffnessLeftFlank

    @property
    def normal_stiffness_right_flank(self) -> 'float':
        '''float: 'NormalStiffnessRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalStiffnessRightFlank

    @property
    def transverse_stiffness_left_flank(self) -> 'float':
        '''float: 'TransverseStiffnessLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseStiffnessLeftFlank

    @property
    def transverse_stiffness_right_flank(self) -> 'float':
        '''float: 'TransverseStiffnessRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseStiffnessRightFlank

    @property
    def tilt_stiffness(self) -> 'float':
        '''float: 'TiltStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TiltStiffness

    @property
    def contact_status(self) -> '_94.GearMeshContactStatus':
        '''GearMeshContactStatus: 'ContactStatus' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.ContactStatus)
        return constructor.new(_94.GearMeshContactStatus)(value) if value else None

    @property
    def separation(self) -> 'float':
        '''float: 'Separation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Separation

    @property
    def separation_normal_to_left_flank(self) -> 'float':
        '''float: 'SeparationNormalToLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SeparationNormalToLeftFlank

    @property
    def separation_normal_to_right_flank(self) -> 'float':
        '''float: 'SeparationNormalToRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SeparationNormalToRightFlank

    @property
    def separation_transverse_to_left_flank(self) -> 'float':
        '''float: 'SeparationTransverseToLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SeparationTransverseToLeftFlank

    @property
    def separation_transverse_to_right_flank(self) -> 'float':
        '''float: 'SeparationTransverseToRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SeparationTransverseToRightFlank

    @property
    def force_normal_to_left_flank(self) -> 'float':
        '''float: 'ForceNormalToLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceNormalToLeftFlank

    @property
    def force_normal_to_right_flank(self) -> 'float':
        '''float: 'ForceNormalToRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceNormalToRightFlank

    @property
    def average_sliding_velocity_left_flank(self) -> 'float':
        '''float: 'AverageSlidingVelocityLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AverageSlidingVelocityLeftFlank

    @property
    def average_sliding_velocity_right_flank(self) -> 'float':
        '''float: 'AverageSlidingVelocityRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AverageSlidingVelocityRightFlank

    @property
    def pitch_line_velocity_left_flank(self) -> 'float':
        '''float: 'PitchLineVelocityLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PitchLineVelocityLeftFlank

    @property
    def pitch_line_velocity_right_flank(self) -> 'float':
        '''float: 'PitchLineVelocityRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PitchLineVelocityRightFlank

    @property
    def misalignment_due_to_tilt_right_flank(self) -> 'float':
        '''float: 'MisalignmentDueToTiltRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MisalignmentDueToTiltRightFlank

    @property
    def misalignment_due_to_tilt_left_flank(self) -> 'float':
        '''float: 'MisalignmentDueToTiltLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MisalignmentDueToTiltLeftFlank

    @property
    def equivalent_misalignment_left_flank(self) -> 'float':
        '''float: 'EquivalentMisalignmentLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EquivalentMisalignmentLeftFlank

    @property
    def equivalent_misalignment_right_flank(self) -> 'float':
        '''float: 'EquivalentMisalignmentRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EquivalentMisalignmentRightFlank

    @property
    def mesh_power_loss(self) -> 'float':
        '''float: 'MeshPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshPowerLoss

    @property
    def coefficient_of_friction_left_flank(self) -> 'float':
        '''float: 'CoefficientOfFrictionLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CoefficientOfFrictionLeftFlank

    @property
    def coefficient_of_friction_right_flank(self) -> 'float':
        '''float: 'CoefficientOfFrictionRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CoefficientOfFrictionRightFlank

    @property
    def tooth_passing_frequency(self) -> 'float':
        '''float: 'ToothPassingFrequency' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothPassingFrequency

    @property
    def tooth_passing_speed_gear_a(self) -> 'float':
        '''float: 'ToothPassingSpeedGearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothPassingSpeedGearA

    @property
    def tooth_passing_speed_gear_b(self) -> 'float':
        '''float: 'ToothPassingSpeedGearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothPassingSpeedGearB

    @property
    def strain_energy_left_flank(self) -> 'float':
        '''float: 'StrainEnergyLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StrainEnergyLeftFlank

    @property
    def strain_energy_right_flank(self) -> 'float':
        '''float: 'StrainEnergyRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StrainEnergyRightFlank

    @property
    def strain_energy_total(self) -> 'float':
        '''float: 'StrainEnergyTotal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StrainEnergyTotal

    @property
    def connection_design(self) -> '_1802.GearMesh':
        '''GearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1802.GearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_concept_gear_mesh(self) -> '_1794.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'ConceptGearMesh':
            raise CastException('Failed to cast connection_design to ConceptGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1794.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cylindrical_gear_mesh(self) -> '_1798.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'CylindricalGearMesh':
            raise CastException('Failed to cast connection_design to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1798.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_face_gear_mesh(self) -> '_1800.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'FaceGearMesh':
            raise CastException('Failed to cast connection_design to FaceGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1800.FaceGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_worm_gear_mesh(self) -> '_1818.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'WormGearMesh':
            raise CastException('Failed to cast connection_design to WormGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1818.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_hypoid_gear_mesh(self) -> '_1804.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'HypoidGearMesh':
            raise CastException('Failed to cast connection_design to HypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1804.HypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_differential_gear_mesh(self) -> '_1790.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'BevelDifferentialGearMesh':
            raise CastException('Failed to cast connection_design to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1790.BevelDifferentialGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_spiral_bevel_gear_mesh(self) -> '_1812.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'SpiralBevelGearMesh':
            raise CastException('Failed to cast connection_design to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1812.SpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_diff_gear_mesh(self) -> '_1814.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'StraightBevelDiffGearMesh':
            raise CastException('Failed to cast connection_design to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1814.StraightBevelDiffGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_gear_mesh(self) -> '_1816.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'StraightBevelGearMesh':
            raise CastException('Failed to cast connection_design to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1816.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_zerol_bevel_gear_mesh(self) -> '_1820.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'ZerolBevelGearMesh':
            raise CastException('Failed to cast connection_design to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1820.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_1808.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGearMesh':
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1808.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGearMesh':
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
