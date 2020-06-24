'''_409.py

CylindricalSetManufacturingConfig
'''


from typing import List

from mastapy.gears.manufacturing.cylindrical import _406, _396
from mastapy._internal import constructor, conversion
from mastapy.gears.analysis import _962
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_SET_MANUFACTURING_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalSetManufacturingConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalSetManufacturingConfig',)


class CylindricalSetManufacturingConfig(_962.GearSetImplementationDetail):
    '''CylindricalSetManufacturingConfig

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_SET_MANUFACTURING_CONFIG

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalSetManufacturingConfig.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def cylindrical_mesh_manufacturing_configurations(self) -> 'List[_406.CylindricalMeshManufacturingConfig]':
        '''List[CylindricalMeshManufacturingConfig]: 'CylindricalMeshManufacturingConfigurations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshManufacturingConfigurations, constructor.new(_406.CylindricalMeshManufacturingConfig))
        return value

    @property
    def cylindrical_gear_manufacturing_configurations(self) -> 'List[_396.CylindricalGearManufacturingConfig]':
        '''List[CylindricalGearManufacturingConfig]: 'CylindricalGearManufacturingConfigurations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearManufacturingConfigurations, constructor.new(_396.CylindricalGearManufacturingConfig))
        return value
