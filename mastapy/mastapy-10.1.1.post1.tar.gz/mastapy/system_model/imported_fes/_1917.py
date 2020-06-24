'''_1917.py

BearingRacePosition
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_BEARING_RACE_POSITION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'BearingRacePosition')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingRacePosition',)


class BearingRacePosition(Enum):
    '''BearingRacePosition

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _BEARING_RACE_POSITION

    __hash__ = None

    INNER = 0
    OUTER = 1
