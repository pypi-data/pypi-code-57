'''_367.py

AGMACylindricalGearMaterial
'''


from mastapy.materials import _47, _48, _49
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy.gears.materials import _375
from mastapy._internal.python_net import python_net_import

_AGMA_CYLINDRICAL_GEAR_MATERIAL = python_net_import('SMT.MastaAPI.Gears.Materials', 'AGMACylindricalGearMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMACylindricalGearMaterial',)


class AGMACylindricalGearMaterial(_375.CylindricalGearMaterial):
    '''AGMACylindricalGearMaterial

    This is a mastapy class.
    '''

    TYPE = _AGMA_CYLINDRICAL_GEAR_MATERIAL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMACylindricalGearMaterial.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def material_application(self) -> '_47.AGMAMaterialApplications':
        '''AGMAMaterialApplications: 'MaterialApplication' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MaterialApplication)
        return constructor.new(_47.AGMAMaterialApplications)(value) if value else None

    @material_application.setter
    def material_application(self, value: '_47.AGMAMaterialApplications'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MaterialApplication = value

    @property
    def stress_cycle_factor_at_1e10_cycles_contact(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'StressCycleFactorAt1E10CyclesContact' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.StressCycleFactorAt1E10CyclesContact) if self.wrapped.StressCycleFactorAt1E10CyclesContact else None

    @stress_cycle_factor_at_1e10_cycles_contact.setter
    def stress_cycle_factor_at_1e10_cycles_contact(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.StressCycleFactorAt1E10CyclesContact = value

    @property
    def stress_cycle_factor_at_1e10_cycles_bending(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'StressCycleFactorAt1E10CyclesBending' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.StressCycleFactorAt1E10CyclesBending) if self.wrapped.StressCycleFactorAt1E10CyclesBending else None

    @stress_cycle_factor_at_1e10_cycles_bending.setter
    def stress_cycle_factor_at_1e10_cycles_bending(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.StressCycleFactorAt1E10CyclesBending = value

    @property
    def material_class(self) -> '_48.AGMAMaterialClasses':
        '''AGMAMaterialClasses: 'MaterialClass' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MaterialClass)
        return constructor.new(_48.AGMAMaterialClasses)(value) if value else None

    @material_class.setter
    def material_class(self, value: '_48.AGMAMaterialClasses'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MaterialClass = value

    @property
    def grade(self) -> '_49.AGMAMaterialGrade':
        '''AGMAMaterialGrade: 'Grade' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Grade)
        return constructor.new(_49.AGMAMaterialGrade)(value) if value else None

    @grade.setter
    def grade(self, value: '_49.AGMAMaterialGrade'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Grade = value

    @property
    def core_hardness_hb(self) -> 'float':
        '''float: 'CoreHardnessHB' is the original name of this property.'''

        return self.wrapped.CoreHardnessHB

    @core_hardness_hb.setter
    def core_hardness_hb(self, value: 'float'):
        self.wrapped.CoreHardnessHB = float(value) if value else 0.0

    @property
    def allowable_stress_number_bending(self) -> 'float':
        '''float: 'AllowableStressNumberBending' is the original name of this property.'''

        return self.wrapped.AllowableStressNumberBending

    @allowable_stress_number_bending.setter
    def allowable_stress_number_bending(self, value: 'float'):
        self.wrapped.AllowableStressNumberBending = float(value) if value else 0.0
