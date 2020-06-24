'''_284.py

MaterialPropertyClass
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MATERIAL_PROPERTY_CLASS = python_net_import('SMT.MastaAPI.FETools.Enums', 'MaterialPropertyClass')


__docformat__ = 'restructuredtext en'
__all__ = ('MaterialPropertyClass',)


class MaterialPropertyClass(Enum):
    '''MaterialPropertyClass

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _MATERIAL_PROPERTY_CLASS
    __hash__ = None

    LINEAR_ISOTROPIC = 0
    LINEAR_ORTHOTROPIC = 2
    LINEAR_ANISOTROPIC = 3
    HYPERELASTIC = 4
    UNKNOWN_CLASS = 5
