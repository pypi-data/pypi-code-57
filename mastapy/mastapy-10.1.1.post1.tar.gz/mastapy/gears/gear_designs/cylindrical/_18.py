'''_18.py

CylindricalGearDesignSettings
'''


from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _733, _1000
from mastapy.gears import _314, _306, _288
from mastapy.utility.units_and_measurements import _1107
from mastapy._internal.implicit import overridable, enum_with_selected_value
from mastapy.gears.micro_geometry import (
    _573, _574, _576, _578,
    _584, _575, _577, _583
)
from mastapy.utility import _80
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_DESIGN_SETTINGS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearDesignSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearDesignSettings',)


class CylindricalGearDesignSettings(_80.PerMachineSettings):
    '''CylindricalGearDesignSettings

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_DESIGN_SETTINGS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearDesignSettings.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def draw_micro_geometry_profile_chart_with_relief_on_horizontal_axis(self) -> 'bool':
        '''bool: 'DrawMicroGeometryProfileChartWithReliefOnHorizontalAxis' is the original name of this property.'''

        return self.wrapped.DrawMicroGeometryProfileChartWithReliefOnHorizontalAxis

    @draw_micro_geometry_profile_chart_with_relief_on_horizontal_axis.setter
    def draw_micro_geometry_profile_chart_with_relief_on_horizontal_axis(self, value: 'bool'):
        self.wrapped.DrawMicroGeometryProfileChartWithReliefOnHorizontalAxis = bool(value) if value else False

    @property
    def draw_micro_geometry_charts_with_face_width_axis_oriented_to_view_through_air(self) -> 'bool':
        '''bool: 'DrawMicroGeometryChartsWithFaceWidthAxisOrientedToViewThroughAir' is the original name of this property.'''

        return self.wrapped.DrawMicroGeometryChartsWithFaceWidthAxisOrientedToViewThroughAir

    @draw_micro_geometry_charts_with_face_width_axis_oriented_to_view_through_air.setter
    def draw_micro_geometry_charts_with_face_width_axis_oriented_to_view_through_air(self, value: 'bool'):
        self.wrapped.DrawMicroGeometryChartsWithFaceWidthAxisOrientedToViewThroughAir = bool(value) if value else False

    @property
    def cylindrical_gear_profile_measurement(self) -> '_733.CylindricalGearProfileMeasurementType':
        '''CylindricalGearProfileMeasurementType: 'CylindricalGearProfileMeasurement' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.CylindricalGearProfileMeasurement)
        return constructor.new(_733.CylindricalGearProfileMeasurementType)(value) if value else None

    @cylindrical_gear_profile_measurement.setter
    def cylindrical_gear_profile_measurement(self, value: '_733.CylindricalGearProfileMeasurementType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CylindricalGearProfileMeasurement = value

    @property
    def agma_quality_grade_type(self) -> '_314.QualityGradeTypes':
        '''QualityGradeTypes: 'AGMAQualityGradeType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.AGMAQualityGradeType)
        return constructor.new(_314.QualityGradeTypes)(value) if value else None

    @agma_quality_grade_type.setter
    def agma_quality_grade_type(self, value: '_314.QualityGradeTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AGMAQualityGradeType = value

    @property
    def tolerance_rounding_system(self) -> '_1107.MeasurementSystem':
        '''MeasurementSystem: 'ToleranceRoundingSystem' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ToleranceRoundingSystem)
        return constructor.new(_1107.MeasurementSystem)(value) if value else None

    @tolerance_rounding_system.setter
    def tolerance_rounding_system(self, value: '_1107.MeasurementSystem'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ToleranceRoundingSystem = value

    @property
    def iso_tolerances_standard(self) -> 'overridable.Overridable_ISOToleranceStandard':
        '''overridable.Overridable_ISOToleranceStandard: 'ISOTolerancesStandard' is the original name of this property.'''

        return constructor.new(overridable.Overridable_ISOToleranceStandard)(self.wrapped.ISOTolerancesStandard) if self.wrapped.ISOTolerancesStandard else None

    @iso_tolerances_standard.setter
    def iso_tolerances_standard(self, value: 'overridable.Overridable_ISOToleranceStandard.implicit_type()'):
        wrapper_type = overridable.Overridable_ISOToleranceStandard.TYPE
        enclosed_type = overridable.Overridable_ISOToleranceStandard.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.ISOTolerancesStandard = value

    @property
    def agma_tolerances_standard(self) -> '_288.AGMAToleranceStandard':
        '''AGMAToleranceStandard: 'AGMATolerancesStandard' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.AGMATolerancesStandard)
        return constructor.new(_288.AGMAToleranceStandard)(value) if value else None

    @agma_tolerances_standard.setter
    def agma_tolerances_standard(self, value: '_288.AGMAToleranceStandard'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AGMATolerancesStandard = value

    @property
    def use_diametral_pitch(self) -> 'bool':
        '''bool: 'UseDiametralPitch' is the original name of this property.'''

        return self.wrapped.UseDiametralPitch

    @use_diametral_pitch.setter
    def use_diametral_pitch(self, value: 'bool'):
        self.wrapped.UseDiametralPitch = bool(value) if value else False

    @property
    def use_same_micro_geometry_on_both_flanks_by_default(self) -> 'bool':
        '''bool: 'UseSameMicroGeometryOnBothFlanksByDefault' is the original name of this property.'''

        return self.wrapped.UseSameMicroGeometryOnBothFlanksByDefault

    @use_same_micro_geometry_on_both_flanks_by_default.setter
    def use_same_micro_geometry_on_both_flanks_by_default(self, value: 'bool'):
        self.wrapped.UseSameMicroGeometryOnBothFlanksByDefault = bool(value) if value else False

    @property
    def micro_geometry_lead_relief_definition(self) -> '_1000.MicroGeometryConvention':
        '''MicroGeometryConvention: 'MicroGeometryLeadReliefDefinition' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MicroGeometryLeadReliefDefinition)
        return constructor.new(_1000.MicroGeometryConvention)(value) if value else None

    @micro_geometry_lead_relief_definition.setter
    def micro_geometry_lead_relief_definition(self, value: '_1000.MicroGeometryConvention'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MicroGeometryLeadReliefDefinition = value

    @property
    def enable_proportion_system_for_tip_alteration_coefficient(self) -> 'bool':
        '''bool: 'EnableProportionSystemForTipAlterationCoefficient' is the original name of this property.'''

        return self.wrapped.EnableProportionSystemForTipAlterationCoefficient

    @enable_proportion_system_for_tip_alteration_coefficient.setter
    def enable_proportion_system_for_tip_alteration_coefficient(self, value: 'bool'):
        self.wrapped.EnableProportionSystemForTipAlterationCoefficient = bool(value) if value else False

    @property
    def centre_tolerance_charts_at_maximum_fullness(self) -> 'bool':
        '''bool: 'CentreToleranceChartsAtMaximumFullness' is the original name of this property.'''

        return self.wrapped.CentreToleranceChartsAtMaximumFullness

    @centre_tolerance_charts_at_maximum_fullness.setter
    def centre_tolerance_charts_at_maximum_fullness(self, value: 'bool'):
        self.wrapped.CentreToleranceChartsAtMaximumFullness = bool(value) if value else False

    @property
    def shift_micro_geometry_lead_and_profile_modification_to_have_zero_maximum(self) -> 'bool':
        '''bool: 'ShiftMicroGeometryLeadAndProfileModificationToHaveZeroMaximum' is the original name of this property.'''

        return self.wrapped.ShiftMicroGeometryLeadAndProfileModificationToHaveZeroMaximum

    @shift_micro_geometry_lead_and_profile_modification_to_have_zero_maximum.setter
    def shift_micro_geometry_lead_and_profile_modification_to_have_zero_maximum(self, value: 'bool'):
        self.wrapped.ShiftMicroGeometryLeadAndProfileModificationToHaveZeroMaximum = bool(value) if value else False

    @property
    def number_of_points_for_2d_micro_geometry_plots(self) -> 'int':
        '''int: 'NumberOfPointsFor2DMicroGeometryPlots' is the original name of this property.'''

        return self.wrapped.NumberOfPointsFor2DMicroGeometryPlots

    @number_of_points_for_2d_micro_geometry_plots.setter
    def number_of_points_for_2d_micro_geometry_plots(self, value: 'int'):
        self.wrapped.NumberOfPointsFor2DMicroGeometryPlots = int(value) if value else 0

    @property
    def default_location_of_evaluation_lower_limit(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit':
        '''enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit: 'DefaultLocationOfEvaluationLowerLimit' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit)(self.wrapped.DefaultLocationOfEvaluationLowerLimit) if self.wrapped.DefaultLocationOfEvaluationLowerLimit else None

    @default_location_of_evaluation_lower_limit.setter
    def default_location_of_evaluation_lower_limit(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.DefaultLocationOfEvaluationLowerLimit = value

    @property
    def default_location_of_evaluation_upper_limit(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit':
        '''enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit: 'DefaultLocationOfEvaluationUpperLimit' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit)(self.wrapped.DefaultLocationOfEvaluationUpperLimit) if self.wrapped.DefaultLocationOfEvaluationUpperLimit else None

    @default_location_of_evaluation_upper_limit.setter
    def default_location_of_evaluation_upper_limit(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.DefaultLocationOfEvaluationUpperLimit = value

    @property
    def default_location_of_tip_relief_evaluation(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation':
        '''enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation: 'DefaultLocationOfTipReliefEvaluation' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation)(self.wrapped.DefaultLocationOfTipReliefEvaluation) if self.wrapped.DefaultLocationOfTipReliefEvaluation else None

    @default_location_of_tip_relief_evaluation.setter
    def default_location_of_tip_relief_evaluation(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.DefaultLocationOfTipReliefEvaluation = value

    @property
    def main_profile_modification_ends_at_the_start_of_tip_relief_by_default(self) -> '_578.MainProfileReliefEndsAtTheStartOfTipReliefOption':
        '''MainProfileReliefEndsAtTheStartOfTipReliefOption: 'MainProfileModificationEndsAtTheStartOfTipReliefByDefault' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MainProfileModificationEndsAtTheStartOfTipReliefByDefault)
        return constructor.new(_578.MainProfileReliefEndsAtTheStartOfTipReliefOption)(value) if value else None

    @main_profile_modification_ends_at_the_start_of_tip_relief_by_default.setter
    def main_profile_modification_ends_at_the_start_of_tip_relief_by_default(self, value: '_578.MainProfileReliefEndsAtTheStartOfTipReliefOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MainProfileModificationEndsAtTheStartOfTipReliefByDefault = value

    @property
    def default_location_of_tip_relief_start(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation':
        '''enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation: 'DefaultLocationOfTipReliefStart' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation)(self.wrapped.DefaultLocationOfTipReliefStart) if self.wrapped.DefaultLocationOfTipReliefStart else None

    @default_location_of_tip_relief_start.setter
    def default_location_of_tip_relief_start(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.DefaultLocationOfTipReliefStart = value

    @property
    def measure_tip_reliefs_from_extrapolated_linear_relief_by_default(self) -> 'bool':
        '''bool: 'MeasureTipReliefsFromExtrapolatedLinearReliefByDefault' is the original name of this property.'''

        return self.wrapped.MeasureTipReliefsFromExtrapolatedLinearReliefByDefault

    @measure_tip_reliefs_from_extrapolated_linear_relief_by_default.setter
    def measure_tip_reliefs_from_extrapolated_linear_relief_by_default(self, value: 'bool'):
        self.wrapped.MeasureTipReliefsFromExtrapolatedLinearReliefByDefault = bool(value) if value else False

    @property
    def parabolic_tip_relief_starts_tangent_to_main_profile_relief_by_default(self) -> '_584.ParabolicTipReliefStartsTangentToMainProfileRelief':
        '''ParabolicTipReliefStartsTangentToMainProfileRelief: 'ParabolicTipReliefStartsTangentToMainProfileReliefByDefault' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ParabolicTipReliefStartsTangentToMainProfileReliefByDefault)
        return constructor.new(_584.ParabolicTipReliefStartsTangentToMainProfileRelief)(value) if value else None

    @parabolic_tip_relief_starts_tangent_to_main_profile_relief_by_default.setter
    def parabolic_tip_relief_starts_tangent_to_main_profile_relief_by_default(self, value: '_584.ParabolicTipReliefStartsTangentToMainProfileRelief'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ParabolicTipReliefStartsTangentToMainProfileReliefByDefault = value

    @property
    def default_location_of_root_relief_evaluation(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation':
        '''enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation: 'DefaultLocationOfRootReliefEvaluation' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation)(self.wrapped.DefaultLocationOfRootReliefEvaluation) if self.wrapped.DefaultLocationOfRootReliefEvaluation else None

    @default_location_of_root_relief_evaluation.setter
    def default_location_of_root_relief_evaluation(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.DefaultLocationOfRootReliefEvaluation = value

    @property
    def main_profile_modification_ends_at_the_start_of_root_relief_by_default(self) -> '_577.MainProfileReliefEndsAtTheStartOfRootReliefOption':
        '''MainProfileReliefEndsAtTheStartOfRootReliefOption: 'MainProfileModificationEndsAtTheStartOfRootReliefByDefault' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MainProfileModificationEndsAtTheStartOfRootReliefByDefault)
        return constructor.new(_577.MainProfileReliefEndsAtTheStartOfRootReliefOption)(value) if value else None

    @main_profile_modification_ends_at_the_start_of_root_relief_by_default.setter
    def main_profile_modification_ends_at_the_start_of_root_relief_by_default(self, value: '_577.MainProfileReliefEndsAtTheStartOfRootReliefOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MainProfileModificationEndsAtTheStartOfRootReliefByDefault = value

    @property
    def default_location_of_root_relief_start(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation':
        '''enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation: 'DefaultLocationOfRootReliefStart' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation)(self.wrapped.DefaultLocationOfRootReliefStart) if self.wrapped.DefaultLocationOfRootReliefStart else None

    @default_location_of_root_relief_start.setter
    def default_location_of_root_relief_start(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.DefaultLocationOfRootReliefStart = value

    @property
    def measure_root_reliefs_from_extrapolated_linear_relief_by_default(self) -> 'bool':
        '''bool: 'MeasureRootReliefsFromExtrapolatedLinearReliefByDefault' is the original name of this property.'''

        return self.wrapped.MeasureRootReliefsFromExtrapolatedLinearReliefByDefault

    @measure_root_reliefs_from_extrapolated_linear_relief_by_default.setter
    def measure_root_reliefs_from_extrapolated_linear_relief_by_default(self, value: 'bool'):
        self.wrapped.MeasureRootReliefsFromExtrapolatedLinearReliefByDefault = bool(value) if value else False

    @property
    def parabolic_root_relief_starts_tangent_to_main_profile_relief_by_default(self) -> '_583.ParabolicRootReliefStartsTangentToMainProfileRelief':
        '''ParabolicRootReliefStartsTangentToMainProfileRelief: 'ParabolicRootReliefStartsTangentToMainProfileReliefByDefault' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ParabolicRootReliefStartsTangentToMainProfileReliefByDefault)
        return constructor.new(_583.ParabolicRootReliefStartsTangentToMainProfileRelief)(value) if value else None

    @parabolic_root_relief_starts_tangent_to_main_profile_relief_by_default.setter
    def parabolic_root_relief_starts_tangent_to_main_profile_relief_by_default(self, value: '_583.ParabolicRootReliefStartsTangentToMainProfileRelief'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ParabolicRootReliefStartsTangentToMainProfileReliefByDefault = value
