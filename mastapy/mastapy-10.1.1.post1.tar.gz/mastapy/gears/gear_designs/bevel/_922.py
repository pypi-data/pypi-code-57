'''_922.py

PrimeMoverCharacteristicGleason
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_PRIME_MOVER_CHARACTERISTIC_GLEASON = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Bevel', 'PrimeMoverCharacteristicGleason')


__docformat__ = 'restructuredtext en'
__all__ = ('PrimeMoverCharacteristicGleason',)


class PrimeMoverCharacteristicGleason(Enum):
    '''PrimeMoverCharacteristicGleason

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _PRIME_MOVER_CHARACTERISTIC_GLEASON

    __hash__ = None

    UNIFORM = 0
    LIGHT_SHOCK = 1
    MEDIUM_SHOCK = 2
