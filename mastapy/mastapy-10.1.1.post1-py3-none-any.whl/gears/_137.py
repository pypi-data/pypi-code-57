'''_137.py

LubricationMethods
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_LUBRICATION_METHODS = python_net_import('SMT.MastaAPI.Gears', 'LubricationMethods')


__docformat__ = 'restructuredtext en'
__all__ = ('LubricationMethods',)


class LubricationMethods(Enum):
    '''LubricationMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _LUBRICATION_METHODS

    __hash__ = None

    SPRAYINJECTION_LUBRICATION = 0
    DIP_LUBRICATION = 1
    SUBMERGED = 2
    ADDITIONAL_SPRAY_LUBRICATION = 3
