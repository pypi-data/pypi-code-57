'''_866.py

UseAdvancedLTCAOptions
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_USE_ADVANCED_LTCA_OPTIONS = python_net_import('SMT.MastaAPI.Gears.LTCA', 'UseAdvancedLTCAOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('UseAdvancedLTCAOptions',)


class UseAdvancedLTCAOptions(Enum):
    '''UseAdvancedLTCAOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _USE_ADVANCED_LTCA_OPTIONS
    __hash__ = None

    YES = 0
    NO = 1
    SPECIFY_FOR_EACH_MESH = 2
