'''_105.py

OilSealMaterialType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_OIL_SEAL_MATERIAL_TYPE = python_net_import('SMT.MastaAPI.Materials.Efficiency', 'OilSealMaterialType')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealMaterialType',)


class OilSealMaterialType(Enum):
    '''OilSealMaterialType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _OIL_SEAL_MATERIAL_TYPE

    __hash__ = None

    VITON = 0
    BUNAN = 1
