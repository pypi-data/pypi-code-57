'''_5985.py

MBDAnalysisOptions
'''


from mastapy._internal.implicit import enum_with_selected_value, list_with_selected_item, overridable
from mastapy.system_model.analyses_and_results.mbd_analyses import (
    _5915, _5961, _5912, _6003,
    _5969, _5970, _5986
)
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _1934
from mastapy.nodal_analysis import _115
from mastapy.system_model.analyses_and_results.mbd_analyses.external_interfaces import _6047
from mastapy.system_model.analyses_and_results.modal_analyses import _5884
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_MBD_ANALYSIS_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'MBDAnalysisOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('MBDAnalysisOptions',)


class MBDAnalysisOptions(_1.APIBase):
    '''MBDAnalysisOptions

    This is a mastapy class.
    '''

    TYPE = _MBD_ANALYSIS_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MBDAnalysisOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def bearing_stiffness_model(self) -> 'enum_with_selected_value.EnumWithSelectedValue_BearingStiffnessModel':
        '''enum_with_selected_value.EnumWithSelectedValue_BearingStiffnessModel: 'BearingStiffnessModel' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_BearingStiffnessModel)(self.wrapped.BearingStiffnessModel) if self.wrapped.BearingStiffnessModel else None

    @bearing_stiffness_model.setter
    def bearing_stiffness_model(self, value: 'enum_with_selected_value.EnumWithSelectedValue_BearingStiffnessModel.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_BearingStiffnessModel.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BearingStiffnessModel.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.BearingStiffnessModel = value

    @property
    def load_case_for_linearised_bearing_stiffness(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'LoadCaseForLinearisedBearingStiffness' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.LoadCaseForLinearisedBearingStiffness) if self.wrapped.LoadCaseForLinearisedBearingStiffness else None

    @load_case_for_linearised_bearing_stiffness.setter
    def load_case_for_linearised_bearing_stiffness(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.LoadCaseForLinearisedBearingStiffness = value

    @property
    def gear_mesh_stiffness_model(self) -> 'enum_with_selected_value.EnumWithSelectedValue_GearMeshStiffnessModel':
        '''enum_with_selected_value.EnumWithSelectedValue_GearMeshStiffnessModel: 'GearMeshStiffnessModel' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_GearMeshStiffnessModel)(self.wrapped.GearMeshStiffnessModel) if self.wrapped.GearMeshStiffnessModel else None

    @gear_mesh_stiffness_model.setter
    def gear_mesh_stiffness_model(self, value: 'enum_with_selected_value.EnumWithSelectedValue_GearMeshStiffnessModel.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_GearMeshStiffnessModel.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_GearMeshStiffnessModel.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.GearMeshStiffnessModel = value

    @property
    def include_gear_backlash(self) -> 'bool':
        '''bool: 'IncludeGearBacklash' is the original name of this property.'''

        return self.wrapped.IncludeGearBacklash

    @include_gear_backlash.setter
    def include_gear_backlash(self, value: 'bool'):
        self.wrapped.IncludeGearBacklash = bool(value) if value else False

    @property
    def include_microgeometry(self) -> 'bool':
        '''bool: 'IncludeMicrogeometry' is the original name of this property.'''

        return self.wrapped.IncludeMicrogeometry

    @include_microgeometry.setter
    def include_microgeometry(self, value: 'bool'):
        self.wrapped.IncludeMicrogeometry = bool(value) if value else False

    @property
    def use_load_sensitive_stiffness(self) -> 'bool':
        '''bool: 'UseLoadSensitiveStiffness' is the original name of this property.'''

        return self.wrapped.UseLoadSensitiveStiffness

    @use_load_sensitive_stiffness.setter
    def use_load_sensitive_stiffness(self, value: 'bool'):
        self.wrapped.UseLoadSensitiveStiffness = bool(value) if value else False

    @property
    def filter_cut_off(self) -> 'float':
        '''float: 'FilterCutOff' is the original name of this property.'''

        return self.wrapped.FilterCutOff

    @filter_cut_off.setter
    def filter_cut_off(self, value: 'float'):
        self.wrapped.FilterCutOff = float(value) if value else 0.0

    @property
    def maximum_frequency_in_signal(self) -> 'float':
        '''float: 'MaximumFrequencyInSignal' is the original name of this property.'''

        return self.wrapped.MaximumFrequencyInSignal

    @maximum_frequency_in_signal.setter
    def maximum_frequency_in_signal(self, value: 'float'):
        self.wrapped.MaximumFrequencyInSignal = float(value) if value else 0.0

    @property
    def maximum_angular_jerk(self) -> 'float':
        '''float: 'MaximumAngularJerk' is the original name of this property.'''

        return self.wrapped.MaximumAngularJerk

    @maximum_angular_jerk.setter
    def maximum_angular_jerk(self, value: 'float'):
        self.wrapped.MaximumAngularJerk = float(value) if value else 0.0

    @property
    def analysis_type(self) -> '_5912.AnalysisTypes':
        '''AnalysisTypes: 'AnalysisType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.AnalysisType)
        return constructor.new(_5912.AnalysisTypes)(value) if value else None

    @analysis_type.setter
    def analysis_type(self, value: '_5912.AnalysisTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AnalysisType = value

    @property
    def load_case_for_component_speed_ratios(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'LoadCaseForComponentSpeedRatios' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.LoadCaseForComponentSpeedRatios) if self.wrapped.LoadCaseForComponentSpeedRatios else None

    @load_case_for_component_speed_ratios.setter
    def load_case_for_component_speed_ratios(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.LoadCaseForComponentSpeedRatios = value

    @property
    def include_shaft_and_housing_flexibilities(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption':
        '''enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption: 'IncludeShaftAndHousingFlexibilities' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption)(self.wrapped.IncludeShaftAndHousingFlexibilities) if self.wrapped.IncludeShaftAndHousingFlexibilities else None

    @include_shaft_and_housing_flexibilities.setter
    def include_shaft_and_housing_flexibilities(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.IncludeShaftAndHousingFlexibilities = value

    @property
    def bearing_rayleigh_damping_beta(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'BearingRayleighDampingBeta' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.BearingRayleighDampingBeta) if self.wrapped.BearingRayleighDampingBeta else None

    @bearing_rayleigh_damping_beta.setter
    def bearing_rayleigh_damping_beta(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.BearingRayleighDampingBeta = value

    @property
    def shaft_and_housing_rayleigh_damping_beta(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ShaftAndHousingRayleighDampingBeta' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ShaftAndHousingRayleighDampingBeta) if self.wrapped.ShaftAndHousingRayleighDampingBeta else None

    @shaft_and_housing_rayleigh_damping_beta.setter
    def shaft_and_housing_rayleigh_damping_beta(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ShaftAndHousingRayleighDampingBeta = value

    @property
    def gear_mesh_rayleigh_damping_beta(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'GearMeshRayleighDampingBeta' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.GearMeshRayleighDampingBeta) if self.wrapped.GearMeshRayleighDampingBeta else None

    @gear_mesh_rayleigh_damping_beta.setter
    def gear_mesh_rayleigh_damping_beta(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.GearMeshRayleighDampingBeta = value

    @property
    def belt_rayleigh_damping_beta(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'BeltRayleighDampingBeta' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.BeltRayleighDampingBeta) if self.wrapped.BeltRayleighDampingBeta else None

    @belt_rayleigh_damping_beta.setter
    def belt_rayleigh_damping_beta(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.BeltRayleighDampingBeta = value

    @property
    def spline_rayleigh_damping_beta(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SplineRayleighDampingBeta' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SplineRayleighDampingBeta) if self.wrapped.SplineRayleighDampingBeta else None

    @spline_rayleigh_damping_beta.setter
    def spline_rayleigh_damping_beta(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.SplineRayleighDampingBeta = value

    @property
    def interference_fit_rayleigh_damping_beta(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'InterferenceFitRayleighDampingBeta' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.InterferenceFitRayleighDampingBeta) if self.wrapped.InterferenceFitRayleighDampingBeta else None

    @interference_fit_rayleigh_damping_beta.setter
    def interference_fit_rayleigh_damping_beta(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.InterferenceFitRayleighDampingBeta = value

    @property
    def create_inertia_adjusted_static_load_cases(self) -> 'bool':
        '''bool: 'CreateInertiaAdjustedStaticLoadCases' is the original name of this property.'''

        return self.wrapped.CreateInertiaAdjustedStaticLoadCases

    @create_inertia_adjusted_static_load_cases.setter
    def create_inertia_adjusted_static_load_cases(self, value: 'bool'):
        self.wrapped.CreateInertiaAdjustedStaticLoadCases = bool(value) if value else False

    @property
    def number_of_static_load_cases(self) -> 'int':
        '''int: 'NumberOfStaticLoadCases' is the original name of this property.'''

        return self.wrapped.NumberOfStaticLoadCases

    @number_of_static_load_cases.setter
    def number_of_static_load_cases(self, value: 'int'):
        self.wrapped.NumberOfStaticLoadCases = int(value) if value else 0

    @property
    def start_time(self) -> 'float':
        '''float: 'StartTime' is the original name of this property.'''

        return self.wrapped.StartTime

    @start_time.setter
    def start_time(self, value: 'float'):
        self.wrapped.StartTime = float(value) if value else 0.0

    @property
    def sample_length(self) -> 'float':
        '''float: 'SampleLength' is the original name of this property.'''

        return self.wrapped.SampleLength

    @sample_length.setter
    def sample_length(self, value: 'float'):
        self.wrapped.SampleLength = float(value) if value else 0.0

    @property
    def method_to_define_period(self) -> '_5969.InertiaAdjustedLoadCasePeriodMethod':
        '''InertiaAdjustedLoadCasePeriodMethod: 'MethodToDefinePeriod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MethodToDefinePeriod)
        return constructor.new(_5969.InertiaAdjustedLoadCasePeriodMethod)(value) if value else None

    @method_to_define_period.setter
    def method_to_define_period(self, value: '_5969.InertiaAdjustedLoadCasePeriodMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MethodToDefinePeriod = value

    @property
    def reference_power_load_to_define_period(self) -> 'list_with_selected_item.ListWithSelectedItem_PowerLoad':
        '''list_with_selected_item.ListWithSelectedItem_PowerLoad: 'ReferencePowerLoadToDefinePeriod' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_PowerLoad)(self.wrapped.ReferencePowerLoadToDefinePeriod) if self.wrapped.ReferencePowerLoadToDefinePeriod else None

    @reference_power_load_to_define_period.setter
    def reference_power_load_to_define_period(self, value: 'list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.ReferencePowerLoadToDefinePeriod = value

    @property
    def power_load_rotation(self) -> 'float':
        '''float: 'PowerLoadRotation' is the original name of this property.'''

        return self.wrapped.PowerLoadRotation

    @power_load_rotation.setter
    def power_load_rotation(self, value: 'float'):
        self.wrapped.PowerLoadRotation = float(value) if value else 0.0

    @property
    def start_at_zero_angle(self) -> 'bool':
        '''bool: 'StartAtZeroAngle' is the original name of this property.'''

        return self.wrapped.StartAtZeroAngle

    @start_at_zero_angle.setter
    def start_at_zero_angle(self, value: 'bool'):
        self.wrapped.StartAtZeroAngle = bool(value) if value else False

    @property
    def static_load_cases_to_create(self) -> '_5970.InertiaAdjustedLoadCaseResultsToCreate':
        '''InertiaAdjustedLoadCaseResultsToCreate: 'StaticLoadCasesToCreate' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.StaticLoadCasesToCreate)
        return constructor.new(_5970.InertiaAdjustedLoadCaseResultsToCreate)(value) if value else None

    @static_load_cases_to_create.setter
    def static_load_cases_to_create(self, value: '_5970.InertiaAdjustedLoadCaseResultsToCreate'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.StaticLoadCasesToCreate = value

    @property
    def use_temperature_model(self) -> 'bool':
        '''bool: 'UseTemperatureModel' is the original name of this property.'''

        return self.wrapped.UseTemperatureModel

    @use_temperature_model.setter
    def use_temperature_model(self, value: 'bool'):
        self.wrapped.UseTemperatureModel = bool(value) if value else False

    @property
    def transient_solver_options(self) -> '_115.TransientSolverOptions':
        '''TransientSolverOptions: 'TransientSolverOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_115.TransientSolverOptions)(self.wrapped.TransientSolverOptions) if self.wrapped.TransientSolverOptions else None

    @property
    def external_interface_options(self) -> '_6047.DynamicExternalInterfaceOptions':
        '''DynamicExternalInterfaceOptions: 'ExternalInterfaceOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6047.DynamicExternalInterfaceOptions)(self.wrapped.ExternalInterfaceOptions) if self.wrapped.ExternalInterfaceOptions else None

    @property
    def run_up_analysis_options(self) -> '_5986.MBDRunUpAnalysisOptions':
        '''MBDRunUpAnalysisOptions: 'RunUpAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5986.MBDRunUpAnalysisOptions)(self.wrapped.RunUpAnalysisOptions) if self.wrapped.RunUpAnalysisOptions else None

    @property
    def frequency_response_options(self) -> '_5884.FrequencyResponseAnalysisOptions':
        '''FrequencyResponseAnalysisOptions: 'FrequencyResponseOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5884.FrequencyResponseAnalysisOptions)(self.wrapped.FrequencyResponseOptions) if self.wrapped.FrequencyResponseOptions else None
