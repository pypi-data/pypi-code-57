'''_6045.py

LoadCase
'''


from typing import List

from mastapy.system_model.analyses_and_results import (
    _2176, _2171, _2154, _2162,
    _2169, _2170, _2156, _2173,
    _2174, _2175, _2167, _2157,
    _2166, _2165, _2163, _2164,
    _2177, _2172, _2155, _2160,
    _2159, _2158, _2161, _2168,
    _2153, _2180
)
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.bearings.bearing_results.rolling.iso_rating_results import _1718
from mastapy.bearings.bearing_results.rolling import _1586
from mastapy.system_model import _1803, _1800, _1811
from mastapy.gears import _139
from mastapy.system_model.analyses_and_results.static_loads import (
    _6205, _6048, _6166, _6050,
    _6093, _6134, _6140, _6143,
    _6146, _6179, _6189, _6210,
    _6213, _6120, _6156, _6067,
    _6072, _6085, _6181, _6199,
    _6052, _6046, _6047, _6054,
    _6066, _6065, _6071, _6084,
    _6099, _6112, _6116, _6053,
    _6124, _6136, _6148, _6149,
    _6151, _6153, _6155, _6162,
    _6165, _6172, _6176, _6207,
    _6208, _6174, _6075, _6077,
    _6113, _6115, _6049, _6051,
    _6057, _6059, _6060, _6061,
    _6062, _6064, _6078, _6082,
    _6091, _6095, _6096, _6118,
    _6123, _6133, _6135, _6139,
    _6141, _6142, _6144, _6145,
    _6147, _6160, _6178, _6180,
    _6185, _6187, _6188, _6190,
    _6191, _6192, _6209, _6211,
    _6212, _6214, _6158, _6157,
    _6056, _6069, _6068, _6074,
    _6073, _6087, _6086, _6089,
    _6090, _6167, _6173, _6171,
    _6169, _6183, _6182, _6194,
    _6193, _6195, _6196, _6200,
    _6201, _6202, _6088, _6055,
    _6070, _6083, _6138, _6159,
    _6170, _6175, _6058, _6076,
    _6114, _6186, _6063, _6080
)
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3549
from mastapy.system_model.connections_and_sockets.gears import (
    _1860, _1870, _1876, _1879,
    _1880, _1881, _1884, _1888,
    _1890, _1892, _1874, _1862,
    _1866, _1872, _1886, _1864,
    _1868
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1900, _1894, _1896, _1898,
    _1902, _1904
)
from mastapy.system_model.part_model import (
    _1981, _1982, _1985, _1987,
    _1988, _1989, _1992, _1993,
    _1996, _1997, _1980, _1998,
    _2001, _2004, _2005, _2006,
    _2008, _2009, _2010, _2012,
    _2013, _2015, _2017, _2018,
    _2019
)
from mastapy.system_model.part_model.shaft_model import _2022
from mastapy.system_model.part_model.gears import (
    _2060, _2061, _2067, _2068,
    _2052, _2053, _2054, _2055,
    _2056, _2057, _2058, _2059,
    _2062, _2063, _2064, _2065,
    _2066, _2069, _2071, _2073,
    _2074, _2075, _2076, _2077,
    _2078, _2079, _2080, _2081,
    _2082, _2083, _2084, _2085,
    _2086, _2087, _2088, _2089,
    _2090, _2091, _2092, _2093
)
from mastapy.system_model.part_model.couplings import (
    _2122, _2123, _2111, _2113,
    _2114, _2116, _2117, _2118,
    _2119, _2120, _2121, _2124,
    _2132, _2130, _2131, _2133,
    _2134, _2135, _2137, _2138,
    _2139, _2140, _2141, _2143
)
from mastapy.system_model.connections_and_sockets import (
    _1837, _1832, _1833, _1836,
    _1845, _1848, _1852, _1856
)
from mastapy._internal.python_net import python_net_import

_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'LoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadCase',)


class LoadCase(_2180.Context):
    '''LoadCase

    This is a mastapy class.
    '''

    TYPE = _LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def system_deflection(self) -> '_2176.SystemDeflectionAnalysis':
        '''SystemDeflectionAnalysis: 'SystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2176.SystemDeflectionAnalysis)(self.wrapped.SystemDeflection) if self.wrapped.SystemDeflection else None

    @property
    def power_flow(self) -> '_2171.PowerFlowAnalysis':
        '''PowerFlowAnalysis: 'PowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2171.PowerFlowAnalysis)(self.wrapped.PowerFlow) if self.wrapped.PowerFlow else None

    @property
    def advanced_system_deflection(self) -> '_2154.AdvancedSystemDeflectionAnalysis':
        '''AdvancedSystemDeflectionAnalysis: 'AdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2154.AdvancedSystemDeflectionAnalysis)(self.wrapped.AdvancedSystemDeflection) if self.wrapped.AdvancedSystemDeflection else None

    @property
    def gear_whine_analysis(self) -> '_2162.GearWhineAnalysisAnalysis':
        '''GearWhineAnalysisAnalysis: 'GearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2162.GearWhineAnalysisAnalysis)(self.wrapped.GearWhineAnalysis) if self.wrapped.GearWhineAnalysis else None

    @property
    def multibody_dynamics(self) -> '_2169.MultibodyDynamicsAnalysis':
        '''MultibodyDynamicsAnalysis: 'MultibodyDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2169.MultibodyDynamicsAnalysis)(self.wrapped.MultibodyDynamics) if self.wrapped.MultibodyDynamics else None

    @property
    def parametric_study_tool(self) -> '_2170.ParametricStudyToolAnalysis':
        '''ParametricStudyToolAnalysis: 'ParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2170.ParametricStudyToolAnalysis)(self.wrapped.ParametricStudyTool) if self.wrapped.ParametricStudyTool else None

    @property
    def compound_parametric_study_tool(self) -> '_2156.CompoundParametricStudyToolAnalysis':
        '''CompoundParametricStudyToolAnalysis: 'CompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2156.CompoundParametricStudyToolAnalysis)(self.wrapped.CompoundParametricStudyTool) if self.wrapped.CompoundParametricStudyTool else None

    @property
    def steady_state_synchronous_response(self) -> '_2173.SteadyStateSynchronousResponseAnalysis':
        '''SteadyStateSynchronousResponseAnalysis: 'SteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2173.SteadyStateSynchronousResponseAnalysis)(self.wrapped.SteadyStateSynchronousResponse) if self.wrapped.SteadyStateSynchronousResponse else None

    @property
    def steady_state_synchronous_responseata_speed(self) -> '_2174.SteadyStateSynchronousResponseataSpeedAnalysis':
        '''SteadyStateSynchronousResponseataSpeedAnalysis: 'SteadyStateSynchronousResponseataSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2174.SteadyStateSynchronousResponseataSpeedAnalysis)(self.wrapped.SteadyStateSynchronousResponseataSpeed) if self.wrapped.SteadyStateSynchronousResponseataSpeed else None

    @property
    def steady_state_synchronous_responseona_shaft(self) -> '_2175.SteadyStateSynchronousResponseonaShaftAnalysis':
        '''SteadyStateSynchronousResponseonaShaftAnalysis: 'SteadyStateSynchronousResponseonaShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2175.SteadyStateSynchronousResponseonaShaftAnalysis)(self.wrapped.SteadyStateSynchronousResponseonaShaft) if self.wrapped.SteadyStateSynchronousResponseonaShaft else None

    @property
    def modal_analysis(self) -> '_2167.ModalAnalysisAnalysis':
        '''ModalAnalysisAnalysis: 'ModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2167.ModalAnalysisAnalysis)(self.wrapped.ModalAnalysis) if self.wrapped.ModalAnalysis else None

    @property
    def dynamic_analysis(self) -> '_2157.DynamicAnalysisAnalysis':
        '''DynamicAnalysisAnalysis: 'DynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2157.DynamicAnalysisAnalysis)(self.wrapped.DynamicAnalysis) if self.wrapped.DynamicAnalysis else None

    @property
    def modal_analysesat_stiffnesses(self) -> '_2166.ModalAnalysesatStiffnessesAnalysis':
        '''ModalAnalysesatStiffnessesAnalysis: 'ModalAnalysesatStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2166.ModalAnalysesatStiffnessesAnalysis)(self.wrapped.ModalAnalysesatStiffnesses) if self.wrapped.ModalAnalysesatStiffnesses else None

    @property
    def modal_analysesat_speeds(self) -> '_2165.ModalAnalysesatSpeedsAnalysis':
        '''ModalAnalysesatSpeedsAnalysis: 'ModalAnalysesatSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2165.ModalAnalysesatSpeedsAnalysis)(self.wrapped.ModalAnalysesatSpeeds) if self.wrapped.ModalAnalysesatSpeeds else None

    @property
    def modal_analysesata_speed(self) -> '_2163.ModalAnalysesataSpeedAnalysis':
        '''ModalAnalysesataSpeedAnalysis: 'ModalAnalysesataSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2163.ModalAnalysesataSpeedAnalysis)(self.wrapped.ModalAnalysesataSpeed) if self.wrapped.ModalAnalysesataSpeed else None

    @property
    def modal_analysesata_stiffness(self) -> '_2164.ModalAnalysesataStiffnessAnalysis':
        '''ModalAnalysesataStiffnessAnalysis: 'ModalAnalysesataStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2164.ModalAnalysesataStiffnessAnalysis)(self.wrapped.ModalAnalysesataStiffness) if self.wrapped.ModalAnalysesataStiffness else None

    @property
    def torsional_system_deflection(self) -> '_2177.TorsionalSystemDeflectionAnalysis':
        '''TorsionalSystemDeflectionAnalysis: 'TorsionalSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2177.TorsionalSystemDeflectionAnalysis)(self.wrapped.TorsionalSystemDeflection) if self.wrapped.TorsionalSystemDeflection else None

    @property
    def single_mesh_whine_analysis(self) -> '_2172.SingleMeshWhineAnalysisAnalysis':
        '''SingleMeshWhineAnalysisAnalysis: 'SingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2172.SingleMeshWhineAnalysisAnalysis)(self.wrapped.SingleMeshWhineAnalysis) if self.wrapped.SingleMeshWhineAnalysis else None

    @property
    def advanced_system_deflection_sub_analysis(self) -> '_2155.AdvancedSystemDeflectionSubAnalysisAnalysis':
        '''AdvancedSystemDeflectionSubAnalysisAnalysis: 'AdvancedSystemDeflectionSubAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2155.AdvancedSystemDeflectionSubAnalysisAnalysis)(self.wrapped.AdvancedSystemDeflectionSubAnalysis) if self.wrapped.AdvancedSystemDeflectionSubAnalysis else None

    @property
    def dynamic_modelfor_gear_whine(self) -> '_2160.DynamicModelforGearWhineAnalysis':
        '''DynamicModelforGearWhineAnalysis: 'DynamicModelforGearWhine' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2160.DynamicModelforGearWhineAnalysis)(self.wrapped.DynamicModelforGearWhine) if self.wrapped.DynamicModelforGearWhine else None

    @property
    def dynamic_modelforat_speeds(self) -> '_2159.DynamicModelforatSpeedsAnalysis':
        '''DynamicModelforatSpeedsAnalysis: 'DynamicModelforatSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2159.DynamicModelforatSpeedsAnalysis)(self.wrapped.DynamicModelforatSpeeds) if self.wrapped.DynamicModelforatSpeeds else None

    @property
    def dynamic_modelata_stiffness(self) -> '_2158.DynamicModelataStiffnessAnalysis':
        '''DynamicModelataStiffnessAnalysis: 'DynamicModelataStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2158.DynamicModelataStiffnessAnalysis)(self.wrapped.DynamicModelataStiffness) if self.wrapped.DynamicModelataStiffness else None

    @property
    def dynamic_modelfor_steady_state_synchronous_response(self) -> '_2161.DynamicModelforSteadyStateSynchronousResponseAnalysis':
        '''DynamicModelforSteadyStateSynchronousResponseAnalysis: 'DynamicModelforSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2161.DynamicModelforSteadyStateSynchronousResponseAnalysis)(self.wrapped.DynamicModelforSteadyStateSynchronousResponse) if self.wrapped.DynamicModelforSteadyStateSynchronousResponse else None

    @property
    def modal_analysisfor_whine(self) -> '_2168.ModalAnalysisforWhineAnalysis':
        '''ModalAnalysisforWhineAnalysis: 'ModalAnalysisforWhine' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2168.ModalAnalysisforWhineAnalysis)(self.wrapped.ModalAnalysisforWhine) if self.wrapped.ModalAnalysisforWhine else None

    @property
    def include_bearing_centrifugal(self) -> 'bool':
        '''bool: 'IncludeBearingCentrifugal' is the original name of this property.'''

        return self.wrapped.IncludeBearingCentrifugal

    @include_bearing_centrifugal.setter
    def include_bearing_centrifugal(self, value: 'bool'):
        self.wrapped.IncludeBearingCentrifugal = bool(value) if value else False

    @property
    def include_bearing_centrifugal_ring_expansion(self) -> 'bool':
        '''bool: 'IncludeBearingCentrifugalRingExpansion' is the original name of this property.'''

        return self.wrapped.IncludeBearingCentrifugalRingExpansion

    @include_bearing_centrifugal_ring_expansion.setter
    def include_bearing_centrifugal_ring_expansion(self, value: 'bool'):
        self.wrapped.IncludeBearingCentrifugalRingExpansion = bool(value) if value else False

    @property
    def include_planetary_centrifugal(self) -> 'bool':
        '''bool: 'IncludePlanetaryCentrifugal' is the original name of this property.'''

        return self.wrapped.IncludePlanetaryCentrifugal

    @include_planetary_centrifugal.setter
    def include_planetary_centrifugal(self, value: 'bool'):
        self.wrapped.IncludePlanetaryCentrifugal = bool(value) if value else False

    @property
    def include_gravity(self) -> 'bool':
        '''bool: 'IncludeGravity' is the original name of this property.'''

        return self.wrapped.IncludeGravity

    @include_gravity.setter
    def include_gravity(self, value: 'bool'):
        self.wrapped.IncludeGravity = bool(value) if value else False

    @property
    def stress_concentration_method_for_rating(self) -> 'enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod':
        '''enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod: 'StressConcentrationMethodForRating' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.StressConcentrationMethodForRating, value) if self.wrapped.StressConcentrationMethodForRating else None

    @stress_concentration_method_for_rating.setter
    def stress_concentration_method_for_rating(self, value: 'enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.StressConcentrationMethodForRating = value

    @property
    def number_of_strips_for_roller_calculation(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfStripsForRollerCalculation' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfStripsForRollerCalculation) if self.wrapped.NumberOfStripsForRollerCalculation else None

    @number_of_strips_for_roller_calculation.setter
    def number_of_strips_for_roller_calculation(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.NumberOfStripsForRollerCalculation = value

    @property
    def use_default_temperatures(self) -> 'bool':
        '''bool: 'UseDefaultTemperatures' is the original name of this property.'''

        return self.wrapped.UseDefaultTemperatures

    @use_default_temperatures.setter
    def use_default_temperatures(self, value: 'bool'):
        self.wrapped.UseDefaultTemperatures = bool(value) if value else False

    @property
    def include_fitting_effects(self) -> 'bool':
        '''bool: 'IncludeFittingEffects' is the original name of this property.'''

        return self.wrapped.IncludeFittingEffects

    @include_fitting_effects.setter
    def include_fitting_effects(self, value: 'bool'):
        self.wrapped.IncludeFittingEffects = bool(value) if value else False

    @property
    def include_thermal_expansion_effects(self) -> 'bool':
        '''bool: 'IncludeThermalExpansionEffects' is the original name of this property.'''

        return self.wrapped.IncludeThermalExpansionEffects

    @include_thermal_expansion_effects.setter
    def include_thermal_expansion_effects(self, value: 'bool'):
        self.wrapped.IncludeThermalExpansionEffects = bool(value) if value else False

    @property
    def include_ring_ovality(self) -> 'bool':
        '''bool: 'IncludeRingOvality' is the original name of this property.'''

        return self.wrapped.IncludeRingOvality

    @include_ring_ovality.setter
    def include_ring_ovality(self, value: 'bool'):
        self.wrapped.IncludeRingOvality = bool(value) if value else False

    @property
    def ring_ovality_scaling(self) -> 'float':
        '''float: 'RingOvalityScaling' is the original name of this property.'''

        return self.wrapped.RingOvalityScaling

    @ring_ovality_scaling.setter
    def ring_ovality_scaling(self, value: 'float'):
        self.wrapped.RingOvalityScaling = float(value) if value else 0.0

    @property
    def include_gear_blank_elastic_distortion(self) -> 'bool':
        '''bool: 'IncludeGearBlankElasticDistortion' is the original name of this property.'''

        return self.wrapped.IncludeGearBlankElasticDistortion

    @include_gear_blank_elastic_distortion.setter
    def include_gear_blank_elastic_distortion(self, value: 'bool'):
        self.wrapped.IncludeGearBlankElasticDistortion = bool(value) if value else False

    @property
    def include_inner_race_distortion_for_flexible_pin_spindle(self) -> 'bool':
        '''bool: 'IncludeInnerRaceDistortionForFlexiblePinSpindle' is the original name of this property.'''

        return self.wrapped.IncludeInnerRaceDistortionForFlexiblePinSpindle

    @include_inner_race_distortion_for_flexible_pin_spindle.setter
    def include_inner_race_distortion_for_flexible_pin_spindle(self, value: 'bool'):
        self.wrapped.IncludeInnerRaceDistortionForFlexiblePinSpindle = bool(value) if value else False

    @property
    def ball_bearing_contact_calculation(self) -> '_1586.BallBearingContactCalculation':
        '''BallBearingContactCalculation: 'BallBearingContactCalculation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.BallBearingContactCalculation)
        return constructor.new(_1586.BallBearingContactCalculation)(value) if value else None

    @ball_bearing_contact_calculation.setter
    def ball_bearing_contact_calculation(self, value: '_1586.BallBearingContactCalculation'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BallBearingContactCalculation = value

    @property
    def model_bearing_mounting_clearances_automatically(self) -> 'bool':
        '''bool: 'ModelBearingMountingClearancesAutomatically' is the original name of this property.'''

        return self.wrapped.ModelBearingMountingClearancesAutomatically

    @model_bearing_mounting_clearances_automatically.setter
    def model_bearing_mounting_clearances_automatically(self, value: 'bool'):
        self.wrapped.ModelBearingMountingClearancesAutomatically = bool(value) if value else False

    @property
    def maximum_shaft_section_length_to_diameter_ratio(self) -> 'float':
        '''float: 'MaximumShaftSectionLengthToDiameterRatio' is the original name of this property.'''

        return self.wrapped.MaximumShaftSectionLengthToDiameterRatio

    @maximum_shaft_section_length_to_diameter_ratio.setter
    def maximum_shaft_section_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def maximum_shaft_section_cross_sectional_area_ratio(self) -> 'float':
        '''float: 'MaximumShaftSectionCrossSectionalAreaRatio' is the original name of this property.'''

        return self.wrapped.MaximumShaftSectionCrossSectionalAreaRatio

    @maximum_shaft_section_cross_sectional_area_ratio.setter
    def maximum_shaft_section_cross_sectional_area_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionCrossSectionalAreaRatio = float(value) if value else 0.0

    @property
    def maximum_shaft_section_polar_area_moment_of_inertia_ratio(self) -> 'float':
        '''float: 'MaximumShaftSectionPolarAreaMomentOfInertiaRatio' is the original name of this property.'''

        return self.wrapped.MaximumShaftSectionPolarAreaMomentOfInertiaRatio

    @maximum_shaft_section_polar_area_moment_of_inertia_ratio.setter
    def maximum_shaft_section_polar_area_moment_of_inertia_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionPolarAreaMomentOfInertiaRatio = float(value) if value else 0.0

    @property
    def use_single_node_for_spline_rigid_bond_detailed_connection_connections(self) -> 'bool':
        '''bool: 'UseSingleNodeForSplineRigidBondDetailedConnectionConnections' is the original name of this property.'''

        return self.wrapped.UseSingleNodeForSplineRigidBondDetailedConnectionConnections

    @use_single_node_for_spline_rigid_bond_detailed_connection_connections.setter
    def use_single_node_for_spline_rigid_bond_detailed_connection_connections(self, value: 'bool'):
        self.wrapped.UseSingleNodeForSplineRigidBondDetailedConnectionConnections = bool(value) if value else False

    @property
    def spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio(self) -> 'float':
        '''float: 'SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio' is the original name of this property.'''

        return self.wrapped.SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio

    @spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio.setter
    def spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def use_single_node_for_cylindrical_gear_meshes(self) -> 'bool':
        '''bool: 'UseSingleNodeForCylindricalGearMeshes' is the original name of this property.'''

        return self.wrapped.UseSingleNodeForCylindricalGearMeshes

    @use_single_node_for_cylindrical_gear_meshes.setter
    def use_single_node_for_cylindrical_gear_meshes(self, value: 'bool'):
        self.wrapped.UseSingleNodeForCylindricalGearMeshes = bool(value) if value else False

    @property
    def force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes(self) -> 'bool':
        '''bool: 'ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes' is the original name of this property.'''

        return self.wrapped.ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes

    @force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes.setter
    def force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes(self, value: 'bool'):
        self.wrapped.ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes = bool(value) if value else False

    @property
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self) -> 'float':
        '''float: 'GearMeshNodesPerUnitLengthToDiameterRatio' is the original name of this property.'''

        return self.wrapped.GearMeshNodesPerUnitLengthToDiameterRatio

    @gear_mesh_nodes_per_unit_length_to_diameter_ratio.setter
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.GearMeshNodesPerUnitLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def minimum_number_of_gear_mesh_nodes(self) -> 'int':
        '''int: 'MinimumNumberOfGearMeshNodes' is the original name of this property.'''

        return self.wrapped.MinimumNumberOfGearMeshNodes

    @minimum_number_of_gear_mesh_nodes.setter
    def minimum_number_of_gear_mesh_nodes(self, value: 'int'):
        self.wrapped.MinimumNumberOfGearMeshNodes = int(value) if value else 0

    @property
    def peak_load_factor_for_shafts(self) -> 'float':
        '''float: 'PeakLoadFactorForShafts' is the original name of this property.'''

        return self.wrapped.PeakLoadFactorForShafts

    @peak_load_factor_for_shafts.setter
    def peak_load_factor_for_shafts(self, value: 'float'):
        self.wrapped.PeakLoadFactorForShafts = float(value) if value else 0.0

    @property
    def mesh_stiffness_model(self) -> 'enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel':
        '''enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel: 'MeshStiffnessModel' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.MeshStiffnessModel, value) if self.wrapped.MeshStiffnessModel else None

    @mesh_stiffness_model.setter
    def mesh_stiffness_model(self, value: 'enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.MeshStiffnessModel = value

    @property
    def micro_geometry_model_in_system_deflection(self) -> 'overridable.Overridable_MicroGeometryModel':
        '''overridable.Overridable_MicroGeometryModel: 'MicroGeometryModelInSystemDeflection' is the original name of this property.'''

        value = overridable.Overridable_MicroGeometryModel.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.MicroGeometryModelInSystemDeflection, value) if self.wrapped.MicroGeometryModelInSystemDeflection else None

    @micro_geometry_model_in_system_deflection.setter
    def micro_geometry_model_in_system_deflection(self, value: 'overridable.Overridable_MicroGeometryModel.implicit_type()'):
        wrapper_type = overridable.Overridable_MicroGeometryModel.wrapper_type()
        enclosed_type = overridable.Overridable_MicroGeometryModel.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.MicroGeometryModelInSystemDeflection = value

    @property
    def minimum_force_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumForceForBearingToBeConsideredLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumForceForBearingToBeConsideredLoaded) if self.wrapped.MinimumForceForBearingToBeConsideredLoaded else None

    @minimum_force_for_bearing_to_be_considered_loaded.setter
    def minimum_force_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.MinimumForceForBearingToBeConsideredLoaded = value

    @property
    def minimum_moment_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumMomentForBearingToBeConsideredLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumMomentForBearingToBeConsideredLoaded) if self.wrapped.MinimumMomentForBearingToBeConsideredLoaded else None

    @minimum_moment_for_bearing_to_be_considered_loaded.setter
    def minimum_moment_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.MinimumMomentForBearingToBeConsideredLoaded = value

    @property
    def energy_convergence_absolute_tolerance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'EnergyConvergenceAbsoluteTolerance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.EnergyConvergenceAbsoluteTolerance) if self.wrapped.EnergyConvergenceAbsoluteTolerance else None

    @energy_convergence_absolute_tolerance.setter
    def energy_convergence_absolute_tolerance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.EnergyConvergenceAbsoluteTolerance = value

    @property
    def hypoid_gear_wind_up_removal_method_for_misalignments(self) -> '_1800.HypoidWindUpRemovalMethod':
        '''HypoidWindUpRemovalMethod: 'HypoidGearWindUpRemovalMethodForMisalignments' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.HypoidGearWindUpRemovalMethodForMisalignments)
        return constructor.new(_1800.HypoidWindUpRemovalMethod)(value) if value else None

    @hypoid_gear_wind_up_removal_method_for_misalignments.setter
    def hypoid_gear_wind_up_removal_method_for_misalignments(self, value: '_1800.HypoidWindUpRemovalMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HypoidGearWindUpRemovalMethodForMisalignments = value

    @property
    def include_tilt_stiffness_for_bevel_hypoid_gears(self) -> 'bool':
        '''bool: 'IncludeTiltStiffnessForBevelHypoidGears' is the original name of this property.'''

        return self.wrapped.IncludeTiltStiffnessForBevelHypoidGears

    @include_tilt_stiffness_for_bevel_hypoid_gears.setter
    def include_tilt_stiffness_for_bevel_hypoid_gears(self, value: 'bool'):
        self.wrapped.IncludeTiltStiffnessForBevelHypoidGears = bool(value) if value else False

    @property
    def minimum_power_for_gear_mesh_to_be_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumPowerForGearMeshToBeLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumPowerForGearMeshToBeLoaded) if self.wrapped.MinimumPowerForGearMeshToBeLoaded else None

    @minimum_power_for_gear_mesh_to_be_loaded.setter
    def minimum_power_for_gear_mesh_to_be_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.MinimumPowerForGearMeshToBeLoaded = value

    @property
    def minimum_torque_for_gear_mesh_to_be_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumTorqueForGearMeshToBeLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumTorqueForGearMeshToBeLoaded) if self.wrapped.MinimumTorqueForGearMeshToBeLoaded else None

    @minimum_torque_for_gear_mesh_to_be_loaded.setter
    def minimum_torque_for_gear_mesh_to_be_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.MinimumTorqueForGearMeshToBeLoaded = value

    @property
    def tolerance_factor_for_outer_fit(self) -> 'float':
        '''float: 'ToleranceFactorForOuterFit' is the original name of this property.'''

        return self.wrapped.ToleranceFactorForOuterFit

    @tolerance_factor_for_outer_fit.setter
    def tolerance_factor_for_outer_fit(self, value: 'float'):
        self.wrapped.ToleranceFactorForOuterFit = float(value) if value else 0.0

    @property
    def tolerance_factor_for_inner_fit(self) -> 'float':
        '''float: 'ToleranceFactorForInnerFit' is the original name of this property.'''

        return self.wrapped.ToleranceFactorForInnerFit

    @tolerance_factor_for_inner_fit.setter
    def tolerance_factor_for_inner_fit(self, value: 'float'):
        self.wrapped.ToleranceFactorForInnerFit = float(value) if value else 0.0

    @property
    def tolerance_factor_for_outer_support(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForOuterSupport' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForOuterSupport) if self.wrapped.ToleranceFactorForOuterSupport else None

    @tolerance_factor_for_outer_support.setter
    def tolerance_factor_for_outer_support(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ToleranceFactorForOuterSupport = value

    @property
    def tolerance_factor_for_outer_ring(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForOuterRing' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForOuterRing) if self.wrapped.ToleranceFactorForOuterRing else None

    @tolerance_factor_for_outer_ring.setter
    def tolerance_factor_for_outer_ring(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ToleranceFactorForOuterRing = value

    @property
    def tolerance_factor_for_inner_support(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForInnerSupport' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForInnerSupport) if self.wrapped.ToleranceFactorForInnerSupport else None

    @tolerance_factor_for_inner_support.setter
    def tolerance_factor_for_inner_support(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ToleranceFactorForInnerSupport = value

    @property
    def tolerance_factor_for_inner_ring(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForInnerRing' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForInnerRing) if self.wrapped.ToleranceFactorForInnerRing else None

    @tolerance_factor_for_inner_ring.setter
    def tolerance_factor_for_inner_ring(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ToleranceFactorForInnerRing = value

    @property
    def tolerance_factor_for_radial_internal_clearances(self) -> 'float':
        '''float: 'ToleranceFactorForRadialInternalClearances' is the original name of this property.'''

        return self.wrapped.ToleranceFactorForRadialInternalClearances

    @tolerance_factor_for_radial_internal_clearances.setter
    def tolerance_factor_for_radial_internal_clearances(self, value: 'float'):
        self.wrapped.ToleranceFactorForRadialInternalClearances = float(value) if value else 0.0

    @property
    def tolerance_factor_for_axial_internal_clearances(self) -> 'float':
        '''float: 'ToleranceFactorForAxialInternalClearances' is the original name of this property.'''

        return self.wrapped.ToleranceFactorForAxialInternalClearances

    @tolerance_factor_for_axial_internal_clearances.setter
    def tolerance_factor_for_axial_internal_clearances(self, value: 'float'):
        self.wrapped.ToleranceFactorForAxialInternalClearances = float(value) if value else 0.0

    @property
    def relative_tolerance_for_convergence(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RelativeToleranceForConvergence' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RelativeToleranceForConvergence) if self.wrapped.RelativeToleranceForConvergence else None

    @relative_tolerance_for_convergence.setter
    def relative_tolerance_for_convergence(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.RelativeToleranceForConvergence = value

    @property
    def air_density(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AirDensity' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AirDensity) if self.wrapped.AirDensity else None

    @air_density.setter
    def air_density(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.AirDensity = value

    @property
    def speed_of_sound(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SpeedOfSound' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SpeedOfSound) if self.wrapped.SpeedOfSound else None

    @speed_of_sound.setter
    def speed_of_sound(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.SpeedOfSound = value

    @property
    def characteristic_specific_acoustic_impedance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'CharacteristicSpecificAcousticImpedance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.CharacteristicSpecificAcousticImpedance) if self.wrapped.CharacteristicSpecificAcousticImpedance else None

    @characteristic_specific_acoustic_impedance.setter
    def characteristic_specific_acoustic_impedance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.CharacteristicSpecificAcousticImpedance = value

    @property
    def transmission_efficiency_settings(self) -> '_6205.TransmissionEfficiencySettings':
        '''TransmissionEfficiencySettings: 'TransmissionEfficiencySettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6205.TransmissionEfficiencySettings)(self.wrapped.TransmissionEfficiencySettings) if self.wrapped.TransmissionEfficiencySettings else None

    @property
    def additional_acceleration(self) -> '_6048.AdditionalAccelerationOptions':
        '''AdditionalAccelerationOptions: 'AdditionalAcceleration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6048.AdditionalAccelerationOptions)(self.wrapped.AdditionalAcceleration) if self.wrapped.AdditionalAcceleration else None

    @property
    def temperatures(self) -> '_1811.TransmissionTemperatureSet':
        '''TransmissionTemperatureSet: 'Temperatures' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1811.TransmissionTemperatureSet)(self.wrapped.Temperatures) if self.wrapped.Temperatures else None

    @property
    def input_power_load(self) -> '_6166.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'InputPowerLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6166.PowerLoadLoadCase)(self.wrapped.InputPowerLoad) if self.wrapped.InputPowerLoad else None

    @property
    def output_power_load(self) -> '_6166.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'OutputPowerLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6166.PowerLoadLoadCase)(self.wrapped.OutputPowerLoad) if self.wrapped.OutputPowerLoad else None

    @property
    def parametric_study_tool_options(self) -> '_3549.ParametricStudyToolOptions':
        '''ParametricStudyToolOptions: 'ParametricStudyToolOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3549.ParametricStudyToolOptions)(self.wrapped.ParametricStudyToolOptions) if self.wrapped.ParametricStudyToolOptions else None

    @property
    def power_loads(self) -> 'List[_6166.PowerLoadLoadCase]':
        '''List[PowerLoadLoadCase]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6166.PowerLoadLoadCase))
        return value

    def inputs_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1860.AGMAGleasonConicalGearMesh') -> '_6050.AGMAGleasonConicalGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6050.AGMAGleasonConicalGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_cylindrical_gear_mesh(self, design_entity: '_1870.CylindricalGearMesh') -> '_6093.CylindricalGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6093.CylindricalGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_hypoid_gear_mesh(self, design_entity: '_1876.HypoidGearMesh') -> '_6134.HypoidGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6134.HypoidGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1879.KlingelnbergCycloPalloidConicalGearMesh') -> '_6140.KlingelnbergCycloPalloidConicalGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6140.KlingelnbergCycloPalloidConicalGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1880.KlingelnbergCycloPalloidHypoidGearMesh') -> '_6143.KlingelnbergCycloPalloidHypoidGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6143.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1881.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_6146.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6146.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_spiral_bevel_gear_mesh(self, design_entity: '_1884.SpiralBevelGearMesh') -> '_6179.SpiralBevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6179.SpiralBevelGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_straight_bevel_gear_mesh(self, design_entity: '_1888.StraightBevelGearMesh') -> '_6189.StraightBevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6189.StraightBevelGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_worm_gear_mesh(self, design_entity: '_1890.WormGearMesh') -> '_6210.WormGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6210.WormGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_zerol_bevel_gear_mesh(self, design_entity: '_1892.ZerolBevelGearMesh') -> '_6213.ZerolBevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6213.ZerolBevelGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_gear_mesh(self, design_entity: '_1874.GearMesh') -> '_6120.GearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6120.GearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_part_to_part_shear_coupling_connection(self, design_entity: '_1900.PartToPartShearCouplingConnection') -> '_6156.PartToPartShearCouplingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6156.PartToPartShearCouplingConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_clutch_connection(self, design_entity: '_1894.ClutchConnection') -> '_6067.ClutchConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6067.ClutchConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_concept_coupling_connection(self, design_entity: '_1896.ConceptCouplingConnection') -> '_6072.ConceptCouplingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6072.ConceptCouplingConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_coupling_connection(self, design_entity: '_1898.CouplingConnection') -> '_6085.CouplingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6085.CouplingConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_spring_damper_connection(self, design_entity: '_1902.SpringDamperConnection') -> '_6181.SpringDamperConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6181.SpringDamperConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_torque_converter_connection(self, design_entity: '_1904.TorqueConverterConnection') -> '_6199.TorqueConverterConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6199.TorqueConverterConnectionLoadCase)(method_result) if method_result else None

    def analysis_of(self, analysis_type: '_6052.AnalysisType') -> '_2153.SingleAnalysis':
        ''' 'AnalysisOf' is the original name of this method.

        Args:
            analysis_type (mastapy.system_model.analyses_and_results.static_loads.AnalysisType)

        Returns:
            mastapy.system_model.analyses_and_results.SingleAnalysis
        '''

        analysis_type = conversion.mp_to_pn_enum(analysis_type)
        method_result = self.wrapped.AnalysisOf(analysis_type)
        return constructor.new(_2153.SingleAnalysis)(method_result) if method_result else None

    def delete(self):
        ''' 'Delete' is the original name of this method.'''

        self.wrapped.Delete()

    def inputs_for_abstract_assembly(self, design_entity: '_1981.AbstractAssembly') -> '_6046.AbstractAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6046.AbstractAssemblyLoadCase)(method_result) if method_result else None

    def inputs_for_abstract_shaft_or_housing(self, design_entity: '_1982.AbstractShaftOrHousing') -> '_6047.AbstractShaftOrHousingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6047.AbstractShaftOrHousingLoadCase)(method_result) if method_result else None

    def inputs_for_bearing(self, design_entity: '_1985.Bearing') -> '_6054.BearingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6054.BearingLoadCase)(method_result) if method_result else None

    def inputs_for_bolt(self, design_entity: '_1987.Bolt') -> '_6066.BoltLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6066.BoltLoadCase)(method_result) if method_result else None

    def inputs_for_bolted_joint(self, design_entity: '_1988.BoltedJoint') -> '_6065.BoltedJointLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6065.BoltedJointLoadCase)(method_result) if method_result else None

    def inputs_for_component(self, design_entity: '_1989.Component') -> '_6071.ComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6071.ComponentLoadCase)(method_result) if method_result else None

    def inputs_for_connector(self, design_entity: '_1992.Connector') -> '_6084.ConnectorLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6084.ConnectorLoadCase)(method_result) if method_result else None

    def inputs_for_datum(self, design_entity: '_1993.Datum') -> '_6099.DatumLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6099.DatumLoadCase)(method_result) if method_result else None

    def inputs_for_external_cad_model(self, design_entity: '_1996.ExternalCADModel') -> '_6112.ExternalCADModelLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6112.ExternalCADModelLoadCase)(method_result) if method_result else None

    def inputs_for_flexible_pin_assembly(self, design_entity: '_1997.FlexiblePinAssembly') -> '_6116.FlexiblePinAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6116.FlexiblePinAssemblyLoadCase)(method_result) if method_result else None

    def inputs_for_assembly(self, design_entity: '_1980.Assembly') -> '_6053.AssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6053.AssemblyLoadCase)(method_result) if method_result else None

    def inputs_for_guide_dxf_model(self, design_entity: '_1998.GuideDxfModel') -> '_6124.GuideDxfModelLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6124.GuideDxfModelLoadCase)(method_result) if method_result else None

    def inputs_for_imported_fe_component(self, design_entity: '_2001.ImportedFEComponent') -> '_6136.ImportedFEComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6136.ImportedFEComponentLoadCase)(method_result) if method_result else None

    def inputs_for_mass_disc(self, design_entity: '_2004.MassDisc') -> '_6148.MassDiscLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6148.MassDiscLoadCase)(method_result) if method_result else None

    def inputs_for_measurement_component(self, design_entity: '_2005.MeasurementComponent') -> '_6149.MeasurementComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6149.MeasurementComponentLoadCase)(method_result) if method_result else None

    def inputs_for_mountable_component(self, design_entity: '_2006.MountableComponent') -> '_6151.MountableComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6151.MountableComponentLoadCase)(method_result) if method_result else None

    def inputs_for_oil_seal(self, design_entity: '_2008.OilSeal') -> '_6153.OilSealLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6153.OilSealLoadCase)(method_result) if method_result else None

    def inputs_for_part(self, design_entity: '_2009.Part') -> '_6155.PartLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6155.PartLoadCase)(method_result) if method_result else None

    def inputs_for_planet_carrier(self, design_entity: '_2010.PlanetCarrier') -> '_6162.PlanetCarrierLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6162.PlanetCarrierLoadCase)(method_result) if method_result else None

    def inputs_for_point_load(self, design_entity: '_2012.PointLoad') -> '_6165.PointLoadLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6165.PointLoadLoadCase)(method_result) if method_result else None

    def inputs_for_power_load(self, design_entity: '_2013.PowerLoad') -> '_6166.PowerLoadLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6166.PowerLoadLoadCase)(method_result) if method_result else None

    def inputs_for_root_assembly(self, design_entity: '_2015.RootAssembly') -> '_6172.RootAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6172.RootAssemblyLoadCase)(method_result) if method_result else None

    def inputs_for_specialised_assembly(self, design_entity: '_2017.SpecialisedAssembly') -> '_6176.SpecialisedAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6176.SpecialisedAssemblyLoadCase)(method_result) if method_result else None

    def inputs_for_unbalanced_mass(self, design_entity: '_2018.UnbalancedMass') -> '_6207.UnbalancedMassLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6207.UnbalancedMassLoadCase)(method_result) if method_result else None

    def inputs_for_virtual_component(self, design_entity: '_2019.VirtualComponent') -> '_6208.VirtualComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6208.VirtualComponentLoadCase)(method_result) if method_result else None

    def inputs_for_shaft(self, design_entity: '_2022.Shaft') -> '_6174.ShaftLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6174.ShaftLoadCase)(method_result) if method_result else None

    def inputs_for_concept_gear(self, design_entity: '_2060.ConceptGear') -> '_6075.ConceptGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6075.ConceptGearLoadCase)(method_result) if method_result else None

    def inputs_for_concept_gear_set(self, design_entity: '_2061.ConceptGearSet') -> '_6077.ConceptGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6077.ConceptGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_face_gear(self, design_entity: '_2067.FaceGear') -> '_6113.FaceGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6113.FaceGearLoadCase)(method_result) if method_result else None

    def inputs_for_face_gear_set(self, design_entity: '_2068.FaceGearSet') -> '_6115.FaceGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6115.FaceGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_agma_gleason_conical_gear(self, design_entity: '_2052.AGMAGleasonConicalGear') -> '_6049.AGMAGleasonConicalGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6049.AGMAGleasonConicalGearLoadCase)(method_result) if method_result else None

    def inputs_for_agma_gleason_conical_gear_set(self, design_entity: '_2053.AGMAGleasonConicalGearSet') -> '_6051.AGMAGleasonConicalGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6051.AGMAGleasonConicalGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_bevel_differential_gear(self, design_entity: '_2054.BevelDifferentialGear') -> '_6057.BevelDifferentialGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6057.BevelDifferentialGearLoadCase)(method_result) if method_result else None

    def inputs_for_bevel_differential_gear_set(self, design_entity: '_2055.BevelDifferentialGearSet') -> '_6059.BevelDifferentialGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6059.BevelDifferentialGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_bevel_differential_planet_gear(self, design_entity: '_2056.BevelDifferentialPlanetGear') -> '_6060.BevelDifferentialPlanetGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6060.BevelDifferentialPlanetGearLoadCase)(method_result) if method_result else None

    def inputs_for_bevel_differential_sun_gear(self, design_entity: '_2057.BevelDifferentialSunGear') -> '_6061.BevelDifferentialSunGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6061.BevelDifferentialSunGearLoadCase)(method_result) if method_result else None

    def inputs_for_bevel_gear(self, design_entity: '_2058.BevelGear') -> '_6062.BevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6062.BevelGearLoadCase)(method_result) if method_result else None

    def inputs_for_bevel_gear_set(self, design_entity: '_2059.BevelGearSet') -> '_6064.BevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6064.BevelGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_conical_gear(self, design_entity: '_2062.ConicalGear') -> '_6078.ConicalGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6078.ConicalGearLoadCase)(method_result) if method_result else None

    def inputs_for_conical_gear_set(self, design_entity: '_2063.ConicalGearSet') -> '_6082.ConicalGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6082.ConicalGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_cylindrical_gear(self, design_entity: '_2064.CylindricalGear') -> '_6091.CylindricalGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6091.CylindricalGearLoadCase)(method_result) if method_result else None

    def inputs_for_cylindrical_gear_set(self, design_entity: '_2065.CylindricalGearSet') -> '_6095.CylindricalGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6095.CylindricalGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_cylindrical_planet_gear(self, design_entity: '_2066.CylindricalPlanetGear') -> '_6096.CylindricalPlanetGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6096.CylindricalPlanetGearLoadCase)(method_result) if method_result else None

    def inputs_for_gear(self, design_entity: '_2069.Gear') -> '_6118.GearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6118.GearLoadCase)(method_result) if method_result else None

    def inputs_for_gear_set(self, design_entity: '_2071.GearSet') -> '_6123.GearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6123.GearSetLoadCase)(method_result) if method_result else None

    def inputs_for_hypoid_gear(self, design_entity: '_2073.HypoidGear') -> '_6133.HypoidGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6133.HypoidGearLoadCase)(method_result) if method_result else None

    def inputs_for_hypoid_gear_set(self, design_entity: '_2074.HypoidGearSet') -> '_6135.HypoidGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6135.HypoidGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2075.KlingelnbergCycloPalloidConicalGear') -> '_6139.KlingelnbergCycloPalloidConicalGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6139.KlingelnbergCycloPalloidConicalGearLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2076.KlingelnbergCycloPalloidConicalGearSet') -> '_6141.KlingelnbergCycloPalloidConicalGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6141.KlingelnbergCycloPalloidConicalGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2077.KlingelnbergCycloPalloidHypoidGear') -> '_6142.KlingelnbergCycloPalloidHypoidGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6142.KlingelnbergCycloPalloidHypoidGearLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2078.KlingelnbergCycloPalloidHypoidGearSet') -> '_6144.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6144.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2079.KlingelnbergCycloPalloidSpiralBevelGear') -> '_6145.KlingelnbergCycloPalloidSpiralBevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6145.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2080.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_6147.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6147.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_planetary_gear_set(self, design_entity: '_2081.PlanetaryGearSet') -> '_6160.PlanetaryGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6160.PlanetaryGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_spiral_bevel_gear(self, design_entity: '_2082.SpiralBevelGear') -> '_6178.SpiralBevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6178.SpiralBevelGearLoadCase)(method_result) if method_result else None

    def inputs_for_spiral_bevel_gear_set(self, design_entity: '_2083.SpiralBevelGearSet') -> '_6180.SpiralBevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6180.SpiralBevelGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_straight_bevel_diff_gear(self, design_entity: '_2084.StraightBevelDiffGear') -> '_6185.StraightBevelDiffGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6185.StraightBevelDiffGearLoadCase)(method_result) if method_result else None

    def inputs_for_straight_bevel_diff_gear_set(self, design_entity: '_2085.StraightBevelDiffGearSet') -> '_6187.StraightBevelDiffGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6187.StraightBevelDiffGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_straight_bevel_gear(self, design_entity: '_2086.StraightBevelGear') -> '_6188.StraightBevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6188.StraightBevelGearLoadCase)(method_result) if method_result else None

    def inputs_for_straight_bevel_gear_set(self, design_entity: '_2087.StraightBevelGearSet') -> '_6190.StraightBevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6190.StraightBevelGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_straight_bevel_planet_gear(self, design_entity: '_2088.StraightBevelPlanetGear') -> '_6191.StraightBevelPlanetGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6191.StraightBevelPlanetGearLoadCase)(method_result) if method_result else None

    def inputs_for_straight_bevel_sun_gear(self, design_entity: '_2089.StraightBevelSunGear') -> '_6192.StraightBevelSunGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6192.StraightBevelSunGearLoadCase)(method_result) if method_result else None

    def inputs_for_worm_gear(self, design_entity: '_2090.WormGear') -> '_6209.WormGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6209.WormGearLoadCase)(method_result) if method_result else None

    def inputs_for_worm_gear_set(self, design_entity: '_2091.WormGearSet') -> '_6211.WormGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6211.WormGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_zerol_bevel_gear(self, design_entity: '_2092.ZerolBevelGear') -> '_6212.ZerolBevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6212.ZerolBevelGearLoadCase)(method_result) if method_result else None

    def inputs_for_zerol_bevel_gear_set(self, design_entity: '_2093.ZerolBevelGearSet') -> '_6214.ZerolBevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6214.ZerolBevelGearSetLoadCase)(method_result) if method_result else None

    def inputs_for_part_to_part_shear_coupling(self, design_entity: '_2122.PartToPartShearCoupling') -> '_6158.PartToPartShearCouplingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6158.PartToPartShearCouplingLoadCase)(method_result) if method_result else None

    def inputs_for_part_to_part_shear_coupling_half(self, design_entity: '_2123.PartToPartShearCouplingHalf') -> '_6157.PartToPartShearCouplingHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6157.PartToPartShearCouplingHalfLoadCase)(method_result) if method_result else None

    def inputs_for_belt_drive(self, design_entity: '_2111.BeltDrive') -> '_6056.BeltDriveLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6056.BeltDriveLoadCase)(method_result) if method_result else None

    def inputs_for_clutch(self, design_entity: '_2113.Clutch') -> '_6069.ClutchLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6069.ClutchLoadCase)(method_result) if method_result else None

    def inputs_for_clutch_half(self, design_entity: '_2114.ClutchHalf') -> '_6068.ClutchHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6068.ClutchHalfLoadCase)(method_result) if method_result else None

    def inputs_for_concept_coupling(self, design_entity: '_2116.ConceptCoupling') -> '_6074.ConceptCouplingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6074.ConceptCouplingLoadCase)(method_result) if method_result else None

    def inputs_for_concept_coupling_half(self, design_entity: '_2117.ConceptCouplingHalf') -> '_6073.ConceptCouplingHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6073.ConceptCouplingHalfLoadCase)(method_result) if method_result else None

    def inputs_for_coupling(self, design_entity: '_2118.Coupling') -> '_6087.CouplingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6087.CouplingLoadCase)(method_result) if method_result else None

    def inputs_for_coupling_half(self, design_entity: '_2119.CouplingHalf') -> '_6086.CouplingHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6086.CouplingHalfLoadCase)(method_result) if method_result else None

    def inputs_for_cvt(self, design_entity: '_2120.CVT') -> '_6089.CVTLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6089.CVTLoadCase)(method_result) if method_result else None

    def inputs_for_cvt_pulley(self, design_entity: '_2121.CVTPulley') -> '_6090.CVTPulleyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6090.CVTPulleyLoadCase)(method_result) if method_result else None

    def inputs_for_pulley(self, design_entity: '_2124.Pulley') -> '_6167.PulleyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6167.PulleyLoadCase)(method_result) if method_result else None

    def inputs_for_shaft_hub_connection(self, design_entity: '_2132.ShaftHubConnection') -> '_6173.ShaftHubConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6173.ShaftHubConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_rolling_ring(self, design_entity: '_2130.RollingRing') -> '_6171.RollingRingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6171.RollingRingLoadCase)(method_result) if method_result else None

    def inputs_for_rolling_ring_assembly(self, design_entity: '_2131.RollingRingAssembly') -> '_6169.RollingRingAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6169.RollingRingAssemblyLoadCase)(method_result) if method_result else None

    def inputs_for_spring_damper(self, design_entity: '_2133.SpringDamper') -> '_6183.SpringDamperLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6183.SpringDamperLoadCase)(method_result) if method_result else None

    def inputs_for_spring_damper_half(self, design_entity: '_2134.SpringDamperHalf') -> '_6182.SpringDamperHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6182.SpringDamperHalfLoadCase)(method_result) if method_result else None

    def inputs_for_synchroniser(self, design_entity: '_2135.Synchroniser') -> '_6194.SynchroniserLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6194.SynchroniserLoadCase)(method_result) if method_result else None

    def inputs_for_synchroniser_half(self, design_entity: '_2137.SynchroniserHalf') -> '_6193.SynchroniserHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6193.SynchroniserHalfLoadCase)(method_result) if method_result else None

    def inputs_for_synchroniser_part(self, design_entity: '_2138.SynchroniserPart') -> '_6195.SynchroniserPartLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6195.SynchroniserPartLoadCase)(method_result) if method_result else None

    def inputs_for_synchroniser_sleeve(self, design_entity: '_2139.SynchroniserSleeve') -> '_6196.SynchroniserSleeveLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6196.SynchroniserSleeveLoadCase)(method_result) if method_result else None

    def inputs_for_torque_converter(self, design_entity: '_2140.TorqueConverter') -> '_6200.TorqueConverterLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6200.TorqueConverterLoadCase)(method_result) if method_result else None

    def inputs_for_torque_converter_pump(self, design_entity: '_2141.TorqueConverterPump') -> '_6201.TorqueConverterPumpLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6201.TorqueConverterPumpLoadCase)(method_result) if method_result else None

    def inputs_for_torque_converter_turbine(self, design_entity: '_2143.TorqueConverterTurbine') -> '_6202.TorqueConverterTurbineLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6202.TorqueConverterTurbineLoadCase)(method_result) if method_result else None

    def inputs_for_cvt_belt_connection(self, design_entity: '_1837.CVTBeltConnection') -> '_6088.CVTBeltConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6088.CVTBeltConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_belt_connection(self, design_entity: '_1832.BeltConnection') -> '_6055.BeltConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6055.BeltConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_coaxial_connection(self, design_entity: '_1833.CoaxialConnection') -> '_6070.CoaxialConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6070.CoaxialConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_connection(self, design_entity: '_1836.Connection') -> '_6083.ConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6083.ConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_inter_mountable_component_connection(self, design_entity: '_1845.InterMountableComponentConnection') -> '_6138.InterMountableComponentConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6138.InterMountableComponentConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_planetary_connection(self, design_entity: '_1848.PlanetaryConnection') -> '_6159.PlanetaryConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6159.PlanetaryConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_rolling_ring_connection(self, design_entity: '_1852.RollingRingConnection') -> '_6170.RollingRingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6170.RollingRingConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_shaft_to_mountable_component_connection(self, design_entity: '_1856.ShaftToMountableComponentConnection') -> '_6175.ShaftToMountableComponentConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6175.ShaftToMountableComponentConnectionLoadCase)(method_result) if method_result else None

    def inputs_for_bevel_differential_gear_mesh(self, design_entity: '_1862.BevelDifferentialGearMesh') -> '_6058.BevelDifferentialGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6058.BevelDifferentialGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_concept_gear_mesh(self, design_entity: '_1866.ConceptGearMesh') -> '_6076.ConceptGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6076.ConceptGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_face_gear_mesh(self, design_entity: '_1872.FaceGearMesh') -> '_6114.FaceGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6114.FaceGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1886.StraightBevelDiffGearMesh') -> '_6186.StraightBevelDiffGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6186.StraightBevelDiffGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_bevel_gear_mesh(self, design_entity: '_1864.BevelGearMesh') -> '_6063.BevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6063.BevelGearMeshLoadCase)(method_result) if method_result else None

    def inputs_for_conical_gear_mesh(self, design_entity: '_1868.ConicalGearMesh') -> '_6080.ConicalGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6080.ConicalGearMeshLoadCase)(method_result) if method_result else None
