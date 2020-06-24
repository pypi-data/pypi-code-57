'''_1934.py

PowerLoad
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable, enum_with_selected_value
from mastapy.system_model import _1735
from mastapy.system_model.part_model import _1941, _1939
from mastapy._internal.python_net import python_net_import

_POWER_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PowerLoad')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoad',)


class PowerLoad(_1939.VirtualComponent):
    '''PowerLoad

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoad.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def positive_is_forwards(self) -> 'bool':
        '''bool: 'PositiveIsForwards' is the original name of this property.'''

        return self.wrapped.PositiveIsForwards

    @positive_is_forwards.setter
    def positive_is_forwards(self, value: 'bool'):
        self.wrapped.PositiveIsForwards = bool(value) if value else False

    @property
    def tyre_rolling_radius(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TyreRollingRadius' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TyreRollingRadius) if self.wrapped.TyreRollingRadius else None

    @tyre_rolling_radius.setter
    def tyre_rolling_radius(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.TyreRollingRadius = value

    @property
    def torsional_stiffness(self) -> 'float':
        '''float: 'TorsionalStiffness' is the original name of this property.'''

        return self.wrapped.TorsionalStiffness

    @torsional_stiffness.setter
    def torsional_stiffness(self, value: 'float'):
        self.wrapped.TorsionalStiffness = float(value) if value else 0.0

    @property
    def power_load_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_PowerLoadType':
        '''enum_with_selected_value.EnumWithSelectedValue_PowerLoadType: 'PowerLoadType' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_PowerLoadType)(self.wrapped.PowerLoadType) if self.wrapped.PowerLoadType else None

    @power_load_type.setter
    def power_load_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_PowerLoadType.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_PowerLoadType.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_PowerLoadType.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.PowerLoadType = value

    @property
    def number_of_blades(self) -> 'int':
        '''int: 'NumberOfBlades' is the original name of this property.'''

        return self.wrapped.NumberOfBlades

    @number_of_blades.setter
    def number_of_blades(self, value: 'int'):
        self.wrapped.NumberOfBlades = int(value) if value else 0

    @property
    def number_of_wheels(self) -> 'int':
        '''int: 'NumberOfWheels' is the original name of this property.'''

        return self.wrapped.NumberOfWheels

    @number_of_wheels.setter
    def number_of_wheels(self, value: 'int'):
        self.wrapped.NumberOfWheels = int(value) if value else 0

    @property
    def default_number_of_slots(self) -> 'int':
        '''int: 'DefaultNumberOfSlots' is the original name of this property.'''

        return self.wrapped.DefaultNumberOfSlots

    @default_number_of_slots.setter
    def default_number_of_slots(self, value: 'int'):
        self.wrapped.DefaultNumberOfSlots = int(value) if value else 0

    @property
    def default_inner_diameter_of_stator_teeth(self) -> 'float':
        '''float: 'DefaultInnerDiameterOfStatorTeeth' is the original name of this property.'''

        return self.wrapped.DefaultInnerDiameterOfStatorTeeth

    @default_inner_diameter_of_stator_teeth.setter
    def default_inner_diameter_of_stator_teeth(self, value: 'float'):
        self.wrapped.DefaultInnerDiameterOfStatorTeeth = float(value) if value else 0.0

    @property
    def default_effective_length(self) -> 'float':
        '''float: 'DefaultEffectiveLength' is the original name of this property.'''

        return self.wrapped.DefaultEffectiveLength

    @default_effective_length.setter
    def default_effective_length(self, value: 'float'):
        self.wrapped.DefaultEffectiveLength = float(value) if value else 0.0

    @property
    def width_for_drawing(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'WidthForDrawing' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.WidthForDrawing) if self.wrapped.WidthForDrawing else None

    @width_for_drawing.setter
    def width_for_drawing(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.WidthForDrawing = value

    @property
    def single_blade_details(self) -> '_1941.WindTurbineSingleBladeDetails':
        '''WindTurbineSingleBladeDetails: 'SingleBladeDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1941.WindTurbineSingleBladeDetails)(self.wrapped.SingleBladeDetails) if self.wrapped.SingleBladeDetails else None
