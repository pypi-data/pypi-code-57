'''_1176.py

KeyTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_KEY_TYPES = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.KeyedJoints', 'KeyTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('KeyTypes',)


class KeyTypes(Enum):
    '''KeyTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _KEY_TYPES
    __hash__ = None

    TYPE_A = 0
    TYPE_B = 1
    TYPE_AB = 2
    TYPE_C = 3
    TYPE_D = 4
    TYPE_E = 5
    TYPE_F = 6
    TYPE_G = 7
    TYPE_H = 8
    TYPE_J = 9
