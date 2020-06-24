'''_984.py

CylindricalMeshedGear
'''


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _560
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MESHED_GEAR = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalMeshedGear')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalMeshedGear',)


class CylindricalMeshedGear(_1.APIBase):
    '''CylindricalMeshedGear

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_MESHED_GEAR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalMeshedGear.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def sliding_factor_at_tooth_tip(self) -> 'float':
        '''float: 'SlidingFactorAtToothTip' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SlidingFactorAtToothTip

    @property
    def load_direction_angle(self) -> 'float':
        '''float: 'LoadDirectionAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadDirectionAngle

    @property
    def clearance_from_form_diameter_to_sap_diameter(self) -> 'float':
        '''float: 'ClearanceFromFormDiameterToSAPDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ClearanceFromFormDiameterToSAPDiameter

    @property
    def dedendum_path_of_contact(self) -> 'float':
        '''float: 'DedendumPathOfContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DedendumPathOfContact

    @property
    def specific_sliding_at_sap(self) -> 'float':
        '''float: 'SpecificSlidingAtSAP' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpecificSlidingAtSAP

    @property
    def specific_sliding_at_eap(self) -> 'float':
        '''float: 'SpecificSlidingAtEAP' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpecificSlidingAtEAP

    @property
    def working_pitch_diameter(self) -> 'float':
        '''float: 'WorkingPitchDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WorkingPitchDiameter

    @property
    def face_width_to_working_pitch_diameter_ratio(self) -> 'float':
        '''float: 'FaceWidthToWorkingPitchDiameterRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FaceWidthToWorkingPitchDiameterRatio

    @property
    def effective_face_width_to_reference_diameter_ratio(self) -> 'float':
        '''float: 'EffectiveFaceWidthToReferenceDiameterRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EffectiveFaceWidthToReferenceDiameterRatio

    @property
    def tip_clearance_factor(self) -> 'float':
        '''float: 'TipClearanceFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TipClearanceFactor

    @property
    def tip_clearance_at_tight_mesh_maximum_metal(self) -> 'float':
        '''float: 'TipClearanceAtTightMeshMaximumMetal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TipClearanceAtTightMeshMaximumMetal

    @property
    def tip_clearance_at_tight_mesh_minimum_metal(self) -> 'float':
        '''float: 'TipClearanceAtTightMeshMinimumMetal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TipClearanceAtTightMeshMinimumMetal

    @property
    def tip_clearance(self) -> 'float':
        '''float: 'TipClearance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TipClearance

    @property
    def form_over_dimension(self) -> 'float':
        '''float: 'FormOverDimension' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FormOverDimension

    @property
    def length_of_addendum_path_of_contact(self) -> 'float':
        '''float: 'LengthOfAddendumPathOfContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LengthOfAddendumPathOfContact

    @property
    def partial_contact_ratio(self) -> 'float':
        '''float: 'PartialContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PartialContactRatio

    @property
    def profile_line_length_of_the_active_tooth_flank(self) -> 'float':
        '''float: 'ProfileLineLengthOfTheActiveToothFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ProfileLineLengthOfTheActiveToothFlank

    @property
    def lowest_point_of_fewest_tooth_contacts(self) -> '_560.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'LowestPointOfFewestToothContacts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_560.CylindricalGearProfileMeasurement)(self.wrapped.LowestPointOfFewestToothContacts) if self.wrapped.LowestPointOfFewestToothContacts else None

    @property
    def highest_point_of_fewest_tooth_contacts(self) -> '_560.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'HighestPointOfFewestToothContacts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_560.CylindricalGearProfileMeasurement)(self.wrapped.HighestPointOfFewestToothContacts) if self.wrapped.HighestPointOfFewestToothContacts else None

    @property
    def start_of_active_profile(self) -> '_560.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'StartOfActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_560.CylindricalGearProfileMeasurement)(self.wrapped.StartOfActiveProfile) if self.wrapped.StartOfActiveProfile else None

    @property
    def end_of_active_profile(self) -> '_560.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'EndOfActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_560.CylindricalGearProfileMeasurement)(self.wrapped.EndOfActiveProfile) if self.wrapped.EndOfActiveProfile else None
