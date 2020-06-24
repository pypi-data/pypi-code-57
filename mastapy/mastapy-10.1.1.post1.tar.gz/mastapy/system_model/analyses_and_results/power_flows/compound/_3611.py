'''_3611.py

GearMeshCompoundPowerFlow
'''


from mastapy.gears.rating import _340
from mastapy._internal import constructor
from mastapy.gears.rating.worm import _390
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _468
from mastapy.gears.rating.cylindrical import _484
from mastapy.gears.rating.conical import _542
from mastapy.gears.rating.concept import _545
from mastapy.system_model.analyses_and_results.power_flows.compound import _3586
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'GearMeshCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshCompoundPowerFlow',)


class GearMeshCompoundPowerFlow(_3586.InterMountableComponentConnectionCompoundPowerFlow):
    '''GearMeshCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_mesh_duty_cycle_rating(self) -> '_340.MeshDutyCycleRating':
        '''MeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_340.MeshDutyCycleRating)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None

    @property
    def gear_mesh_duty_cycle_rating_of_type_worm_mesh_duty_cycle_rating(self) -> '_390.WormMeshDutyCycleRating':
        '''WormMeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__ != 'WormMeshDutyCycleRating':
            raise CastException('Failed to cast gear_mesh_duty_cycle_rating to WormMeshDutyCycleRating. Expected: {}.'.format(self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__))

        return constructor.new(_390.WormMeshDutyCycleRating)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None

    @property
    def gear_mesh_duty_cycle_rating_of_type_face_gear_mesh_duty_cycle_rating(self) -> '_468.FaceGearMeshDutyCycleRating':
        '''FaceGearMeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__ != 'FaceGearMeshDutyCycleRating':
            raise CastException('Failed to cast gear_mesh_duty_cycle_rating to FaceGearMeshDutyCycleRating. Expected: {}.'.format(self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__))

        return constructor.new(_468.FaceGearMeshDutyCycleRating)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None

    @property
    def gear_mesh_duty_cycle_rating_of_type_cylindrical_mesh_duty_cycle_rating(self) -> '_484.CylindricalMeshDutyCycleRating':
        '''CylindricalMeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__ != 'CylindricalMeshDutyCycleRating':
            raise CastException('Failed to cast gear_mesh_duty_cycle_rating to CylindricalMeshDutyCycleRating. Expected: {}.'.format(self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__))

        return constructor.new(_484.CylindricalMeshDutyCycleRating)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None

    @property
    def gear_mesh_duty_cycle_rating_of_type_conical_mesh_duty_cycle_rating(self) -> '_542.ConicalMeshDutyCycleRating':
        '''ConicalMeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__ != 'ConicalMeshDutyCycleRating':
            raise CastException('Failed to cast gear_mesh_duty_cycle_rating to ConicalMeshDutyCycleRating. Expected: {}.'.format(self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__))

        return constructor.new(_542.ConicalMeshDutyCycleRating)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None

    @property
    def gear_mesh_duty_cycle_rating_of_type_concept_gear_mesh_duty_cycle_rating(self) -> '_545.ConceptGearMeshDutyCycleRating':
        '''ConceptGearMeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__ != 'ConceptGearMeshDutyCycleRating':
            raise CastException('Failed to cast gear_mesh_duty_cycle_rating to ConceptGearMeshDutyCycleRating. Expected: {}.'.format(self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__))

        return constructor.new(_545.ConceptGearMeshDutyCycleRating)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None
