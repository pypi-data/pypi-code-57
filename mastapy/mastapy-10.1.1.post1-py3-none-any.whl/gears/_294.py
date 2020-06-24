'''_294.py

ContactRatioRequirements
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CONTACT_RATIO_REQUIREMENTS = python_net_import('SMT.MastaAPI.Gears', 'ContactRatioRequirements')


__docformat__ = 'restructuredtext en'
__all__ = ('ContactRatioRequirements',)


class ContactRatioRequirements(Enum):
    '''ContactRatioRequirements

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _CONTACT_RATIO_REQUIREMENTS
    __hash__ = None

    MAXIMISE = 0
    CLOSE_TO_INTEGER = 1
    IGNORE = 2
