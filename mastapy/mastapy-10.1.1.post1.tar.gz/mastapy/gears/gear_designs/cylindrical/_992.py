'''_992.py

GearSetManufacturingConfigurationSetup
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _968, _990
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_SET_MANUFACTURING_CONFIGURATION_SETUP = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'GearSetManufacturingConfigurationSetup')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetManufacturingConfigurationSetup',)


class GearSetManufacturingConfigurationSetup(_1.APIBase):
    '''GearSetManufacturingConfigurationSetup

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_MANUFACTURING_CONFIGURATION_SETUP
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetManufacturingConfigurationSetup.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def create_new_suitable_cutters(self) -> '_968.CreateNewSuitableCutterOption':
        '''CreateNewSuitableCutterOption: 'CreateNewSuitableCutters' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.CreateNewSuitableCutters)
        return constructor.new(_968.CreateNewSuitableCutterOption)(value) if value else None

    @create_new_suitable_cutters.setter
    def create_new_suitable_cutters(self, value: '_968.CreateNewSuitableCutterOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CreateNewSuitableCutters = value

    @property
    def use_as_design_mode_geometry(self) -> '_968.CreateNewSuitableCutterOption':
        '''CreateNewSuitableCutterOption: 'UseAsDesignModeGeometry' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.UseAsDesignModeGeometry)
        return constructor.new(_968.CreateNewSuitableCutterOption)(value) if value else None

    @use_as_design_mode_geometry.setter
    def use_as_design_mode_geometry(self, value: '_968.CreateNewSuitableCutterOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.UseAsDesignModeGeometry = value

    @property
    def gears(self) -> 'List[_990.GearManufacturingConfigSetupViewModel]':
        '''List[GearManufacturingConfigSetupViewModel]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_990.GearManufacturingConfigSetupViewModel))
        return value
