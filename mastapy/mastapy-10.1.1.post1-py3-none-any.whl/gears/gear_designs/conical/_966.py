'''_966.py

ActiveConicalFlank
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ACTIVE_CONICAL_FLANK = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical', 'ActiveConicalFlank')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveConicalFlank',)


class ActiveConicalFlank(Enum):
    '''ActiveConicalFlank

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ACTIVE_CONICAL_FLANK
    __hash__ = None

    DRIVE = 0
    COAST = 1
