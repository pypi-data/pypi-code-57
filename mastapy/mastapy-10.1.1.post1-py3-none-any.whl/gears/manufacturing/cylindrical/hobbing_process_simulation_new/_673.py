'''_673.py

HobbingProcessSimulationInput
'''


from mastapy._internal.implicit import enum_with_selected_value
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _658, _677, _678, _692
)
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_HOBBING_PROCESS_SIMULATION_INPUT = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'HobbingProcessSimulationInput')


__docformat__ = 'restructuredtext en'
__all__ = ('HobbingProcessSimulationInput',)


class HobbingProcessSimulationInput(_692.ProcessSimulationInput):
    '''HobbingProcessSimulationInput

    This is a mastapy class.
    '''

    TYPE = _HOBBING_PROCESS_SIMULATION_INPUT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HobbingProcessSimulationInput.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def process_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ActiveProcessMethod':
        '''enum_with_selected_value.EnumWithSelectedValue_ActiveProcessMethod: 'ProcessMethod' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_ActiveProcessMethod)(self.wrapped.ProcessMethod) if self.wrapped.ProcessMethod else None

    @process_method.setter
    def process_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ActiveProcessMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_ActiveProcessMethod.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ActiveProcessMethod.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.ProcessMethod = value

    @property
    def hob_manufacture_error(self) -> '_677.HobManufactureError':
        '''HobManufactureError: 'HobManufactureError' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_677.HobManufactureError)(self.wrapped.HobManufactureError) if self.wrapped.HobManufactureError else None

    @property
    def hob_resharpening_error(self) -> '_678.HobResharpeningError':
        '''HobResharpeningError: 'HobResharpeningError' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_678.HobResharpeningError)(self.wrapped.HobResharpeningError) if self.wrapped.HobResharpeningError else None
