'''_12.py

BearingSettings
'''


from mastapy._internal.implicit import enum_with_selected_value
from mastapy.bearings import (
    _1480, _1479, _1472, _1473
)
from mastapy._internal import constructor, conversion
from mastapy.utility import _77
from mastapy._internal.python_net import python_net_import

_BEARING_SETTINGS = python_net_import('SMT.MastaAPI.Bearings', 'BearingSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingSettings',)


class BearingSettings(_77.PerMachineSettings):
    '''BearingSettings

    This is a mastapy class.
    '''

    TYPE = _BEARING_SETTINGS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingSettings.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def default_roller_profile(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes':
        '''enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes: 'DefaultRollerProfile' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes)(self.wrapped.DefaultRollerProfile) if self.wrapped.DefaultRollerProfile else None

    @default_roller_profile.setter
    def default_roller_profile(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.DefaultRollerProfile = value

    @property
    def tolerance_used_for_diameter_warnings_and_database_filter(self) -> 'float':
        '''float: 'ToleranceUsedForDiameterWarningsAndDatabaseFilter' is the original name of this property.'''

        return self.wrapped.ToleranceUsedForDiameterWarningsAndDatabaseFilter

    @tolerance_used_for_diameter_warnings_and_database_filter.setter
    def tolerance_used_for_diameter_warnings_and_database_filter(self, value: 'float'):
        self.wrapped.ToleranceUsedForDiameterWarningsAndDatabaseFilter = float(value) if value else 0.0

    @property
    def failure_probability_for_rating_life(self) -> '_1479.RatingLife':
        '''RatingLife: 'FailureProbabilityForRatingLife' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.FailureProbabilityForRatingLife)
        return constructor.new(_1479.RatingLife)(value) if value else None

    @failure_probability_for_rating_life.setter
    def failure_probability_for_rating_life(self, value: '_1479.RatingLife'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FailureProbabilityForRatingLife = value

    @property
    def use_plain_journal_bearing_misalignment_factors(self) -> 'bool':
        '''bool: 'UsePlainJournalBearingMisalignmentFactors' is the original name of this property.'''

        return self.wrapped.UsePlainJournalBearingMisalignmentFactors

    @use_plain_journal_bearing_misalignment_factors.setter
    def use_plain_journal_bearing_misalignment_factors(self, value: 'bool'):
        self.wrapped.UsePlainJournalBearingMisalignmentFactors = bool(value) if value else False

    @property
    def include_exponent_and_reduction_factors_in_isots162812008(self) -> '_1472.ExponentAndReductionFactorsInISO16281Calculation':
        '''ExponentAndReductionFactorsInISO16281Calculation: 'IncludeExponentAndReductionFactorsInISOTS162812008' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.IncludeExponentAndReductionFactorsInISOTS162812008)
        return constructor.new(_1472.ExponentAndReductionFactorsInISO16281Calculation)(value) if value else None

    @include_exponent_and_reduction_factors_in_isots162812008.setter
    def include_exponent_and_reduction_factors_in_isots162812008(self, value: '_1472.ExponentAndReductionFactorsInISO16281Calculation'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.IncludeExponentAndReductionFactorsInISOTS162812008 = value

    @property
    def lubricant_film_temperature_calculation_pressure_fed_grease_filled_bearings(self) -> 'enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions':
        '''enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions: 'LubricantFilmTemperatureCalculationPressureFedGreaseFilledBearings' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions)(self.wrapped.LubricantFilmTemperatureCalculationPressureFedGreaseFilledBearings) if self.wrapped.LubricantFilmTemperatureCalculationPressureFedGreaseFilledBearings else None

    @lubricant_film_temperature_calculation_pressure_fed_grease_filled_bearings.setter
    def lubricant_film_temperature_calculation_pressure_fed_grease_filled_bearings(self, value: 'enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.LubricantFilmTemperatureCalculationPressureFedGreaseFilledBearings = value

    @property
    def lubricant_film_temperature_calculation_splashed_submerged_bearings(self) -> 'enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions':
        '''enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions: 'LubricantFilmTemperatureCalculationSplashedSubmergedBearings' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions)(self.wrapped.LubricantFilmTemperatureCalculationSplashedSubmergedBearings) if self.wrapped.LubricantFilmTemperatureCalculationSplashedSubmergedBearings else None

    @lubricant_film_temperature_calculation_splashed_submerged_bearings.setter
    def lubricant_film_temperature_calculation_splashed_submerged_bearings(self, value: 'enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FluidFilmTemperatureOptions.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.LubricantFilmTemperatureCalculationSplashedSubmergedBearings = value

    @property
    def ball_bearing_weibull_reliability_slope(self) -> 'float':
        '''float: 'BallBearingWeibullReliabilitySlope' is the original name of this property.'''

        return self.wrapped.BallBearingWeibullReliabilitySlope

    @ball_bearing_weibull_reliability_slope.setter
    def ball_bearing_weibull_reliability_slope(self, value: 'float'):
        self.wrapped.BallBearingWeibullReliabilitySlope = float(value) if value else 0.0

    @property
    def roller_bearing_weibull_reliability_slope(self) -> 'float':
        '''float: 'RollerBearingWeibullReliabilitySlope' is the original name of this property.'''

        return self.wrapped.RollerBearingWeibullReliabilitySlope

    @roller_bearing_weibull_reliability_slope.setter
    def roller_bearing_weibull_reliability_slope(self, value: 'float'):
        self.wrapped.RollerBearingWeibullReliabilitySlope = float(value) if value else 0.0

    @property
    def third_weibull_parameter(self) -> 'float':
        '''float: 'ThirdWeibullParameter' is the original name of this property.'''

        return self.wrapped.ThirdWeibullParameter

    @third_weibull_parameter.setter
    def third_weibull_parameter(self, value: 'float'):
        self.wrapped.ThirdWeibullParameter = float(value) if value else 0.0
