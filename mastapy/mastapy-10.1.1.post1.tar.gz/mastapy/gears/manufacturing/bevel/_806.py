'''_806.py

ConicalMeshManufacturingConfig
'''


from mastapy.gears.manufacturing.bevel import _815, _808
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_MANUFACTURING_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalMeshManufacturingConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshManufacturingConfig',)


class ConicalMeshManufacturingConfig(_808.ConicalMeshMicroGeometryConfigBase):
    '''ConicalMeshManufacturingConfig

    This is a mastapy class.
    '''

    TYPE = _CONICAL_MESH_MANUFACTURING_CONFIG
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalMeshManufacturingConfig.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def wheel_config(self) -> '_815.ConicalWheelManufacturingConfig':
        '''ConicalWheelManufacturingConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_815.ConicalWheelManufacturingConfig)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None
