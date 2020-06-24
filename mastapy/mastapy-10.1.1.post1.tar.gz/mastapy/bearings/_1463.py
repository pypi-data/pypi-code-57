'''_1463.py

BearingDampingMatrixOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_BEARING_DAMPING_MATRIX_OPTION = python_net_import('SMT.MastaAPI.Bearings', 'BearingDampingMatrixOption')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingDampingMatrixOption',)


class BearingDampingMatrixOption(Enum):
    '''BearingDampingMatrixOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _BEARING_DAMPING_MATRIX_OPTION
    __hash__ = None

    NO_DAMPING = 0
    SPECIFY_MATRIX = 1
    SPEED_DEPENDENT = 2
