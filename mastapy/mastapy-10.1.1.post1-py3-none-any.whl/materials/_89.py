'''_89.py

SoundPressureEnclosureType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SOUND_PRESSURE_ENCLOSURE_TYPE = python_net_import('SMT.MastaAPI.Materials', 'SoundPressureEnclosureType')


__docformat__ = 'restructuredtext en'
__all__ = ('SoundPressureEnclosureType',)


class SoundPressureEnclosureType(Enum):
    '''SoundPressureEnclosureType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _SOUND_PRESSURE_ENCLOSURE_TYPE

    __hash__ = None

    FREE_FIELD = 0
    FREE_FIELD_OVER_REFLECTING_PLANE = 1
