'''_1841.py

BearingNodeAlignmentOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_BEARING_NODE_ALIGNMENT_OPTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'BearingNodeAlignmentOption')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingNodeAlignmentOption',)


class BearingNodeAlignmentOption(Enum):
    '''BearingNodeAlignmentOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _BEARING_NODE_ALIGNMENT_OPTION
    __hash__ = None

    CENTRE_OF_BEARING = 0
    CENTRE_OF_RACE = 1
