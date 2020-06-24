'''_6413.py

GearSetCompoundAdvancedSystemDeflection
'''


from mastapy.gears.rating import _164
from mastapy._internal import constructor
from mastapy.gears.rating.worm import _177
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _251
from mastapy.gears.rating.cylindrical import _263
from mastapy.gears.rating.conical import _326
from mastapy.gears.rating.concept import _337
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _6450
from mastapy._internal.python_net import python_net_import

_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'GearSetCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetCompoundAdvancedSystemDeflection',)


class GearSetCompoundAdvancedSystemDeflection(_6450.SpecialisedAssemblyCompoundAdvancedSystemDeflection):
    '''GearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_duty_cycle_rating(self) -> '_164.GearSetDutyCycleRating':
        '''GearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_164.GearSetDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def gear_duty_cycle_rating_of_type_worm_gear_set_duty_cycle_rating(self) -> '_177.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _177.WormGearSetDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to WormGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleRating.__class__.__qualname__))

        return constructor.new(_177.WormGearSetDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def gear_duty_cycle_rating_of_type_face_gear_set_duty_cycle_rating(self) -> '_251.FaceGearSetDutyCycleRating':
        '''FaceGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _251.FaceGearSetDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to FaceGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleRating.__class__.__qualname__))

        return constructor.new(_251.FaceGearSetDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def gear_duty_cycle_rating_of_type_cylindrical_gear_set_duty_cycle_rating(self) -> '_263.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _263.CylindricalGearSetDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to CylindricalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleRating.__class__.__qualname__))

        return constructor.new(_263.CylindricalGearSetDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def gear_duty_cycle_rating_of_type_conical_gear_set_duty_cycle_rating(self) -> '_326.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _326.ConicalGearSetDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to ConicalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleRating.__class__.__qualname__))

        return constructor.new(_326.ConicalGearSetDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def gear_duty_cycle_rating_of_type_concept_gear_set_duty_cycle_rating(self) -> '_337.ConceptGearSetDutyCycleRating':
        '''ConceptGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _337.ConceptGearSetDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to ConceptGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleRating.__class__.__qualname__))

        return constructor.new(_337.ConceptGearSetDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None
