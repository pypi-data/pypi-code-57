'''_1212.py

AcousticWeighting
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ACOUSTIC_WEIGHTING = python_net_import('SMT.MastaAPI.MathUtility', 'AcousticWeighting')


__docformat__ = 'restructuredtext en'
__all__ = ('AcousticWeighting',)


class AcousticWeighting(Enum):
    '''AcousticWeighting

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ACOUSTIC_WEIGHTING
    __hash__ = None

    NONE = 0
    AWEIGHTING = 1
    BWEIGHTING = 2
    CWEIGHTING = 3
    DWEIGHTING = 4
