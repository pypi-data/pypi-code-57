'''_560.py

ConicalGearManufacturingConfig
'''


from mastapy.gears.manufacturing.bevel import _562
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MANUFACTURING_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalGearManufacturingConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearManufacturingConfig',)


class ConicalGearManufacturingConfig(_562.ConicalGearMicroGeometryConfigBase):
    '''ConicalGearManufacturingConfig

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_MANUFACTURING_CONFIG

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearManufacturingConfig.TYPE'):
        super().__init__(instance_to_wrap)
