'''_978.py

CylindricalGearSetManufacturingConfigurationSelection
'''


from mastapy._internal.implicit import list_with_selected_item
from mastapy.gears.manufacturing.cylindrical import _625
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_MANUFACTURING_CONFIGURATION_SELECTION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearSetManufacturingConfigurationSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetManufacturingConfigurationSelection',)


class CylindricalGearSetManufacturingConfigurationSelection(_1.APIBase):
    '''CylindricalGearSetManufacturingConfigurationSelection

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_MANUFACTURING_CONFIGURATION_SELECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetManufacturingConfigurationSelection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def manufacturing_configuration(self) -> 'list_with_selected_item.ListWithSelectedItem_CylindricalSetManufacturingConfig':
        '''list_with_selected_item.ListWithSelectedItem_CylindricalSetManufacturingConfig: 'ManufacturingConfiguration' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_CylindricalSetManufacturingConfig)(self.wrapped.ManufacturingConfiguration) if self.wrapped.ManufacturingConfiguration else None

    @manufacturing_configuration.setter
    def manufacturing_configuration(self, value: 'list_with_selected_item.ListWithSelectedItem_CylindricalSetManufacturingConfig.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_CylindricalSetManufacturingConfig.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_CylindricalSetManufacturingConfig.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.ManufacturingConfiguration = value
