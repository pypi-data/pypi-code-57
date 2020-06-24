'''_1231.py

RotationAxis
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ROTATION_AXIS = python_net_import('SMT.MastaAPI.MathUtility', 'RotationAxis')


__docformat__ = 'restructuredtext en'
__all__ = ('RotationAxis',)


class RotationAxis(Enum):
    '''RotationAxis

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ROTATION_AXIS
    __hash__ = None

    X_AXIS = 0
    Y_AXIS = 1
    Z_AXIS = 2
    USERSPECIFIED = 3
