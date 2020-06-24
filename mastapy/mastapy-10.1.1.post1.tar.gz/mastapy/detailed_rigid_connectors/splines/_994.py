'''_994.py

FinishingMethods
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_FINISHING_METHODS = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'FinishingMethods')


__docformat__ = 'restructuredtext en'
__all__ = ('FinishingMethods',)


class FinishingMethods(Enum):
    '''FinishingMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _FINISHING_METHODS

    __hash__ = None

    GRINDING = 0
    UNSPECIFIED = 1
