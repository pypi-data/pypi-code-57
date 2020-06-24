'''_2309.py

BearingLoadCase
'''


from mastapy.utility import _1269
from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy.materials.efficiency import _278
from mastapy.system_model.analyses_and_results.mbd_analyses import _5916
from mastapy.system_model.part_model import _1908
from mastapy.bearings.tolerances import _1495, _1500
from mastapy.bearings.bearing_results.rolling import _1658
from mastapy.system_model.analyses_and_results.static_loads import _2313
from mastapy._internal.python_net import python_net_import

_BEARING_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BearingLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingLoadCase',)


class BearingLoadCase(_2313.ConnectorLoadCase):
    '''BearingLoadCase

    This is a mastapy class.
    '''

    TYPE = _BEARING_LOAD_CASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def include_fitting_effects(self) -> '_1269.LoadCaseOverrideOption':
        '''LoadCaseOverrideOption: 'IncludeFittingEffects' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.IncludeFittingEffects)
        return constructor.new(_1269.LoadCaseOverrideOption)(value) if value else None

    @include_fitting_effects.setter
    def include_fitting_effects(self, value: '_1269.LoadCaseOverrideOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.IncludeFittingEffects = value

    @property
    def include_thermal_expansion_effects(self) -> '_1269.LoadCaseOverrideOption':
        '''LoadCaseOverrideOption: 'IncludeThermalExpansionEffects' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.IncludeThermalExpansionEffects)
        return constructor.new(_1269.LoadCaseOverrideOption)(value) if value else None

    @include_thermal_expansion_effects.setter
    def include_thermal_expansion_effects(self, value: '_1269.LoadCaseOverrideOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.IncludeThermalExpansionEffects = value

    @property
    def include_ring_ovality(self) -> '_1269.LoadCaseOverrideOption':
        '''LoadCaseOverrideOption: 'IncludeRingOvality' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.IncludeRingOvality)
        return constructor.new(_1269.LoadCaseOverrideOption)(value) if value else None

    @include_ring_ovality.setter
    def include_ring_ovality(self, value: '_1269.LoadCaseOverrideOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.IncludeRingOvality = value

    @property
    def inner_node_meaning(self) -> 'str':
        '''str: 'InnerNodeMeaning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InnerNodeMeaning

    @property
    def outer_node_meaning(self) -> 'str':
        '''str: 'OuterNodeMeaning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OuterNodeMeaning

    @property
    def override_design_left_support_detail(self) -> 'bool':
        '''bool: 'OverrideDesignLeftSupportDetail' is the original name of this property.'''

        return self.wrapped.OverrideDesignLeftSupportDetail

    @override_design_left_support_detail.setter
    def override_design_left_support_detail(self, value: 'bool'):
        self.wrapped.OverrideDesignLeftSupportDetail = bool(value) if value else False

    @property
    def override_all_planets_left_support_detail(self) -> 'bool':
        '''bool: 'OverrideAllPlanetsLeftSupportDetail' is the original name of this property.'''

        return self.wrapped.OverrideAllPlanetsLeftSupportDetail

    @override_all_planets_left_support_detail.setter
    def override_all_planets_left_support_detail(self, value: 'bool'):
        self.wrapped.OverrideAllPlanetsLeftSupportDetail = bool(value) if value else False

    @property
    def override_design_right_support_detail(self) -> 'bool':
        '''bool: 'OverrideDesignRightSupportDetail' is the original name of this property.'''

        return self.wrapped.OverrideDesignRightSupportDetail

    @override_design_right_support_detail.setter
    def override_design_right_support_detail(self, value: 'bool'):
        self.wrapped.OverrideDesignRightSupportDetail = bool(value) if value else False

    @property
    def override_all_planets_right_support_detail(self) -> 'bool':
        '''bool: 'OverrideAllPlanetsRightSupportDetail' is the original name of this property.'''

        return self.wrapped.OverrideAllPlanetsRightSupportDetail

    @override_all_planets_right_support_detail.setter
    def override_all_planets_right_support_detail(self, value: 'bool'):
        self.wrapped.OverrideAllPlanetsRightSupportDetail = bool(value) if value else False

    @property
    def use_design_friction_coefficients(self) -> 'bool':
        '''bool: 'UseDesignFrictionCoefficients' is the original name of this property.'''

        return self.wrapped.UseDesignFrictionCoefficients

    @use_design_friction_coefficients.setter
    def use_design_friction_coefficients(self, value: 'bool'):
        self.wrapped.UseDesignFrictionCoefficients = bool(value) if value else False

    @property
    def override_design_inner_support_detail(self) -> 'bool':
        '''bool: 'OverrideDesignInnerSupportDetail' is the original name of this property.'''

        return self.wrapped.OverrideDesignInnerSupportDetail

    @override_design_inner_support_detail.setter
    def override_design_inner_support_detail(self, value: 'bool'):
        self.wrapped.OverrideDesignInnerSupportDetail = bool(value) if value else False

    @property
    def override_all_planets_inner_support_detail(self) -> 'bool':
        '''bool: 'OverrideAllPlanetsInnerSupportDetail' is the original name of this property.'''

        return self.wrapped.OverrideAllPlanetsInnerSupportDetail

    @override_all_planets_inner_support_detail.setter
    def override_all_planets_inner_support_detail(self, value: 'bool'):
        self.wrapped.OverrideAllPlanetsInnerSupportDetail = bool(value) if value else False

    @property
    def override_design_outer_support_detail(self) -> 'bool':
        '''bool: 'OverrideDesignOuterSupportDetail' is the original name of this property.'''

        return self.wrapped.OverrideDesignOuterSupportDetail

    @override_design_outer_support_detail.setter
    def override_design_outer_support_detail(self, value: 'bool'):
        self.wrapped.OverrideDesignOuterSupportDetail = bool(value) if value else False

    @property
    def override_all_planets_outer_support_detail(self) -> 'bool':
        '''bool: 'OverrideAllPlanetsOuterSupportDetail' is the original name of this property.'''

        return self.wrapped.OverrideAllPlanetsOuterSupportDetail

    @override_all_planets_outer_support_detail.setter
    def override_all_planets_outer_support_detail(self, value: 'bool'):
        self.wrapped.OverrideAllPlanetsOuterSupportDetail = bool(value) if value else False

    @property
    def axial_force_preload(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AxialForcePreload' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AxialForcePreload) if self.wrapped.AxialForcePreload else None

    @axial_force_preload.setter
    def axial_force_preload(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.AxialForcePreload = value

    @property
    def preload_spring_initial_compression(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'PreloadSpringInitialCompression' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.PreloadSpringInitialCompression) if self.wrapped.PreloadSpringInitialCompression else None

    @preload_spring_initial_compression.setter
    def preload_spring_initial_compression(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.PreloadSpringInitialCompression = value

    @property
    def contact_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ContactAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ContactAngle) if self.wrapped.ContactAngle else None

    @contact_angle.setter
    def contact_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ContactAngle = value

    @property
    def axial_displacement_preload(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AxialDisplacementPreload' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AxialDisplacementPreload) if self.wrapped.AxialDisplacementPreload else None

    @axial_displacement_preload.setter
    def axial_displacement_preload(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.AxialDisplacementPreload = value

    @property
    def axial_internal_clearance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AxialInternalClearance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AxialInternalClearance) if self.wrapped.AxialInternalClearance else None

    @axial_internal_clearance.setter
    def axial_internal_clearance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.AxialInternalClearance = value

    @property
    def radial_internal_clearance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RadialInternalClearance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RadialInternalClearance) if self.wrapped.RadialInternalClearance else None

    @radial_internal_clearance.setter
    def radial_internal_clearance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.RadialInternalClearance = value

    @property
    def coefficient_of_friction(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'CoefficientOfFriction' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.CoefficientOfFriction) if self.wrapped.CoefficientOfFriction else None

    @coefficient_of_friction.setter
    def coefficient_of_friction(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.CoefficientOfFriction = value

    @property
    def efficiency_rating_method(self) -> 'overridable.Overridable_EfficiencyRatingMethod':
        '''overridable.Overridable_EfficiencyRatingMethod: 'EfficiencyRatingMethod' is the original name of this property.'''

        return constructor.new(overridable.Overridable_EfficiencyRatingMethod)(self.wrapped.EfficiencyRatingMethod) if self.wrapped.EfficiencyRatingMethod else None

    @efficiency_rating_method.setter
    def efficiency_rating_method(self, value: 'overridable.Overridable_EfficiencyRatingMethod.implicit_type()'):
        wrapper_type = overridable.Overridable_EfficiencyRatingMethod.TYPE
        enclosed_type = overridable.Overridable_EfficiencyRatingMethod.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.EfficiencyRatingMethod = value

    @property
    def element_temperature(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ElementTemperature' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ElementTemperature) if self.wrapped.ElementTemperature else None

    @element_temperature.setter
    def element_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ElementTemperature = value

    @property
    def lubricant_film_temperature(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'LubricantFilmTemperature' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.LubricantFilmTemperature) if self.wrapped.LubricantFilmTemperature else None

    @lubricant_film_temperature.setter
    def lubricant_film_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.LubricantFilmTemperature = value

    @property
    def lubricant_windage_churning_temperature(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'LubricantWindageChurningTemperature' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.LubricantWindageChurningTemperature) if self.wrapped.LubricantWindageChurningTemperature else None

    @lubricant_windage_churning_temperature.setter
    def lubricant_windage_churning_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.LubricantWindageChurningTemperature = value

    @property
    def oil_inlet_temperature(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'OilInletTemperature' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.OilInletTemperature) if self.wrapped.OilInletTemperature else None

    @oil_inlet_temperature.setter
    def oil_inlet_temperature(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.OilInletTemperature = value

    @property
    def first_element_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'FirstElementAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.FirstElementAngle) if self.wrapped.FirstElementAngle else None

    @first_element_angle.setter
    def first_element_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.FirstElementAngle = value

    @property
    def bearing_stiffness_model(self) -> '_5916.BearingStiffnessModel':
        '''BearingStiffnessModel: 'BearingStiffnessModel' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.BearingStiffnessModel)
        return constructor.new(_5916.BearingStiffnessModel)(value) if value else None

    @bearing_stiffness_model.setter
    def bearing_stiffness_model(self, value: '_5916.BearingStiffnessModel'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BearingStiffnessModel = value

    @property
    def bearing_stiffness_model_used_in_analysis(self) -> '_5916.BearingStiffnessModel':
        '''BearingStiffnessModel: 'BearingStiffnessModelUsedInAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.BearingStiffnessModelUsedInAnalysis)
        return constructor.new(_5916.BearingStiffnessModel)(value) if value else None

    @property
    def minimum_force_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumForceForBearingToBeConsideredLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumForceForBearingToBeConsideredLoaded) if self.wrapped.MinimumForceForBearingToBeConsideredLoaded else None

    @minimum_force_for_bearing_to_be_considered_loaded.setter
    def minimum_force_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.MinimumForceForBearingToBeConsideredLoaded = value

    @property
    def minimum_moment_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumMomentForBearingToBeConsideredLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumMomentForBearingToBeConsideredLoaded) if self.wrapped.MinimumMomentForBearingToBeConsideredLoaded else None

    @minimum_moment_for_bearing_to_be_considered_loaded.setter
    def minimum_moment_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.MinimumMomentForBearingToBeConsideredLoaded = value

    @property
    def viscosity_ratio(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ViscosityRatio' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ViscosityRatio) if self.wrapped.ViscosityRatio else None

    @viscosity_ratio.setter
    def viscosity_ratio(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ViscosityRatio = value

    @property
    def ring_ovality_scaling(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RingOvalityScaling' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RingOvalityScaling) if self.wrapped.RingOvalityScaling else None

    @ring_ovality_scaling.setter
    def ring_ovality_scaling(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.RingOvalityScaling = value

    @property
    def bearing_life_modification_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'BearingLifeModificationFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.BearingLifeModificationFactor) if self.wrapped.BearingLifeModificationFactor else None

    @bearing_life_modification_factor.setter
    def bearing_life_modification_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.BearingLifeModificationFactor = value

    @property
    def x_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'XStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.XStiffness) if self.wrapped.XStiffness else None

    @x_stiffness.setter
    def x_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.XStiffness = value

    @property
    def y_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'YStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.YStiffness) if self.wrapped.YStiffness else None

    @y_stiffness.setter
    def y_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.YStiffness = value

    @property
    def model_bearing_mounting_clearances_automatically(self) -> 'overridable.Overridable_bool':
        '''overridable.Overridable_bool: 'ModelBearingMountingClearancesAutomatically' is the original name of this property.'''

        return constructor.new(overridable.Overridable_bool)(self.wrapped.ModelBearingMountingClearancesAutomatically) if self.wrapped.ModelBearingMountingClearancesAutomatically else None

    @model_bearing_mounting_clearances_automatically.setter
    def model_bearing_mounting_clearances_automatically(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.TYPE
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else False)
        self.wrapped.ModelBearingMountingClearancesAutomatically = value

    @property
    def component_design(self) -> '_1908.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1908.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def left_ring_detail(self) -> '_1495.RaceDetail':
        '''RaceDetail: 'LeftRingDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1495.RaceDetail)(self.wrapped.LeftRingDetail) if self.wrapped.LeftRingDetail else None

    @property
    def right_ring_detail(self) -> '_1495.RaceDetail':
        '''RaceDetail: 'RightRingDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1495.RaceDetail)(self.wrapped.RightRingDetail) if self.wrapped.RightRingDetail else None

    @property
    def left_support_detail(self) -> '_1500.SupportDetail':
        '''SupportDetail: 'LeftSupportDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1500.SupportDetail)(self.wrapped.LeftSupportDetail) if self.wrapped.LeftSupportDetail else None

    @property
    def right_support_detail(self) -> '_1500.SupportDetail':
        '''SupportDetail: 'RightSupportDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1500.SupportDetail)(self.wrapped.RightSupportDetail) if self.wrapped.RightSupportDetail else None

    @property
    def inner_ring_detail(self) -> '_1495.RaceDetail':
        '''RaceDetail: 'InnerRingDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1495.RaceDetail)(self.wrapped.InnerRingDetail) if self.wrapped.InnerRingDetail else None

    @property
    def friction_coefficients(self) -> '_1658.RollingBearingFrictionCoefficients':
        '''RollingBearingFrictionCoefficients: 'FrictionCoefficients' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1658.RollingBearingFrictionCoefficients)(self.wrapped.FrictionCoefficients) if self.wrapped.FrictionCoefficients else None

    @property
    def outer_ring_detail(self) -> '_1495.RaceDetail':
        '''RaceDetail: 'OuterRingDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1495.RaceDetail)(self.wrapped.OuterRingDetail) if self.wrapped.OuterRingDetail else None

    @property
    def inner_support_detail(self) -> '_1500.SupportDetail':
        '''SupportDetail: 'InnerSupportDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1500.SupportDetail)(self.wrapped.InnerSupportDetail) if self.wrapped.InnerSupportDetail else None

    @property
    def outer_support_detail(self) -> '_1500.SupportDetail':
        '''SupportDetail: 'OuterSupportDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1500.SupportDetail)(self.wrapped.OuterSupportDetail) if self.wrapped.OuterSupportDetail else None
