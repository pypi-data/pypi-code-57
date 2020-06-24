'''_1728.py

HypoidWindUpRemovalMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_HYPOID_WIND_UP_REMOVAL_METHOD = python_net_import('SMT.MastaAPI.SystemModel', 'HypoidWindUpRemovalMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidWindUpRemovalMethod',)


class HypoidWindUpRemovalMethod(Enum):
    '''HypoidWindUpRemovalMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _HYPOID_WIND_UP_REMOVAL_METHOD
    __hash__ = None

    INVARIANT_UNDER_RIGID_BODY_TRANSLATIONS_AND_ROTATIONS = 0
    ZERO_WIND_UP_SAE_750152 = 1
