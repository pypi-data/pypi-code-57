'''_1200.py

DetailedBoltDesign
'''


from typing import List

from mastapy.bolts import (
    _1206, _1203, _1198, _1191,
    _1190, _1193
)
from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.python_net import python_net_import
from mastapy._internal.vector_3d import Vector3D
from mastapy import _1

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_DETAILED_BOLT_DESIGN = python_net_import('SMT.MastaAPI.Bolts', 'DetailedBoltDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('DetailedBoltDesign',)


class DetailedBoltDesign(_1.APIBase):
    '''DetailedBoltDesign

    This is a mastapy class.
    '''

    TYPE = _DETAILED_BOLT_DESIGN
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DetailedBoltDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def rolled_before_or_after_heat_treatment(self) -> '_1206.RolledBeforeOrAfterHeatTreament':
        '''RolledBeforeOrAfterHeatTreament: 'RolledBeforeOrAfterHeatTreatment' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.RolledBeforeOrAfterHeatTreatment)
        return constructor.new(_1206.RolledBeforeOrAfterHeatTreament)(value) if value else None

    @rolled_before_or_after_heat_treatment.setter
    def rolled_before_or_after_heat_treatment(self, value: '_1206.RolledBeforeOrAfterHeatTreament'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RolledBeforeOrAfterHeatTreatment = value

    @property
    def number_of_force_transmitting_interfaces(self) -> 'int':
        '''int: 'NumberOfForceTransmittingInterfaces' is the original name of this property.'''

        return self.wrapped.NumberOfForceTransmittingInterfaces

    @number_of_force_transmitting_interfaces.setter
    def number_of_force_transmitting_interfaces(self, value: 'int'):
        self.wrapped.NumberOfForceTransmittingInterfaces = int(value) if value else 0

    @property
    def number_of_torque_transmitting_interfaces(self) -> 'int':
        '''int: 'NumberOfTorqueTransmittingInterfaces' is the original name of this property.'''

        return self.wrapped.NumberOfTorqueTransmittingInterfaces

    @number_of_torque_transmitting_interfaces.setter
    def number_of_torque_transmitting_interfaces(self, value: 'int'):
        self.wrapped.NumberOfTorqueTransmittingInterfaces = int(value) if value else 0

    @property
    def friction_radius(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'FrictionRadius' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.FrictionRadius) if self.wrapped.FrictionRadius else None

    @friction_radius.setter
    def friction_radius(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.FrictionRadius = value

    @property
    def distance_of_bolt_axis_from_central_point(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'DistanceOfBoltAxisFromCentralPoint' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.DistanceOfBoltAxisFromCentralPoint) if self.wrapped.DistanceOfBoltAxisFromCentralPoint else None

    @distance_of_bolt_axis_from_central_point.setter
    def distance_of_bolt_axis_from_central_point(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.DistanceOfBoltAxisFromCentralPoint = value

    @property
    def joint_geometry(self) -> '_1203.JointGeometries':
        '''JointGeometries: 'JointGeometry' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.JointGeometry)
        return constructor.new(_1203.JointGeometries)(value) if value else None

    @joint_geometry.setter
    def joint_geometry(self, value: '_1203.JointGeometries'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.JointGeometry = value

    @property
    def number_of_bolt_sections(self) -> 'int':
        '''int: 'NumberOfBoltSections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfBoltSections

    @property
    def washer_thickness(self) -> 'float':
        '''float: 'WasherThickness' is the original name of this property.'''

        return self.wrapped.WasherThickness

    @washer_thickness.setter
    def washer_thickness(self, value: 'float'):
        self.wrapped.WasherThickness = float(value) if value else 0.0

    @property
    def inside_diameter_of_plane_head_bearing_surface(self) -> 'float':
        '''float: 'InsideDiameterOfPlaneHeadBearingSurface' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InsideDiameterOfPlaneHeadBearingSurface

    @property
    def chamfer_diameter_at_the_clamped_parts(self) -> 'float':
        '''float: 'ChamferDiameterAtTheClampedParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ChamferDiameterAtTheClampedParts

    @property
    def distance_of_the_bolt_axis_from_edge_of_interface(self) -> 'float':
        '''float: 'DistanceOfTheBoltAxisFromEdgeOfInterface' is the original name of this property.'''

        return self.wrapped.DistanceOfTheBoltAxisFromEdgeOfInterface

    @distance_of_the_bolt_axis_from_edge_of_interface.setter
    def distance_of_the_bolt_axis_from_edge_of_interface(self, value: 'float'):
        self.wrapped.DistanceOfTheBoltAxisFromEdgeOfInterface = float(value) if value else 0.0

    @property
    def substitutional_outside_diameter_of_basic_solid_at_interface(self) -> 'float':
        '''float: 'SubstitutionalOutsideDiameterOfBasicSolidAtInterface' is the original name of this property.'''

        return self.wrapped.SubstitutionalOutsideDiameterOfBasicSolidAtInterface

    @substitutional_outside_diameter_of_basic_solid_at_interface.setter
    def substitutional_outside_diameter_of_basic_solid_at_interface(self, value: 'float'):
        self.wrapped.SubstitutionalOutsideDiameterOfBasicSolidAtInterface = float(value) if value else 0.0

    @property
    def substitutional_outside_diameter_of_basic_solid(self) -> 'float':
        '''float: 'SubstitutionalOutsideDiameterOfBasicSolid' is the original name of this property.'''

        return self.wrapped.SubstitutionalOutsideDiameterOfBasicSolid

    @substitutional_outside_diameter_of_basic_solid.setter
    def substitutional_outside_diameter_of_basic_solid(self, value: 'float'):
        self.wrapped.SubstitutionalOutsideDiameterOfBasicSolid = float(value) if value else 0.0

    @property
    def nut_chamfer_diameter(self) -> 'float':
        '''float: 'NutChamferDiameter' is the original name of this property.'''

        return self.wrapped.NutChamferDiameter

    @nut_chamfer_diameter.setter
    def nut_chamfer_diameter(self, value: 'float'):
        self.wrapped.NutChamferDiameter = float(value) if value else 0.0

    @property
    def average_outside_diameter_of_clamped_parts(self) -> 'float':
        '''float: 'AverageOutsideDiameterOfClampedParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AverageOutsideDiameterOfClampedParts

    @property
    def outside_diameter_of_nut(self) -> 'float':
        '''float: 'OutsideDiameterOfNut' is the original name of this property.'''

        return self.wrapped.OutsideDiameterOfNut

    @outside_diameter_of_nut.setter
    def outside_diameter_of_nut(self, value: 'float'):
        self.wrapped.OutsideDiameterOfNut = float(value) if value else 0.0

    @property
    def bearing_area_diameter_at_the_interface(self) -> 'float':
        '''float: 'BearingAreaDiameterAtTheInterface' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BearingAreaDiameterAtTheInterface

    @property
    def substitutional_bending_length_of_bolt(self) -> 'float':
        '''float: 'SubstitutionalBendingLengthOfBolt' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SubstitutionalBendingLengthOfBolt

    @property
    def length_of_free_loaded_thread(self) -> 'float':
        '''float: 'LengthOfFreeLoadedThread' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LengthOfFreeLoadedThread

    @property
    def minimum_plate_thickness(self) -> 'float':
        '''float: 'MinimumPlateThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumPlateThickness

    @property
    def length_of_deformation_sleeve(self) -> 'float':
        '''float: 'LengthOfDeformationSleeve' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LengthOfDeformationSleeve

    @property
    def length_of_deformation_cone(self) -> 'float':
        '''float: 'LengthOfDeformationCone' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LengthOfDeformationCone

    @property
    def measurement_interface_area_perpendicular_to_width(self) -> 'float':
        '''float: 'MeasurementInterfaceAreaPerpendicularToWidth' is the original name of this property.'''

        return self.wrapped.MeasurementInterfaceAreaPerpendicularToWidth

    @measurement_interface_area_perpendicular_to_width.setter
    def measurement_interface_area_perpendicular_to_width(self, value: 'float'):
        self.wrapped.MeasurementInterfaceAreaPerpendicularToWidth = float(value) if value else 0.0

    @property
    def width(self) -> 'float':
        '''float: 'Width' is the original name of this property.'''

        return self.wrapped.Width

    @width.setter
    def width(self, value: 'float'):
        self.wrapped.Width = float(value) if value else 0.0

    @property
    def counter_bore_depth(self) -> 'float':
        '''float: 'CounterBoreDepth' is the original name of this property.'''

        return self.wrapped.CounterBoreDepth

    @counter_bore_depth.setter
    def counter_bore_depth(self, value: 'float'):
        self.wrapped.CounterBoreDepth = float(value) if value else 0.0

    @property
    def limiting_outside_diameter_maximum_diameter_of_deformation_cone(self) -> 'float':
        '''float: 'LimitingOutsideDiameterMaximumDiameterOfDeformationCone' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LimitingOutsideDiameterMaximumDiameterOfDeformationCone

    @property
    def maximum_outside_diameter_of_deformation_cone(self) -> 'float':
        '''float: 'MaximumOutsideDiameterOfDeformationCone' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumOutsideDiameterOfDeformationCone

    @property
    def is_concentrically_clamped(self) -> 'bool':
        '''bool: 'IsConcentricallyClamped' is the original name of this property.'''

        return self.wrapped.IsConcentricallyClamped

    @is_concentrically_clamped.setter
    def is_concentrically_clamped(self, value: 'bool'):
        self.wrapped.IsConcentricallyClamped = bool(value) if value else False

    @property
    def stress_diameter(self) -> 'float':
        '''float: 'StressDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StressDiameter

    @property
    def height(self) -> 'float':
        '''float: 'Height' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Height

    @property
    def clamping_length(self) -> 'float':
        '''float: 'ClampingLength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ClampingLength

    @property
    def minimum_coefficient_of_friction_of_thread(self) -> 'float':
        '''float: 'MinimumCoefficientOfFrictionOfThread' is the original name of this property.'''

        return self.wrapped.MinimumCoefficientOfFrictionOfThread

    @minimum_coefficient_of_friction_of_thread.setter
    def minimum_coefficient_of_friction_of_thread(self, value: 'float'):
        self.wrapped.MinimumCoefficientOfFrictionOfThread = float(value) if value else 0.0

    @property
    def minimum_coefficient_of_friction_of_bearing_area(self) -> 'float':
        '''float: 'MinimumCoefficientOfFrictionOfBearingArea' is the original name of this property.'''

        return self.wrapped.MinimumCoefficientOfFrictionOfBearingArea

    @minimum_coefficient_of_friction_of_bearing_area.setter
    def minimum_coefficient_of_friction_of_bearing_area(self, value: 'float'):
        self.wrapped.MinimumCoefficientOfFrictionOfBearingArea = float(value) if value else 0.0

    @property
    def maximum_coefficient_of_friction_of_thread(self) -> 'float':
        '''float: 'MaximumCoefficientOfFrictionOfThread' is the original name of this property.'''

        return self.wrapped.MaximumCoefficientOfFrictionOfThread

    @maximum_coefficient_of_friction_of_thread.setter
    def maximum_coefficient_of_friction_of_thread(self, value: 'float'):
        self.wrapped.MaximumCoefficientOfFrictionOfThread = float(value) if value else 0.0

    @property
    def maximum_coefficient_of_friction_of_bearing_area(self) -> 'float':
        '''float: 'MaximumCoefficientOfFrictionOfBearingArea' is the original name of this property.'''

        return self.wrapped.MaximumCoefficientOfFrictionOfBearingArea

    @maximum_coefficient_of_friction_of_bearing_area.setter
    def maximum_coefficient_of_friction_of_bearing_area(self, value: 'float'):
        self.wrapped.MaximumCoefficientOfFrictionOfBearingArea = float(value) if value else 0.0

    @property
    def utilization_factor(self) -> 'float':
        '''float: 'UtilizationFactor' is the original name of this property.'''

        return self.wrapped.UtilizationFactor

    @utilization_factor.setter
    def utilization_factor(self, value: 'float'):
        self.wrapped.UtilizationFactor = float(value) if value else 0.0

    @property
    def reduction_coefficient(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ReductionCoefficient' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ReductionCoefficient) if self.wrapped.ReductionCoefficient else None

    @reduction_coefficient.setter
    def reduction_coefficient(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ReductionCoefficient = value

    @property
    def joint_coefficient(self) -> 'float':
        '''float: 'JointCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.JointCoefficient

    @property
    def appropriate_minimum_bolt_diameter(self) -> 'float':
        '''float: 'AppropriateMinimumBoltDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AppropriateMinimumBoltDiameter

    @property
    def appropriate_minimum_cross_sectional_area_for_hollow_bolt(self) -> 'float':
        '''float: 'AppropriateMinimumCrossSectionalAreaForHollowBolt' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AppropriateMinimumCrossSectionalAreaForHollowBolt

    @property
    def stress_cross_sectional_area(self) -> 'float':
        '''float: 'StressCrossSectionalArea' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StressCrossSectionalArea

    @property
    def minimum_bearing_area(self) -> 'float':
        '''float: 'MinimumBearingArea' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumBearingArea

    @property
    def minimum_assembly_bearing_area_of_nut(self) -> 'float':
        '''float: 'MinimumAssemblyBearingAreaOfNut' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumAssemblyBearingAreaOfNut

    @property
    def minimum_assembly_bearing_area_of_head(self) -> 'float':
        '''float: 'MinimumAssemblyBearingAreaOfHead' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumAssemblyBearingAreaOfHead

    @property
    def shearing_area_transverse_loading(self) -> 'float':
        '''float: 'ShearingAreaTransverseLoading' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShearingAreaTransverseLoading

    @property
    def diameter_of_shearing_cross_section(self) -> 'float':
        '''float: 'DiameterOfShearingCrossSection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DiameterOfShearingCrossSection

    @property
    def clamped_parts(self) -> 'List[_1198.ClampedSection]':
        '''List[ClampedSection]: 'ClampedParts' is the original name of this property.'''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ClampedParts, constructor.new(_1198.ClampedSection))
        return value

    @clamped_parts.setter
    def clamped_parts(self, value: 'List[_1198.ClampedSection]'):
        value = value if value else None
        value = conversion.mp_to_pn_objects_in_list(value)
        self.wrapped.ClampedParts = value

    @property
    def substitutional_extension_length_of_engaged_thread(self) -> 'float':
        '''float: 'SubstitutionalExtensionLengthOfEngagedThread' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SubstitutionalExtensionLengthOfEngagedThread

    @property
    def cross_section_of_thread(self) -> 'float':
        '''float: 'CrossSectionOfThread' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CrossSectionOfThread

    @property
    def substitutional_extension_length_of_engaged_nut_thread(self) -> 'float':
        '''float: 'SubstitutionalExtensionLengthOfEngagedNutThread' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SubstitutionalExtensionLengthOfEngagedNutThread

    @property
    def nominal_cross_section(self) -> 'float':
        '''float: 'NominalCrossSection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NominalCrossSection

    @property
    def nominal_cross_section_of_hollow_bolt(self) -> 'float':
        '''float: 'NominalCrossSectionOfHollowBolt' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NominalCrossSectionOfHollowBolt

    @property
    def substitutional_extension_length_of_head(self) -> 'float':
        '''float: 'SubstitutionalExtensionLengthOfHead' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SubstitutionalExtensionLengthOfHead

    @property
    def total_axial_resilience(self) -> 'float':
        '''float: 'TotalAxialResilience' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalAxialResilience

    @property
    def section_radii_of_gyration(self) -> 'List[float]':
        '''List[float]: 'SectionRadiiOfGyration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SectionRadiiOfGyration, float)
        return value

    @property
    def total_bending_resilience(self) -> 'float':
        '''float: 'TotalBendingResilience' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalBendingResilience

    @property
    def length_ratio(self) -> 'float':
        '''float: 'LengthRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LengthRatio

    @property
    def outside_diameter_of_bearing_surface_of_washer(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'OutsideDiameterOfBearingSurfaceOfWasher' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.OutsideDiameterOfBearingSurfaceOfWasher) if self.wrapped.OutsideDiameterOfBearingSurfaceOfWasher else None

    @outside_diameter_of_bearing_surface_of_washer.setter
    def outside_diameter_of_bearing_surface_of_washer(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.OutsideDiameterOfBearingSurfaceOfWasher = value

    @property
    def inside_diameter_of_bearing_surface_of_washer(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'InsideDiameterOfBearingSurfaceOfWasher' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.InsideDiameterOfBearingSurfaceOfWasher) if self.wrapped.InsideDiameterOfBearingSurfaceOfWasher else None

    @inside_diameter_of_bearing_surface_of_washer.setter
    def inside_diameter_of_bearing_surface_of_washer(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.InsideDiameterOfBearingSurfaceOfWasher = value

    @property
    def diameter_ratio(self) -> 'float':
        '''float: 'DiameterRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DiameterRatio

    @property
    def substitutional_moment_of_gyration_of_cone(self) -> 'float':
        '''float: 'SubstitutionalMomentOfGyrationOfCone' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SubstitutionalMomentOfGyrationOfCone

    @property
    def moment_of_gyration_of_cross_section_at_minor_thread_diameter(self) -> 'float':
        '''float: 'MomentOfGyrationOfCrossSectionAtMinorThreadDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MomentOfGyrationOfCrossSectionAtMinorThreadDiameter

    @property
    def substitutional_moment_of_gyration_of_sleeve(self) -> 'float':
        '''float: 'SubstitutionalMomentOfGyrationOfSleeve' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SubstitutionalMomentOfGyrationOfSleeve

    @property
    def substitutional_moment_of_gyration_of_plates(self) -> 'float':
        '''float: 'SubstitutionalMomentOfGyrationOfPlates' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SubstitutionalMomentOfGyrationOfPlates

    @property
    def substitutional_moment_of_gyration_of_plates_minus_bolt_area(self) -> 'float':
        '''float: 'SubstitutionalMomentOfGyrationOfPlatesMinusBoltArea' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SubstitutionalMomentOfGyrationOfPlatesMinusBoltArea

    @property
    def limiting_value_of_interface_dsv(self) -> 'float':
        '''float: 'LimitingValueOfInterfaceDSV' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LimitingValueOfInterfaceDSV

    @property
    def limiting_value_of_interface_esv(self) -> 'float':
        '''float: 'LimitingValueOfInterfaceESV' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LimitingValueOfInterfaceESV

    @property
    def limiting_value_of_interface_esv_with_recessed_tapped_hole(self) -> 'float':
        '''float: 'LimitingValueOfInterfaceESVWithRecessedTappedHole' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LimitingValueOfInterfaceESVWithRecessedTappedHole

    @property
    def elastic_bending_resilience_of_concentric_clamped_parts(self) -> 'float':
        '''float: 'ElasticBendingResilienceOfConcentricClampedParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ElasticBendingResilienceOfConcentricClampedParts

    @property
    def elastic_bending_resilience_of_clamped_parts(self) -> 'float':
        '''float: 'ElasticBendingResilienceOfClampedParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ElasticBendingResilienceOfClampedParts

    @property
    def elastic_resilience_of_clamped_parts(self) -> 'float':
        '''float: 'ElasticResilienceOfClampedParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ElasticResilienceOfClampedParts

    @property
    def elastic_resilience_of_clamped_parts_in_operating_state(self) -> 'float':
        '''float: 'ElasticResilienceOfClampedPartsInOperatingState' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ElasticResilienceOfClampedPartsInOperatingState

    @property
    def consider_this_tapped_thread_bolt_as_a_through_bolted_joint(self) -> 'bool':
        '''bool: 'ConsiderThisTappedThreadBoltAsAThroughBoltedJoint' is the original name of this property.'''

        return self.wrapped.ConsiderThisTappedThreadBoltAsAThroughBoltedJoint

    @consider_this_tapped_thread_bolt_as_a_through_bolted_joint.setter
    def consider_this_tapped_thread_bolt_as_a_through_bolted_joint(self, value: 'bool'):
        self.wrapped.ConsiderThisTappedThreadBoltAsAThroughBoltedJoint = bool(value) if value else False

    @property
    def deformation_cone_angle(self) -> 'float':
        '''float: 'DeformationConeAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeformationConeAngle

    @property
    def elastic_resilience_of_clamped_parts_eccentric_clamping(self) -> 'float':
        '''float: 'ElasticResilienceOfClampedPartsEccentricClamping' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ElasticResilienceOfClampedPartsEccentricClamping

    @property
    def elastic_resilience_of_clamped_parts_eccentric_loading(self) -> 'float':
        '''float: 'ElasticResilienceOfClampedPartsEccentricLoading' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ElasticResilienceOfClampedPartsEccentricLoading

    @property
    def inside_diameter_of_head_bearing_area(self) -> 'float':
        '''float: 'InsideDiameterOfHeadBearingArea' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InsideDiameterOfHeadBearingArea

    @property
    def average_surface_roughness(self) -> 'float':
        '''float: 'AverageSurfaceRoughness' is the original name of this property.'''

        return self.wrapped.AverageSurfaceRoughness

    @average_surface_roughness.setter
    def average_surface_roughness(self, value: 'float'):
        self.wrapped.AverageSurfaceRoughness = float(value) if value else 0.0

    @property
    def minimum_coefficient_of_friction_at_interface(self) -> 'float':
        '''float: 'MinimumCoefficientOfFrictionAtInterface' is the original name of this property.'''

        return self.wrapped.MinimumCoefficientOfFrictionAtInterface

    @minimum_coefficient_of_friction_at_interface.setter
    def minimum_coefficient_of_friction_at_interface(self, value: 'float'):
        self.wrapped.MinimumCoefficientOfFrictionAtInterface = float(value) if value else 0.0

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def diameter_for_the_specified_standard_size(self) -> 'float':
        '''float: 'DiameterForTheSpecifiedStandardSize' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DiameterForTheSpecifiedStandardSize

    @property
    def sealing_area(self) -> 'float':
        '''float: 'SealingArea' is the original name of this property.'''

        return self.wrapped.SealingArea

    @sealing_area.setter
    def sealing_area(self, value: 'float'):
        self.wrapped.SealingArea = float(value) if value else 0.0

    @property
    def edit_bolt_geometry(self) -> 'str':
        '''str: 'EditBoltGeometry' is the original name of this property.'''

        return self.wrapped.EditBoltGeometry.SelectedItemName

    @edit_bolt_geometry.setter
    def edit_bolt_geometry(self, value: 'str'):
        self.wrapped.EditBoltGeometry.SetSelectedItem(str(value) if value else None)

    @property
    def edit_bolt_material(self) -> 'str':
        '''str: 'EditBoltMaterial' is the original name of this property.'''

        return self.wrapped.EditBoltMaterial.SelectedItemName

    @edit_bolt_material.setter
    def edit_bolt_material(self, value: 'str'):
        self.wrapped.EditBoltMaterial.SetSelectedItem(str(value) if value else None)

    @property
    def edit_nut_material(self) -> 'str':
        '''str: 'EditNutMaterial' is the original name of this property.'''

        return self.wrapped.EditNutMaterial.SelectedItemName

    @edit_nut_material.setter
    def edit_nut_material(self, value: 'str'):
        self.wrapped.EditNutMaterial.SetSelectedItem(str(value) if value else None)

    @property
    def edit_tapped_thread_material(self) -> 'str':
        '''str: 'EditTappedThreadMaterial' is the original name of this property.'''

        return self.wrapped.EditTappedThreadMaterial.SelectedItemName

    @edit_tapped_thread_material.setter
    def edit_tapped_thread_material(self, value: 'str'):
        self.wrapped.EditTappedThreadMaterial.SetSelectedItem(str(value) if value else None)

    @property
    def bolt_geometry(self) -> '_1191.BoltGeometry':
        '''BoltGeometry: 'BoltGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1191.BoltGeometry)(self.wrapped.BoltGeometry) if self.wrapped.BoltGeometry else None

    @property
    def orientation(self) -> 'Vector3D':
        '''Vector3D: 'Orientation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.Orientation)
        return value

    @property
    def material_of_nut(self) -> '_1190.BoltedJointMaterial':
        '''BoltedJointMaterial: 'MaterialOfNut' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1190.BoltedJointMaterial)(self.wrapped.MaterialOfNut) if self.wrapped.MaterialOfNut else None

    @property
    def material_of_bolt(self) -> '_1193.BoltMaterial':
        '''BoltMaterial: 'MaterialOfBolt' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1193.BoltMaterial)(self.wrapped.MaterialOfBolt) if self.wrapped.MaterialOfBolt else None

    @property
    def material_of_tapped_thread(self) -> '_1190.BoltedJointMaterial':
        '''BoltedJointMaterial: 'MaterialOfTappedThread' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1190.BoltedJointMaterial)(self.wrapped.MaterialOfTappedThread) if self.wrapped.MaterialOfTappedThread else None

    @property
    def clamped_sections(self) -> 'List[_1198.ClampedSection]':
        '''List[ClampedSection]: 'ClampedSections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ClampedSections, constructor.new(_1198.ClampedSection))
        return value
