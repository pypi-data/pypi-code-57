'''_1962.py

HousedOrMounted
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_HOUSED_OR_MOUNTED = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'HousedOrMounted')


__docformat__ = 'restructuredtext en'
__all__ = ('HousedOrMounted',)


class HousedOrMounted(Enum):
    '''HousedOrMounted

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _HOUSED_OR_MOUNTED
    __hash__ = None

    HOUSED = 0
    MOUNTED = 1
