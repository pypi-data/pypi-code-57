'''_1376.py

GravityForceSource
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_GRAVITY_FORCE_SOURCE = python_net_import('SMT.MastaAPI.NodalAnalysis', 'GravityForceSource')


__docformat__ = 'restructuredtext en'
__all__ = ('GravityForceSource',)


class GravityForceSource(Enum):
    '''GravityForceSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _GRAVITY_FORCE_SOURCE

    __hash__ = None

    NOT_AVAILABLE = 0
    CALCULATED_FROM_MASS_MATRIX = 1
    CALCULATED_FROM_X_Y_Z_COMPONENTS = 2
    IMPORTED_SINGLE_VECTOR = 3
