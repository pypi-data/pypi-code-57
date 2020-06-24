'''_1967.py

ShaftHubConnection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable, enum_with_selected_value
from mastapy.system_model.part_model.couplings import (
    _2071, _2074, _2070, _2073,
    _2072
)
from mastapy.detailed_rigid_connectors.splines import (
    _1148, _1133, _1153, _1128,
    _1131, _1138, _1146, _1135,
    _1139
)
from mastapy.scripting import _712
from mastapy._internal.python_net import python_net_import
from mastapy._internal.cast_exception import CastException
from mastapy.detailed_rigid_connectors.interference_fits import _1183
from mastapy.nodal_analysis import _82
from mastapy.system_model.part_model import _1915

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_SHAFT_HUB_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ShaftHubConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnection',)


class ShaftHubConnection(_1915.Connector):
    '''ShaftHubConnection

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def length(self) -> 'float':
        '''float: 'Length' is the original name of this property.'''

        return self.wrapped.Length

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value else 0.0

    @property
    def radial_clearance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RadialClearance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RadialClearance) if self.wrapped.RadialClearance else None

    @radial_clearance.setter
    def radial_clearance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.RadialClearance = value

    @property
    def tilt_clearance(self) -> 'float':
        '''float: 'TiltClearance' is the original name of this property.'''

        return self.wrapped.TiltClearance

    @tilt_clearance.setter
    def tilt_clearance(self, value: 'float'):
        self.wrapped.TiltClearance = float(value) if value else 0.0

    @property
    def torsional_stiffness_shaft_hub_connection(self) -> 'float':
        '''float: 'TorsionalStiffnessShaftHubConnection' is the original name of this property.'''

        return self.wrapped.TorsionalStiffnessShaftHubConnection

    @torsional_stiffness_shaft_hub_connection.setter
    def torsional_stiffness_shaft_hub_connection(self, value: 'float'):
        self.wrapped.TorsionalStiffnessShaftHubConnection = float(value) if value else 0.0

    @property
    def radial_stiffness_shaft_hub_connection(self) -> 'float':
        '''float: 'RadialStiffnessShaftHubConnection' is the original name of this property.'''

        return self.wrapped.RadialStiffnessShaftHubConnection

    @radial_stiffness_shaft_hub_connection.setter
    def radial_stiffness_shaft_hub_connection(self, value: 'float'):
        self.wrapped.RadialStiffnessShaftHubConnection = float(value) if value else 0.0

    @property
    def axial_stiffness_shaft_hub_connection(self) -> 'float':
        '''float: 'AxialStiffnessShaftHubConnection' is the original name of this property.'''

        return self.wrapped.AxialStiffnessShaftHubConnection

    @axial_stiffness_shaft_hub_connection.setter
    def axial_stiffness_shaft_hub_connection(self, value: 'float'):
        self.wrapped.AxialStiffnessShaftHubConnection = float(value) if value else 0.0

    @property
    def additional_tilt_stiffness(self) -> 'float':
        '''float: 'AdditionalTiltStiffness' is the original name of this property.'''

        return self.wrapped.AdditionalTiltStiffness

    @additional_tilt_stiffness.setter
    def additional_tilt_stiffness(self, value: 'float'):
        self.wrapped.AdditionalTiltStiffness = float(value) if value else 0.0

    @property
    def tilt_stiffness_shaft_hub_connection(self) -> 'float':
        '''float: 'TiltStiffnessShaftHubConnection' is the original name of this property.'''

        return self.wrapped.TiltStiffnessShaftHubConnection

    @tilt_stiffness_shaft_hub_connection.setter
    def tilt_stiffness_shaft_hub_connection(self, value: 'float'):
        self.wrapped.TiltStiffnessShaftHubConnection = float(value) if value else 0.0

    @property
    def outer_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'OuterDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.OuterDiameter) if self.wrapped.OuterDiameter else None

    @outer_diameter.setter
    def outer_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.OuterDiameter = value

    @property
    def inner_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'InnerDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.InnerDiameter) if self.wrapped.InnerDiameter else None

    @inner_diameter.setter
    def inner_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.InnerDiameter = value

    @property
    def tilt_stiffness_type(self) -> '_2071.RigidConnectorTiltStiffnessTypes':
        '''RigidConnectorTiltStiffnessTypes: 'TiltStiffnessType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.TiltStiffnessType)
        return constructor.new(_2071.RigidConnectorTiltStiffnessTypes)(value) if value else None

    @tilt_stiffness_type.setter
    def tilt_stiffness_type(self, value: '_2071.RigidConnectorTiltStiffnessTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TiltStiffnessType = value

    @property
    def type_(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RigidConnectorTypes':
        '''enum_with_selected_value.EnumWithSelectedValue_RigidConnectorTypes: 'Type' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_RigidConnectorTypes)(self.wrapped.Type) if self.wrapped.Type else None

    @type_.setter
    def type_(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RigidConnectorTypes.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorTypes.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorTypes.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.Type = value

    @property
    def spline_type(self) -> '_1148.SplineDesignTypes':
        '''SplineDesignTypes: 'SplineType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.SplineType)
        return constructor.new(_1148.SplineDesignTypes)(value) if value else None

    @spline_type.setter
    def spline_type(self, value: '_1148.SplineDesignTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SplineType = value

    @property
    def torsional_twist_preload(self) -> 'float':
        '''float: 'TorsionalTwistPreload' is the original name of this property.'''

        return self.wrapped.TorsionalTwistPreload

    @torsional_twist_preload.setter
    def torsional_twist_preload(self, value: 'float'):
        self.wrapped.TorsionalTwistPreload = float(value) if value else 0.0

    @property
    def axial_preload(self) -> 'float':
        '''float: 'AxialPreload' is the original name of this property.'''

        return self.wrapped.AxialPreload

    @axial_preload.setter
    def axial_preload(self, value: 'float'):
        self.wrapped.AxialPreload = float(value) if value else 0.0

    @property
    def twod_spline_drawing(self) -> '_712.SMTBitmap':
        '''SMTBitmap: 'TwoDSplineDrawing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_712.SMTBitmap)(self.wrapped.TwoDSplineDrawing) if self.wrapped.TwoDSplineDrawing else None

    @property
    def torsional_stiffness_is_calculated(self) -> 'bool':
        '''bool: 'TorsionalStiffnessIsCalculated' is the original name of this property.'''

        return self.wrapped.TorsionalStiffnessIsCalculated

    @torsional_stiffness_is_calculated.setter
    def torsional_stiffness_is_calculated(self, value: 'bool'):
        self.wrapped.TorsionalStiffnessIsCalculated = bool(value) if value else False

    @property
    def inner_half_material(self) -> 'str':
        '''str: 'InnerHalfMaterial' is the original name of this property.'''

        return self.wrapped.InnerHalfMaterial.SelectedItemName

    @inner_half_material.setter
    def inner_half_material(self, value: 'str'):
        self.wrapped.InnerHalfMaterial.SetSelectedItem(str(value) if value else None)

    @property
    def outer_half_material(self) -> 'str':
        '''str: 'OuterHalfMaterial' is the original name of this property.'''

        return self.wrapped.OuterHalfMaterial.SelectedItemName

    @outer_half_material.setter
    def outer_half_material(self, value: 'str'):
        self.wrapped.OuterHalfMaterial.SetSelectedItem(str(value) if value else None)

    @property
    def stiffness_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RigidConnectorStiffnessType':
        '''enum_with_selected_value.EnumWithSelectedValue_RigidConnectorStiffnessType: 'StiffnessType' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_RigidConnectorStiffnessType)(self.wrapped.StiffnessType) if self.wrapped.StiffnessType else None

    @stiffness_type.setter
    def stiffness_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RigidConnectorStiffnessType.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorStiffnessType.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorStiffnessType.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.StiffnessType = value

    @property
    def contact_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ContactDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ContactDiameter) if self.wrapped.ContactDiameter else None

    @contact_diameter.setter
    def contact_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ContactDiameter = value

    @property
    def number_of_contacts_per_direction(self) -> 'int':
        '''int: 'NumberOfContactsPerDirection' is the original name of this property.'''

        return self.wrapped.NumberOfContactsPerDirection

    @number_of_contacts_per_direction.setter
    def number_of_contacts_per_direction(self, value: 'int'):
        self.wrapped.NumberOfContactsPerDirection = int(value) if value else 0

    @property
    def angular_extent_of_external_teeth(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AngularExtentOfExternalTeeth' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AngularExtentOfExternalTeeth) if self.wrapped.AngularExtentOfExternalTeeth else None

    @angular_extent_of_external_teeth.setter
    def angular_extent_of_external_teeth(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.AngularExtentOfExternalTeeth = value

    @property
    def centre_angle_of_first_external_tooth(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'CentreAngleOfFirstExternalTooth' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.CentreAngleOfFirstExternalTooth) if self.wrapped.CentreAngleOfFirstExternalTooth else None

    @centre_angle_of_first_external_tooth.setter
    def centre_angle_of_first_external_tooth(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.CentreAngleOfFirstExternalTooth = value

    @property
    def contact_stiffness(self) -> 'float':
        '''float: 'ContactStiffness' is the original name of this property.'''

        return self.wrapped.ContactStiffness

    @contact_stiffness.setter
    def contact_stiffness(self, value: 'float'):
        self.wrapped.ContactStiffness = float(value) if value else 0.0

    @property
    def pressure_angle(self) -> 'float':
        '''float: 'PressureAngle' is the original name of this property.'''

        return self.wrapped.PressureAngle

    @pressure_angle.setter
    def pressure_angle(self, value: 'float'):
        self.wrapped.PressureAngle = float(value) if value else 0.0

    @property
    def normal_clearance(self) -> 'float':
        '''float: 'NormalClearance' is the original name of this property.'''

        return self.wrapped.NormalClearance

    @normal_clearance.setter
    def normal_clearance(self, value: 'float'):
        self.wrapped.NormalClearance = float(value) if value else 0.0

    @property
    def helix_angle(self) -> 'float':
        '''float: 'HelixAngle' is the original name of this property.'''

        return self.wrapped.HelixAngle

    @helix_angle.setter
    def helix_angle(self, value: 'float'):
        self.wrapped.HelixAngle = float(value) if value else 0.0

    @property
    def left_flank_helix_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'LeftFlankHelixAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.LeftFlankHelixAngle) if self.wrapped.LeftFlankHelixAngle else None

    @left_flank_helix_angle.setter
    def left_flank_helix_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.LeftFlankHelixAngle = value

    @property
    def right_flank_helix_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RightFlankHelixAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RightFlankHelixAngle) if self.wrapped.RightFlankHelixAngle else None

    @right_flank_helix_angle.setter
    def right_flank_helix_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.RightFlankHelixAngle = value

    @property
    def type_of_fit(self) -> 'enum_with_selected_value.EnumWithSelectedValue_FitTypes':
        '''enum_with_selected_value.EnumWithSelectedValue_FitTypes: 'TypeOfFit' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_FitTypes)(self.wrapped.TypeOfFit) if self.wrapped.TypeOfFit else None

    @type_of_fit.setter
    def type_of_fit(self, value: 'enum_with_selected_value.EnumWithSelectedValue_FitTypes.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_FitTypes.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FitTypes.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.TypeOfFit = value

    @property
    def tooth_spacing_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RigidConnectorToothSpacingType':
        '''enum_with_selected_value.EnumWithSelectedValue_RigidConnectorToothSpacingType: 'ToothSpacingType' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_RigidConnectorToothSpacingType)(self.wrapped.ToothSpacingType) if self.wrapped.ToothSpacingType else None

    @tooth_spacing_type.setter
    def tooth_spacing_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RigidConnectorToothSpacingType.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorToothSpacingType.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorToothSpacingType.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.ToothSpacingType = value

    @property
    def coefficient_of_friction(self) -> 'float':
        '''float: 'CoefficientOfFriction' is the original name of this property.'''

        return self.wrapped.CoefficientOfFriction

    @coefficient_of_friction.setter
    def coefficient_of_friction(self, value: 'float'):
        self.wrapped.CoefficientOfFriction = float(value) if value else 0.0

    @property
    def tangential_stiffness(self) -> 'float':
        '''float: 'TangentialStiffness' is the original name of this property.'''

        return self.wrapped.TangentialStiffness

    @tangential_stiffness.setter
    def tangential_stiffness(self, value: 'float'):
        self.wrapped.TangentialStiffness = float(value) if value else 0.0

    @property
    def spline_joint_design(self) -> '_1153.SplineJointDesign':
        '''SplineJointDesign: 'SplineJointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1153.SplineJointDesign)(self.wrapped.SplineJointDesign) if self.wrapped.SplineJointDesign else None

    @property
    def spline_joint_design_of_type_custom_spline_joint_design(self) -> '_1128.CustomSplineJointDesign':
        '''CustomSplineJointDesign: 'SplineJointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.SplineJointDesign.__class__.__qualname__ != 'CustomSplineJointDesign':
            raise CastException('Failed to cast spline_joint_design to CustomSplineJointDesign. Expected: {}.'.format(self.wrapped.SplineJointDesign.__class__.__qualname__))

        return constructor.new(_1128.CustomSplineJointDesign)(self.wrapped.SplineJointDesign) if self.wrapped.SplineJointDesign else None

    @property
    def spline_joint_design_of_type_din5480_spline_joint_design(self) -> '_1131.DIN5480SplineJointDesign':
        '''DIN5480SplineJointDesign: 'SplineJointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.SplineJointDesign.__class__.__qualname__ != 'DIN5480SplineJointDesign':
            raise CastException('Failed to cast spline_joint_design to DIN5480SplineJointDesign. Expected: {}.'.format(self.wrapped.SplineJointDesign.__class__.__qualname__))

        return constructor.new(_1131.DIN5480SplineJointDesign)(self.wrapped.SplineJointDesign) if self.wrapped.SplineJointDesign else None

    @property
    def spline_joint_design_of_type_iso4156_spline_joint_design(self) -> '_1138.ISO4156SplineJointDesign':
        '''ISO4156SplineJointDesign: 'SplineJointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.SplineJointDesign.__class__.__qualname__ != 'ISO4156SplineJointDesign':
            raise CastException('Failed to cast spline_joint_design to ISO4156SplineJointDesign. Expected: {}.'.format(self.wrapped.SplineJointDesign.__class__.__qualname__))

        return constructor.new(_1138.ISO4156SplineJointDesign)(self.wrapped.SplineJointDesign) if self.wrapped.SplineJointDesign else None

    @property
    def spline_joint_design_of_type_sae_spline_joint_design(self) -> '_1146.SAESplineJointDesign':
        '''SAESplineJointDesign: 'SplineJointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.SplineJointDesign.__class__.__qualname__ != 'SAESplineJointDesign':
            raise CastException('Failed to cast spline_joint_design to SAESplineJointDesign. Expected: {}.'.format(self.wrapped.SplineJointDesign.__class__.__qualname__))

        return constructor.new(_1146.SAESplineJointDesign)(self.wrapped.SplineJointDesign) if self.wrapped.SplineJointDesign else None

    @property
    def spline_joint_design_of_type_gbt3478_spline_joint_design(self) -> '_1135.GBT3478SplineJointDesign':
        '''GBT3478SplineJointDesign: 'SplineJointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.SplineJointDesign.__class__.__qualname__ != 'GBT3478SplineJointDesign':
            raise CastException('Failed to cast spline_joint_design to GBT3478SplineJointDesign. Expected: {}.'.format(self.wrapped.SplineJointDesign.__class__.__qualname__))

        return constructor.new(_1135.GBT3478SplineJointDesign)(self.wrapped.SplineJointDesign) if self.wrapped.SplineJointDesign else None

    @property
    def spline_joint_design_of_type_jisb1603_spline_joint_design(self) -> '_1139.JISB1603SplineJointDesign':
        '''JISB1603SplineJointDesign: 'SplineJointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.SplineJointDesign.__class__.__qualname__ != 'JISB1603SplineJointDesign':
            raise CastException('Failed to cast spline_joint_design to JISB1603SplineJointDesign. Expected: {}.'.format(self.wrapped.SplineJointDesign.__class__.__qualname__))

        return constructor.new(_1139.JISB1603SplineJointDesign)(self.wrapped.SplineJointDesign) if self.wrapped.SplineJointDesign else None

    @property
    def interference_fit_design(self) -> '_1183.InterferenceFitDesign':
        '''InterferenceFitDesign: 'InterferenceFitDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1183.InterferenceFitDesign)(self.wrapped.InterferenceFitDesign) if self.wrapped.InterferenceFitDesign else None

    @property
    def nonlinear_stiffness(self) -> '_82.DiagonalNonlinearStiffness':
        '''DiagonalNonlinearStiffness: 'NonlinearStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_82.DiagonalNonlinearStiffness)(self.wrapped.NonlinearStiffness) if self.wrapped.NonlinearStiffness else None

    @property
    def tooth_locations_external_spline_half(self) -> 'List[_2072.RigidConnectorToothLocation]':
        '''List[RigidConnectorToothLocation]: 'ToothLocationsExternalSplineHalf' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ToothLocationsExternalSplineHalf, constructor.new(_2072.RigidConnectorToothLocation))
        return value
