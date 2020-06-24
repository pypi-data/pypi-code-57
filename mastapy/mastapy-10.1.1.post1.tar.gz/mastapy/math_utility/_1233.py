'''_1233.py

TranslationRotation
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_TRANSLATION_ROTATION = python_net_import('SMT.MastaAPI.MathUtility', 'TranslationRotation')


__docformat__ = 'restructuredtext en'
__all__ = ('TranslationRotation',)


class TranslationRotation(Enum):
    '''TranslationRotation

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _TRANSLATION_ROTATION
    __hash__ = None

    TRANSLATION = 0
    ROTATION = 1
