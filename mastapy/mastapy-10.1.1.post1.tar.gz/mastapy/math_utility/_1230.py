'''_1230.py

ResultOptionsFor3DVector
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_RESULT_OPTIONS_FOR_3D_VECTOR = python_net_import('SMT.MastaAPI.MathUtility', 'ResultOptionsFor3DVector')


__docformat__ = 'restructuredtext en'
__all__ = ('ResultOptionsFor3DVector',)


class ResultOptionsFor3DVector(Enum):
    '''ResultOptionsFor3DVector

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _RESULT_OPTIONS_FOR_3D_VECTOR
    __hash__ = None

    X = 0
    Y = 1
    Z = 2
    MAGNITUDE_XY = 3
    MAGNITUDE = 4
