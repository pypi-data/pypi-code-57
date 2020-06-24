'''_373.py

CylindricalGearAGMAMaterialDatabase
'''


from mastapy.gears.materials import _376, _367
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_AGMA_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Gears.Materials', 'CylindricalGearAGMAMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearAGMAMaterialDatabase',)


class CylindricalGearAGMAMaterialDatabase(_376.CylindricalGearMaterialDatabase['_367.AGMACylindricalGearMaterial']):
    '''CylindricalGearAGMAMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_AGMA_MATERIAL_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearAGMAMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
