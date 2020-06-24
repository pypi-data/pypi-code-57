'''_959.py

ConicalGearMeshDesign
'''


from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy.gears.gear_designs.bevel import _1105, _1111, _1110
from mastapy.gears.gear_designs import _943
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical', 'ConicalGearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearMeshDesign',)


class ConicalGearMeshDesign(_943.GearMeshDesign):
    '''ConicalGearMeshDesign

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_MESH_DESIGN
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def shaft_angle(self) -> 'float':
        '''float: 'ShaftAngle' is the original name of this property.'''

        return self.wrapped.ShaftAngle

    @shaft_angle.setter
    def shaft_angle(self, value: 'float'):
        self.wrapped.ShaftAngle = float(value) if value else 0.0

    @property
    def overload_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'OverloadFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.OverloadFactor) if self.wrapped.OverloadFactor else None

    @overload_factor.setter
    def overload_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.OverloadFactor = value

    @property
    def specify_backlash(self) -> 'bool':
        '''bool: 'SpecifyBacklash' is the original name of this property.'''

        return self.wrapped.SpecifyBacklash

    @specify_backlash.setter
    def specify_backlash(self, value: 'bool'):
        self.wrapped.SpecifyBacklash = bool(value) if value else False

    @property
    def specified_backlash_range_min(self) -> 'float':
        '''float: 'SpecifiedBacklashRangeMin' is the original name of this property.'''

        return self.wrapped.SpecifiedBacklashRangeMin

    @specified_backlash_range_min.setter
    def specified_backlash_range_min(self, value: 'float'):
        self.wrapped.SpecifiedBacklashRangeMin = float(value) if value else 0.0

    @property
    def specified_backlash_range_max(self) -> 'float':
        '''float: 'SpecifiedBacklashRangeMax' is the original name of this property.'''

        return self.wrapped.SpecifiedBacklashRangeMax

    @specified_backlash_range_max.setter
    def specified_backlash_range_max(self, value: 'float'):
        self.wrapped.SpecifiedBacklashRangeMax = float(value) if value else 0.0

    @property
    def driven_machine_characteristic_gleason(self) -> '_1105.DrivenMachineCharacteristicGleason':
        '''DrivenMachineCharacteristicGleason: 'DrivenMachineCharacteristicGleason' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.DrivenMachineCharacteristicGleason)
        return constructor.new(_1105.DrivenMachineCharacteristicGleason)(value) if value else None

    @driven_machine_characteristic_gleason.setter
    def driven_machine_characteristic_gleason(self, value: '_1105.DrivenMachineCharacteristicGleason'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DrivenMachineCharacteristicGleason = value

    @property
    def prime_mover_characteristic_gleason(self) -> '_1111.PrimeMoverCharacteristicGleason':
        '''PrimeMoverCharacteristicGleason: 'PrimeMoverCharacteristicGleason' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.PrimeMoverCharacteristicGleason)
        return constructor.new(_1111.PrimeMoverCharacteristicGleason)(value) if value else None

    @prime_mover_characteristic_gleason.setter
    def prime_mover_characteristic_gleason(self, value: '_1111.PrimeMoverCharacteristicGleason'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.PrimeMoverCharacteristicGleason = value

    @property
    def prime_mover_characteristic(self) -> '_1110.MachineCharacteristicAGMAKlingelnberg':
        '''MachineCharacteristicAGMAKlingelnberg: 'PrimeMoverCharacteristic' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.PrimeMoverCharacteristic)
        return constructor.new(_1110.MachineCharacteristicAGMAKlingelnberg)(value) if value else None

    @prime_mover_characteristic.setter
    def prime_mover_characteristic(self, value: '_1110.MachineCharacteristicAGMAKlingelnberg'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.PrimeMoverCharacteristic = value

    @property
    def driven_machine_characteristic(self) -> '_1110.MachineCharacteristicAGMAKlingelnberg':
        '''MachineCharacteristicAGMAKlingelnberg: 'DrivenMachineCharacteristic' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.DrivenMachineCharacteristic)
        return constructor.new(_1110.MachineCharacteristicAGMAKlingelnberg)(value) if value else None

    @driven_machine_characteristic.setter
    def driven_machine_characteristic(self, value: '_1110.MachineCharacteristicAGMAKlingelnberg'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DrivenMachineCharacteristic = value

    @property
    def pinion_full_circle_edge_radius(self) -> 'float':
        '''float: 'PinionFullCircleEdgeRadius' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PinionFullCircleEdgeRadius

    @property
    def maximum_normal_backlash(self) -> 'float':
        '''float: 'MaximumNormalBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumNormalBacklash

    @property
    def minimum_normal_backlash(self) -> 'float':
        '''float: 'MinimumNormalBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumNormalBacklash
