'''_1109.py

AGMAGleasonConicalGearSetDesign
'''


from typing import Callable, List

from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.gears.gear_designs.bevel import _1098
from mastapy._internal import constructor, conversion
from mastapy.gears import _323, _321
from mastapy.gears.gear_designs.conical import _1090, _863
from mastapy.gleason_smt_link import _280
from mastapy.gears.gear_designs.agma_gleason_conical import _1108
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.AGMAGleasonConical', 'AGMAGleasonConicalGearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearSetDesign',)


class AGMAGleasonConicalGearSetDesign(_863.ConicalGearSetDesign):
    '''AGMAGleasonConicalGearSetDesign

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_SET_DESIGN
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def design_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods':
        '''enum_with_selected_value.EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods: 'DesignMethod' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods)(self.wrapped.DesignMethod) if self.wrapped.DesignMethod else None

    @design_method.setter
    def design_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.DesignMethod = value

    @property
    def input_module(self) -> 'bool':
        '''bool: 'InputModule' is the original name of this property.'''

        return self.wrapped.InputModule

    @input_module.setter
    def input_module(self, value: 'bool'):
        self.wrapped.InputModule = bool(value) if value else False

    @property
    def mean_normal_module(self) -> 'float':
        '''float: 'MeanNormalModule' is the original name of this property.'''

        return self.wrapped.MeanNormalModule

    @mean_normal_module.setter
    def mean_normal_module(self, value: 'float'):
        self.wrapped.MeanNormalModule = float(value) if value else 0.0

    @property
    def tooth_taper(self) -> '_323.SpiralBevelToothTaper':
        '''SpiralBevelToothTaper: 'ToothTaper' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ToothTaper)
        return constructor.new(_323.SpiralBevelToothTaper)(value) if value else None

    @tooth_taper.setter
    def tooth_taper(self, value: '_323.SpiralBevelToothTaper'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ToothTaper = value

    @property
    def reliability_requirement_gleason(self) -> '_1090.GleasonSafetyRequirements':
        '''GleasonSafetyRequirements: 'ReliabilityRequirementGleason' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ReliabilityRequirementGleason)
        return constructor.new(_1090.GleasonSafetyRequirements)(value) if value else None

    @reliability_requirement_gleason.setter
    def reliability_requirement_gleason(self, value: '_1090.GleasonSafetyRequirements'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ReliabilityRequirementGleason = value

    @property
    def reliability_requirement_agma(self) -> '_321.SafetyRequirementsAGMA':
        '''SafetyRequirementsAGMA: 'ReliabilityRequirementAGMA' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ReliabilityRequirementAGMA)
        return constructor.new(_321.SafetyRequirementsAGMA)(value) if value else None

    @reliability_requirement_agma.setter
    def reliability_requirement_agma(self, value: '_321.SafetyRequirementsAGMA'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ReliabilityRequirementAGMA = value

    @property
    def gleason_minimum_factor_of_safety_contact(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'GleasonMinimumFactorOfSafetyContact' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.GleasonMinimumFactorOfSafetyContact) if self.wrapped.GleasonMinimumFactorOfSafetyContact else None

    @gleason_minimum_factor_of_safety_contact.setter
    def gleason_minimum_factor_of_safety_contact(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.GleasonMinimumFactorOfSafetyContact = value

    @property
    def gleason_minimum_factor_of_safety_bending(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'GleasonMinimumFactorOfSafetyBending' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.GleasonMinimumFactorOfSafetyBending) if self.wrapped.GleasonMinimumFactorOfSafetyBending else None

    @gleason_minimum_factor_of_safety_bending.setter
    def gleason_minimum_factor_of_safety_bending(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.GleasonMinimumFactorOfSafetyBending = value

    @property
    def reliability_factor_contact(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ReliabilityFactorContact' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ReliabilityFactorContact) if self.wrapped.ReliabilityFactorContact else None

    @reliability_factor_contact.setter
    def reliability_factor_contact(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ReliabilityFactorContact = value

    @property
    def reliability_factor_bending(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ReliabilityFactorBending' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ReliabilityFactorBending) if self.wrapped.ReliabilityFactorBending else None

    @reliability_factor_bending.setter
    def reliability_factor_bending(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ReliabilityFactorBending = value

    @property
    def number_of_blade_groups(self) -> 'float':
        '''float: 'NumberOfBladeGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfBladeGroups

    @property
    def number_of_crown_gear_teeth(self) -> 'float':
        '''float: 'NumberOfCrownGearTeeth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfCrownGearTeeth

    @property
    def crown_gear_to_cutter_centre_distance(self) -> 'float':
        '''float: 'CrownGearToCutterCentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CrownGearToCutterCentreDistance

    @property
    def wheel_involute_cone_distance(self) -> 'float':
        '''float: 'WheelInvoluteConeDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WheelInvoluteConeDistance

    @property
    def wheel_involute_to_outer_cone_distance_ratio(self) -> 'float':
        '''float: 'WheelInvoluteToOuterConeDistanceRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WheelInvoluteToOuterConeDistanceRatio

    @property
    def wheel_involute_to_mean_cone_distance_ratio(self) -> 'float':
        '''float: 'WheelInvoluteToMeanConeDistanceRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WheelInvoluteToMeanConeDistanceRatio

    @property
    def epicycloid_base_circle_radius(self) -> 'float':
        '''float: 'EpicycloidBaseCircleRadius' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EpicycloidBaseCircleRadius

    @property
    def store_ki_mo_skip_file(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'StoreKIMoSKIPFile' is the original name of this property.'''

        return self.wrapped.StoreKIMoSKIPFile

    @store_ki_mo_skip_file.setter
    def store_ki_mo_skip_file(self, value: 'Callable[[], None]'):
        value = value if value else None
        self.wrapped.StoreKIMoSKIPFile = value

    @property
    def export_ki_mo_skip_file(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ExportKIMoSKIPFile' is the original name of this property.'''

        return self.wrapped.ExportKIMoSKIPFile

    @export_ki_mo_skip_file.setter
    def export_ki_mo_skip_file(self, value: 'Callable[[], None]'):
        value = value if value else None
        self.wrapped.ExportKIMoSKIPFile = value

    @property
    def ki_mo_sxml_data(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'KIMoSXMLData' is the original name of this property.'''

        return self.wrapped.KIMoSXMLData

    @ki_mo_sxml_data.setter
    def ki_mo_sxml_data(self, value: 'Callable[[], None]'):
        value = value if value else None
        self.wrapped.KIMoSXMLData = value

    @property
    def gleason_gemsxml_data(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'GleasonGEMSXMLData' is the original name of this property.'''

        return self.wrapped.GleasonGEMSXMLData

    @gleason_gemsxml_data.setter
    def gleason_gemsxml_data(self, value: 'Callable[[], None]'):
        value = value if value else None
        self.wrapped.GleasonGEMSXMLData = value

    @property
    def manufacturing_method(self) -> '_280.CutterMethod':
        '''CutterMethod: 'ManufacturingMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ManufacturingMethod)
        return constructor.new(_280.CutterMethod)(value) if value else None

    @manufacturing_method.setter
    def manufacturing_method(self, value: '_280.CutterMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ManufacturingMethod = value

    @property
    def required_minimum_topland_to_module_factor(self) -> 'float':
        '''float: 'RequiredMinimumToplandToModuleFactor' is the original name of this property.'''

        return self.wrapped.RequiredMinimumToplandToModuleFactor

    @required_minimum_topland_to_module_factor.setter
    def required_minimum_topland_to_module_factor(self, value: 'float'):
        self.wrapped.RequiredMinimumToplandToModuleFactor = float(value) if value else 0.0

    @property
    def pitch_limit_pressure_angle(self) -> 'float':
        '''float: 'PitchLimitPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PitchLimitPressureAngle

    @property
    def pinion_offset_angle_in_root_plane(self) -> 'float':
        '''float: 'PinionOffsetAngleInRootPlane' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PinionOffsetAngleInRootPlane

    @property
    def conical_meshes(self) -> 'List[_1108.AGMAGleasonConicalGearMeshDesign]':
        '''List[AGMAGleasonConicalGearMeshDesign]: 'ConicalMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConicalMeshes, constructor.new(_1108.AGMAGleasonConicalGearMeshDesign))
        return value

    @property
    def meshes(self) -> 'List[_1108.AGMAGleasonConicalGearMeshDesign]':
        '''List[AGMAGleasonConicalGearMeshDesign]: 'Meshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Meshes, constructor.new(_1108.AGMAGleasonConicalGearMeshDesign))
        return value
