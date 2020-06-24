'''_515.py

CylindricalGearRealCutterDesign
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy.scripting import _6504
from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import (
    _525, _526, _527, _528,
    _529, _530, _532
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.cylindrical.cutters import _506, _508
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_REAL_CUTTER_DESIGN = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalGearRealCutterDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearRealCutterDesign',)


class CylindricalGearRealCutterDesign(_508.CylindricalGearAbstractCutterDesign):
    '''CylindricalGearRealCutterDesign

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_REAL_CUTTER_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearRealCutterDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def has_tolerances(self) -> 'bool':
        '''bool: 'HasTolerances' is the original name of this property.'''

        return self.wrapped.HasTolerances

    @has_tolerances.setter
    def has_tolerances(self, value: 'bool'):
        self.wrapped.HasTolerances = bool(value) if value else False

    @property
    def pitch_on_reference_cylinder(self) -> 'float':
        '''float: 'PitchOnReferenceCylinder' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PitchOnReferenceCylinder

    @property
    def normal_base_pitch(self) -> 'float':
        '''float: 'NormalBasePitch' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalBasePitch

    @property
    def normal_pressure_angle_constant_base_pitch(self) -> 'float':
        '''float: 'NormalPressureAngleConstantBasePitch' is the original name of this property.'''

        return self.wrapped.NormalPressureAngleConstantBasePitch

    @normal_pressure_angle_constant_base_pitch.setter
    def normal_pressure_angle_constant_base_pitch(self, value: 'float'):
        self.wrapped.NormalPressureAngleConstantBasePitch = float(value) if value else 0.0

    @property
    def number_of_points_for_reporting_fillet_shape(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfPointsForReportingFilletShape' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfPointsForReportingFilletShape) if self.wrapped.NumberOfPointsForReportingFilletShape else None

    @number_of_points_for_reporting_fillet_shape.setter
    def number_of_points_for_reporting_fillet_shape(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.NumberOfPointsForReportingFilletShape = value

    @property
    def nominal_cutter_drawing(self) -> '_6504.SMTBitmap':
        '''SMTBitmap: 'NominalCutterDrawing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6504.SMTBitmap)(self.wrapped.NominalCutterDrawing) if self.wrapped.NominalCutterDrawing else None

    @property
    def number_of_points_for_reporting_main_blade_shape(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfPointsForReportingMainBladeShape' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfPointsForReportingMainBladeShape) if self.wrapped.NumberOfPointsForReportingMainBladeShape else None

    @number_of_points_for_reporting_main_blade_shape.setter
    def number_of_points_for_reporting_main_blade_shape(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.NumberOfPointsForReportingMainBladeShape = value

    @property
    def specify_custom_blade_shape(self) -> 'bool':
        '''bool: 'SpecifyCustomBladeShape' is the original name of this property.'''

        return self.wrapped.SpecifyCustomBladeShape

    @specify_custom_blade_shape.setter
    def specify_custom_blade_shape(self, value: 'bool'):
        self.wrapped.SpecifyCustomBladeShape = bool(value) if value else False

    @property
    def is_hob(self) -> 'bool':
        '''bool: 'IsHob' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsHob

    @property
    def is_shaper(self) -> 'bool':
        '''bool: 'IsShaper' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsShaper

    @property
    def cutter_and_gear_normal_base_pitch_comparison_tolerance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'CutterAndGearNormalBasePitchComparisonTolerance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.CutterAndGearNormalBasePitchComparisonTolerance) if self.wrapped.CutterAndGearNormalBasePitchComparisonTolerance else None

    @cutter_and_gear_normal_base_pitch_comparison_tolerance.setter
    def cutter_and_gear_normal_base_pitch_comparison_tolerance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.CutterAndGearNormalBasePitchComparisonTolerance = value

    @property
    def nominal_cutter_shape(self) -> '_525.CutterShapeDefinition':
        '''CutterShapeDefinition: 'NominalCutterShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_525.CutterShapeDefinition)(self.wrapped.NominalCutterShape) if self.wrapped.NominalCutterShape else None

    @property
    def nominal_cutter_shape_of_type_cylindrical_gear_formed_wheel_grinder_tangible(self) -> '_526.CylindricalGearFormedWheelGrinderTangible':
        '''CylindricalGearFormedWheelGrinderTangible: 'NominalCutterShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _526.CylindricalGearFormedWheelGrinderTangible.TYPE not in self.wrapped.NominalCutterShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_cutter_shape to CylindricalGearFormedWheelGrinderTangible. Expected: {}.'.format(self.wrapped.NominalCutterShape.__class__.__qualname__))

        return constructor.new(_526.CylindricalGearFormedWheelGrinderTangible)(self.wrapped.NominalCutterShape) if self.wrapped.NominalCutterShape else None

    @property
    def nominal_cutter_shape_of_type_cylindrical_gear_hob_shape(self) -> '_527.CylindricalGearHobShape':
        '''CylindricalGearHobShape: 'NominalCutterShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _527.CylindricalGearHobShape.TYPE not in self.wrapped.NominalCutterShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_cutter_shape to CylindricalGearHobShape. Expected: {}.'.format(self.wrapped.NominalCutterShape.__class__.__qualname__))

        return constructor.new(_527.CylindricalGearHobShape)(self.wrapped.NominalCutterShape) if self.wrapped.NominalCutterShape else None

    @property
    def nominal_cutter_shape_of_type_cylindrical_gear_shaper_tangible(self) -> '_528.CylindricalGearShaperTangible':
        '''CylindricalGearShaperTangible: 'NominalCutterShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _528.CylindricalGearShaperTangible.TYPE not in self.wrapped.NominalCutterShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_cutter_shape to CylindricalGearShaperTangible. Expected: {}.'.format(self.wrapped.NominalCutterShape.__class__.__qualname__))

        return constructor.new(_528.CylindricalGearShaperTangible)(self.wrapped.NominalCutterShape) if self.wrapped.NominalCutterShape else None

    @property
    def nominal_cutter_shape_of_type_cylindrical_gear_shaver_tangible(self) -> '_529.CylindricalGearShaverTangible':
        '''CylindricalGearShaverTangible: 'NominalCutterShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _529.CylindricalGearShaverTangible.TYPE not in self.wrapped.NominalCutterShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_cutter_shape to CylindricalGearShaverTangible. Expected: {}.'.format(self.wrapped.NominalCutterShape.__class__.__qualname__))

        return constructor.new(_529.CylindricalGearShaverTangible)(self.wrapped.NominalCutterShape) if self.wrapped.NominalCutterShape else None

    @property
    def nominal_cutter_shape_of_type_cylindrical_gear_worm_grinder_shape(self) -> '_530.CylindricalGearWormGrinderShape':
        '''CylindricalGearWormGrinderShape: 'NominalCutterShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _530.CylindricalGearWormGrinderShape.TYPE not in self.wrapped.NominalCutterShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_cutter_shape to CylindricalGearWormGrinderShape. Expected: {}.'.format(self.wrapped.NominalCutterShape.__class__.__qualname__))

        return constructor.new(_530.CylindricalGearWormGrinderShape)(self.wrapped.NominalCutterShape) if self.wrapped.NominalCutterShape else None

    @property
    def nominal_cutter_shape_of_type_rack_shape(self) -> '_532.RackShape':
        '''RackShape: 'NominalCutterShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _532.RackShape.TYPE not in self.wrapped.NominalCutterShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_cutter_shape to RackShape. Expected: {}.'.format(self.wrapped.NominalCutterShape.__class__.__qualname__))

        return constructor.new(_532.RackShape)(self.wrapped.NominalCutterShape) if self.wrapped.NominalCutterShape else None

    @property
    def customised_cutting_edge_profile(self) -> '_506.CustomisableEdgeProfile':
        '''CustomisableEdgeProfile: 'CustomisedCuttingEdgeProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_506.CustomisableEdgeProfile)(self.wrapped.CustomisedCuttingEdgeProfile) if self.wrapped.CustomisedCuttingEdgeProfile else None
