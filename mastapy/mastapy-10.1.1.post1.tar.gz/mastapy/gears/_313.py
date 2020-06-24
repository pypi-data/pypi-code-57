'''_313.py

PlanetaryRatingLoadSharingOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_PLANETARY_RATING_LOAD_SHARING_OPTION = python_net_import('SMT.MastaAPI.Gears', 'PlanetaryRatingLoadSharingOption')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryRatingLoadSharingOption',)


class PlanetaryRatingLoadSharingOption(Enum):
    '''PlanetaryRatingLoadSharingOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _PLANETARY_RATING_LOAD_SHARING_OPTION
    __hash__ = None

    ANALYSIS_RESULTS = 0
    DISTRIBUTED_TO_GIVE_WORST_DAMAGE = 1
    SINGLE_PLANET_TAKING_PEAK_LOAD_OTHER_PLANETS_TAKING_EQUAL_LOAD = 2
