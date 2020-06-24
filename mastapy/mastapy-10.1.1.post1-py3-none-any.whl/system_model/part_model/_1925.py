'''_1925.py

LoadSharingModes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_LOAD_SHARING_MODES = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'LoadSharingModes')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadSharingModes',)


class LoadSharingModes(Enum):
    '''LoadSharingModes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _LOAD_SHARING_MODES
    __hash__ = None

    EQUAL = 0
    USER_DEFINED = 1
    AGMA_EMPIRICAL = 2
    GL = 3
