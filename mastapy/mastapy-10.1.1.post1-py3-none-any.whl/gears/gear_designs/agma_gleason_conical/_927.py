'''_927.py

AGMAGleasonConicalGearDesign
'''


from mastapy.gears.gear_designs.conical import (
    _898, _892, _891, _887,
    _897, _888
)
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import enum_with_selected_value
from mastapy._internal.python_net import python_net_import
from mastapy.gears.manufacturing.bevel.cutters import (
    _597, _598, _599, _600
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears import _116
from mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances import _871, _875, _879
from mastapy.gears.gear_designs.agma_gleason_conical import _926
from mastapy.gears.materials import (
    _378, _367, _369, _371,
    _375, _381, _385, _387
)

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_AGMA_GLEASON_CONICAL_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.AGMAGleasonConical', 'AGMAGleasonConicalGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearDesign',)


class AGMAGleasonConicalGearDesign(_888.ConicalGearDesign):
    '''AGMAGleasonConicalGearDesign

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def front_end_type(self) -> '_898.FrontEndTypes':
        '''FrontEndTypes: 'FrontEndType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.FrontEndType)
        return constructor.new(_898.FrontEndTypes)(value) if value else None

    @front_end_type.setter
    def front_end_type(self, value: '_898.FrontEndTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FrontEndType = value

    @property
    def manufacture_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods':
        '''enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods: 'ManufactureMethod' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.ManufactureMethod, value) if self.wrapped.ManufactureMethod else None

    @manufacture_method.setter
    def manufacture_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ManufactureMethod = value

    @property
    def machine_setting_calculation_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods':
        '''enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods: 'MachineSettingCalculationMethod' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.MachineSettingCalculationMethod, value) if self.wrapped.MachineSettingCalculationMethod else None

    @machine_setting_calculation_method.setter
    def machine_setting_calculation_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.MachineSettingCalculationMethod = value

    @property
    def material(self) -> 'str':
        '''str: 'Material' is the original name of this property.'''

        return self.wrapped.Material.SelectedItemName

    @material.setter
    def material(self, value: 'str'):
        self.wrapped.Material.SetSelectedItem(str(value) if value else None)

    @property
    def allowable_bending_stress(self) -> 'float':
        '''float: 'AllowableBendingStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AllowableBendingStress

    @property
    def allowable_contact_stress(self) -> 'float':
        '''float: 'AllowableContactStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AllowableContactStress

    @property
    def face_width(self) -> 'float':
        '''float: 'FaceWidth' is the original name of this property.'''

        return self.wrapped.FaceWidth

    @face_width.setter
    def face_width(self, value: 'float'):
        self.wrapped.FaceWidth = float(value) if value else 0.0

    @property
    def cutter(self) -> '_887.ConicalGearCutter':
        '''ConicalGearCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_887.ConicalGearCutter)(self.wrapped.Cutter) if self.wrapped.Cutter else None

    @property
    def cutter_of_type_pinion_finish_cutter(self) -> '_597.PinionFinishCutter':
        '''PinionFinishCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _597.PinionFinishCutter.TYPE not in self.wrapped.Cutter.__class__.__mro__:
            raise CastException('Failed to cast cutter to PinionFinishCutter. Expected: {}.'.format(self.wrapped.Cutter.__class__.__qualname__))

        return constructor.new(_597.PinionFinishCutter)(self.wrapped.Cutter) if self.wrapped.Cutter else None

    @property
    def cutter_of_type_pinion_rough_cutter(self) -> '_598.PinionRoughCutter':
        '''PinionRoughCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _598.PinionRoughCutter.TYPE not in self.wrapped.Cutter.__class__.__mro__:
            raise CastException('Failed to cast cutter to PinionRoughCutter. Expected: {}.'.format(self.wrapped.Cutter.__class__.__qualname__))

        return constructor.new(_598.PinionRoughCutter)(self.wrapped.Cutter) if self.wrapped.Cutter else None

    @property
    def cutter_of_type_wheel_finish_cutter(self) -> '_599.WheelFinishCutter':
        '''WheelFinishCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _599.WheelFinishCutter.TYPE not in self.wrapped.Cutter.__class__.__mro__:
            raise CastException('Failed to cast cutter to WheelFinishCutter. Expected: {}.'.format(self.wrapped.Cutter.__class__.__qualname__))

        return constructor.new(_599.WheelFinishCutter)(self.wrapped.Cutter) if self.wrapped.Cutter else None

    @property
    def cutter_of_type_wheel_rough_cutter(self) -> '_600.WheelRoughCutter':
        '''WheelRoughCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _600.WheelRoughCutter.TYPE not in self.wrapped.Cutter.__class__.__mro__:
            raise CastException('Failed to cast cutter to WheelRoughCutter. Expected: {}.'.format(self.wrapped.Cutter.__class__.__qualname__))

        return constructor.new(_600.WheelRoughCutter)(self.wrapped.Cutter) if self.wrapped.Cutter else None

    @property
    def cutter_of_type_dummy_conical_gear_cutter(self) -> '_897.DummyConicalGearCutter':
        '''DummyConicalGearCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _897.DummyConicalGearCutter.TYPE not in self.wrapped.Cutter.__class__.__mro__:
            raise CastException('Failed to cast cutter to DummyConicalGearCutter. Expected: {}.'.format(self.wrapped.Cutter.__class__.__qualname__))

        return constructor.new(_897.DummyConicalGearCutter)(self.wrapped.Cutter) if self.wrapped.Cutter else None

    @property
    def accuracy_grades(self) -> '_116.AccuracyGrades':
        '''AccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_116.AccuracyGrades)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades else None

    @property
    def accuracy_grades_of_type_agma20151_accuracy_grades(self) -> '_871.AGMA20151AccuracyGrades':
        '''AGMA20151AccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _871.AGMA20151AccuracyGrades.TYPE not in self.wrapped.AccuracyGrades.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades to AGMA20151AccuracyGrades. Expected: {}.'.format(self.wrapped.AccuracyGrades.__class__.__qualname__))

        return constructor.new(_871.AGMA20151AccuracyGrades)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades else None

    @property
    def accuracy_grades_of_type_cylindrical_accuracy_grades(self) -> '_875.CylindricalAccuracyGrades':
        '''CylindricalAccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _875.CylindricalAccuracyGrades.TYPE not in self.wrapped.AccuracyGrades.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades to CylindricalAccuracyGrades. Expected: {}.'.format(self.wrapped.AccuracyGrades.__class__.__qualname__))

        return constructor.new(_875.CylindricalAccuracyGrades)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades else None

    @property
    def accuracy_grades_of_type_iso1328_accuracy_grades(self) -> '_879.ISO1328AccuracyGrades':
        '''ISO1328AccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _879.ISO1328AccuracyGrades.TYPE not in self.wrapped.AccuracyGrades.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades to ISO1328AccuracyGrades. Expected: {}.'.format(self.wrapped.AccuracyGrades.__class__.__qualname__))

        return constructor.new(_879.ISO1328AccuracyGrades)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades else None

    @property
    def accuracy_grades_of_type_agma_gleason_conical_accuracy_grades(self) -> '_926.AGMAGleasonConicalAccuracyGrades':
        '''AGMAGleasonConicalAccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _926.AGMAGleasonConicalAccuracyGrades.TYPE not in self.wrapped.AccuracyGrades.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades to AGMAGleasonConicalAccuracyGrades. Expected: {}.'.format(self.wrapped.AccuracyGrades.__class__.__qualname__))

        return constructor.new(_926.AGMAGleasonConicalAccuracyGrades)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades else None

    @property
    def bevel_gear_material(self) -> '_378.GearMaterial':
        '''GearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_378.GearMaterial)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial else None

    @property
    def bevel_gear_material_of_type_agma_cylindrical_gear_material(self) -> '_367.AGMACylindricalGearMaterial':
        '''AGMACylindricalGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _367.AGMACylindricalGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to AGMACylindricalGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new(_367.AGMACylindricalGearMaterial)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial else None

    @property
    def bevel_gear_material_of_type_bevel_gear_iso_material(self) -> '_369.BevelGearISOMaterial':
        '''BevelGearISOMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _369.BevelGearISOMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to BevelGearISOMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new(_369.BevelGearISOMaterial)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial else None

    @property
    def bevel_gear_material_of_type_bevel_gear_material(self) -> '_371.BevelGearMaterial':
        '''BevelGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _371.BevelGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to BevelGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new(_371.BevelGearMaterial)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial else None

    @property
    def bevel_gear_material_of_type_cylindrical_gear_material(self) -> '_375.CylindricalGearMaterial':
        '''CylindricalGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _375.CylindricalGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to CylindricalGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new(_375.CylindricalGearMaterial)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial else None

    @property
    def bevel_gear_material_of_type_iso_cylindrical_gear_material(self) -> '_381.ISOCylindricalGearMaterial':
        '''ISOCylindricalGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _381.ISOCylindricalGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to ISOCylindricalGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new(_381.ISOCylindricalGearMaterial)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial else None

    @property
    def bevel_gear_material_of_type_klingelnberg_cyclo_palloid_conical_gear_material(self) -> '_385.KlingelnbergCycloPalloidConicalGearMaterial':
        '''KlingelnbergCycloPalloidConicalGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _385.KlingelnbergCycloPalloidConicalGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to KlingelnbergCycloPalloidConicalGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new(_385.KlingelnbergCycloPalloidConicalGearMaterial)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial else None

    @property
    def bevel_gear_material_of_type_plastic_cylindrical_gear_material(self) -> '_387.PlasticCylindricalGearMaterial':
        '''PlasticCylindricalGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _387.PlasticCylindricalGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to PlasticCylindricalGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new(_387.PlasticCylindricalGearMaterial)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial else None
