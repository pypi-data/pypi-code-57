'''_1380.py

ITDesignation
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_IT_DESIGNATION = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'ITDesignation')


__docformat__ = 'restructuredtext en'
__all__ = ('ITDesignation',)


class ITDesignation(Enum):
    '''ITDesignation

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _IT_DESIGNATION
    __hash__ = None

    IT1 = 0
    IT2 = 1
    IT3 = 2
    IT4 = 3
    IT5 = 4
    IT6 = 5
    IT7 = 6
    IT8 = 7
    IT9 = 8
    IT10 = 9
    IT11 = 10
    IT12 = 11
    IT13 = 12
    IT14 = 13
