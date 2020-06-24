'''_2566.py

GearCompoundSystemDeflection
'''


from mastapy.gears.rating import _329
from mastapy._internal import constructor
from mastapy.gears.rating.worm import _351
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _467
from mastapy.gears.rating.cylindrical import _472
from mastapy.gears.rating.conical import _543
from mastapy.gears.rating.concept import _549
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2586
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'GearCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundSystemDeflection',)


class GearCompoundSystemDeflection(_2586.MountableComponentCompoundSystemDeflection):
    '''GearCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def duty_cycle_rating(self) -> '_329.GearDutyCycleRating':
        '''GearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_329.GearDutyCycleRating)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def duty_cycle_rating_of_type_worm_gear_duty_cycle_rating(self) -> '_351.WormGearDutyCycleRating':
        '''WormGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.DutyCycleRating.__class__.__qualname__ != 'WormGearDutyCycleRating':
            raise CastException('Failed to cast duty_cycle_rating to WormGearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new(_351.WormGearDutyCycleRating)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def duty_cycle_rating_of_type_face_gear_duty_cycle_rating(self) -> '_467.FaceGearDutyCycleRating':
        '''FaceGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.DutyCycleRating.__class__.__qualname__ != 'FaceGearDutyCycleRating':
            raise CastException('Failed to cast duty_cycle_rating to FaceGearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new(_467.FaceGearDutyCycleRating)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def duty_cycle_rating_of_type_cylindrical_gear_duty_cycle_rating(self) -> '_472.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.DutyCycleRating.__class__.__qualname__ != 'CylindricalGearDutyCycleRating':
            raise CastException('Failed to cast duty_cycle_rating to CylindricalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new(_472.CylindricalGearDutyCycleRating)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def duty_cycle_rating_of_type_conical_gear_duty_cycle_rating(self) -> '_543.ConicalGearDutyCycleRating':
        '''ConicalGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.DutyCycleRating.__class__.__qualname__ != 'ConicalGearDutyCycleRating':
            raise CastException('Failed to cast duty_cycle_rating to ConicalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new(_543.ConicalGearDutyCycleRating)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None

    @property
    def duty_cycle_rating_of_type_concept_gear_duty_cycle_rating(self) -> '_549.ConceptGearDutyCycleRating':
        '''ConceptGearDutyCycleRating: 'DutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.DutyCycleRating.__class__.__qualname__ != 'ConceptGearDutyCycleRating':
            raise CastException('Failed to cast duty_cycle_rating to ConceptGearDutyCycleRating. Expected: {}.'.format(self.wrapped.DutyCycleRating.__class__.__qualname__))

        return constructor.new(_549.ConceptGearDutyCycleRating)(self.wrapped.DutyCycleRating) if self.wrapped.DutyCycleRating else None
