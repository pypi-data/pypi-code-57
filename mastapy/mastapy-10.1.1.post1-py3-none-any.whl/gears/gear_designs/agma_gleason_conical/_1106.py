'''_1106.py

AGMAGleasonConicalGearMeshDesign
'''


from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable, enum_with_selected_value
from mastapy.gears.rating.iso_10300 import (
    _458, _457, _459, _433
)
from mastapy.gears.gear_designs.conical import _598, _895
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.AGMAGleasonConical', 'AGMAGleasonConicalGearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearMeshDesign',)


class AGMAGleasonConicalGearMeshDesign(_895.ConicalGearMeshDesign):
    '''AGMAGleasonConicalGearMeshDesign

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_MESH_DESIGN
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def pinion_face_width_offset(self) -> 'float':
        '''float: 'PinionFaceWidthOffset' is the original name of this property.'''

        return self.wrapped.PinionFaceWidthOffset

    @pinion_face_width_offset.setter
    def pinion_face_width_offset(self, value: 'float'):
        self.wrapped.PinionFaceWidthOffset = float(value) if value else 0.0

    @property
    def net_face_width(self) -> 'float':
        '''float: 'NetFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NetFaceWidth

    @property
    def dynamic_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'DynamicFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.DynamicFactor) if self.wrapped.DynamicFactor else None

    @dynamic_factor.setter
    def dynamic_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.DynamicFactor = value

    @property
    def size_factor_bending(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SizeFactorBending' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SizeFactorBending) if self.wrapped.SizeFactorBending else None

    @size_factor_bending.setter
    def size_factor_bending(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.SizeFactorBending = value

    @property
    def size_factor_contact(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SizeFactorContact' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SizeFactorContact) if self.wrapped.SizeFactorContact else None

    @size_factor_contact.setter
    def size_factor_contact(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.SizeFactorContact = value

    @property
    def surface_condition_factor(self) -> 'float':
        '''float: 'SurfaceConditionFactor' is the original name of this property.'''

        return self.wrapped.SurfaceConditionFactor

    @surface_condition_factor.setter
    def surface_condition_factor(self, value: 'float'):
        self.wrapped.SurfaceConditionFactor = float(value) if value else 0.0

    @property
    def temperature_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TemperatureFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TemperatureFactor) if self.wrapped.TemperatureFactor else None

    @temperature_factor.setter
    def temperature_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.TemperatureFactor = value

    @property
    def hardness_ratio_factor(self) -> 'float':
        '''float: 'HardnessRatioFactor' is the original name of this property.'''

        return self.wrapped.HardnessRatioFactor

    @hardness_ratio_factor.setter
    def hardness_ratio_factor(self, value: 'float'):
        self.wrapped.HardnessRatioFactor = float(value) if value else 0.0

    @property
    def tooth_lengthwise_curvature_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToothLengthwiseCurvatureFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToothLengthwiseCurvatureFactor) if self.wrapped.ToothLengthwiseCurvatureFactor else None

    @tooth_lengthwise_curvature_factor.setter
    def tooth_lengthwise_curvature_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ToothLengthwiseCurvatureFactor = value

    @property
    def crowning_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'CrowningFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.CrowningFactor) if self.wrapped.CrowningFactor else None

    @crowning_factor.setter
    def crowning_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.CrowningFactor = value

    @property
    def crowned(self) -> 'bool':
        '''bool: 'Crowned' is the original name of this property.'''

        return self.wrapped.Crowned

    @crowned.setter
    def crowned(self, value: 'bool'):
        self.wrapped.Crowned = bool(value) if value else False

    @property
    def wheel_effective_face_width_factor(self) -> 'float':
        '''float: 'WheelEffectiveFaceWidthFactor' is the original name of this property.'''

        return self.wrapped.WheelEffectiveFaceWidthFactor

    @wheel_effective_face_width_factor.setter
    def wheel_effective_face_width_factor(self, value: 'float'):
        self.wrapped.WheelEffectiveFaceWidthFactor = float(value) if value else 0.0

    @property
    def profile_crowning_setting(self) -> '_458.ProfileCrowningSetting':
        '''ProfileCrowningSetting: 'ProfileCrowningSetting' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ProfileCrowningSetting)
        return constructor.new(_458.ProfileCrowningSetting)(value) if value else None

    @profile_crowning_setting.setter
    def profile_crowning_setting(self, value: '_458.ProfileCrowningSetting'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ProfileCrowningSetting = value

    @property
    def load_distribution_factor_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LoadDistributionFactorMethods':
        '''enum_with_selected_value.EnumWithSelectedValue_LoadDistributionFactorMethods: 'LoadDistributionFactorMethod' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_LoadDistributionFactorMethods)(self.wrapped.LoadDistributionFactorMethod) if self.wrapped.LoadDistributionFactorMethod else None

    @load_distribution_factor_method.setter
    def load_distribution_factor_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LoadDistributionFactorMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_LoadDistributionFactorMethods.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LoadDistributionFactorMethods.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.LoadDistributionFactorMethod = value

    @property
    def load_distribution_factor(self) -> 'float':
        '''float: 'LoadDistributionFactor' is the original name of this property.'''

        return self.wrapped.LoadDistributionFactor

    @load_distribution_factor.setter
    def load_distribution_factor(self, value: 'float'):
        self.wrapped.LoadDistributionFactor = float(value) if value else 0.0

    @property
    def mounting_conditions_of_pinion_and_wheel(self) -> '_457.MountingConditionsOfPinionAndWheel':
        '''MountingConditionsOfPinionAndWheel: 'MountingConditionsOfPinionAndWheel' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MountingConditionsOfPinionAndWheel)
        return constructor.new(_457.MountingConditionsOfPinionAndWheel)(value) if value else None

    @mounting_conditions_of_pinion_and_wheel.setter
    def mounting_conditions_of_pinion_and_wheel(self, value: '_457.MountingConditionsOfPinionAndWheel'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MountingConditionsOfPinionAndWheel = value

    @property
    def verification_of_contact_pattern(self) -> '_459.VerificationOfContactPattern':
        '''VerificationOfContactPattern: 'VerificationOfContactPattern' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.VerificationOfContactPattern)
        return constructor.new(_459.VerificationOfContactPattern)(value) if value else None

    @verification_of_contact_pattern.setter
    def verification_of_contact_pattern(self, value: '_459.VerificationOfContactPattern'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.VerificationOfContactPattern = value

    @property
    def iso10300_gear_set_finishing_methods(self) -> '_433.Iso10300FinishingMethods':
        '''Iso10300FinishingMethods: 'ISO10300GearSetFinishingMethods' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ISO10300GearSetFinishingMethods)
        return constructor.new(_433.Iso10300FinishingMethods)(value) if value else None

    @iso10300_gear_set_finishing_methods.setter
    def iso10300_gear_set_finishing_methods(self, value: '_433.Iso10300FinishingMethods'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ISO10300GearSetFinishingMethods = value
