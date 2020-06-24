'''_2038.py

GearOrientations
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_GEAR_ORIENTATIONS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'GearOrientations')


__docformat__ = 'restructuredtext en'
__all__ = ('GearOrientations',)


class GearOrientations(Enum):
    '''GearOrientations

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _GEAR_ORIENTATIONS
    __hash__ = None

    LEFT = 0
    RIGHT = 1
