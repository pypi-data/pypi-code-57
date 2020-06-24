'''_1912.py

AngleSource
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ANGLE_SOURCE = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'AngleSource')


__docformat__ = 'restructuredtext en'
__all__ = ('AngleSource',)


class AngleSource(Enum):
    '''AngleSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _ANGLE_SOURCE

    __hash__ = None

    SPECIFIED_VALUE = 0
    DERIVED = 1
    INDEX = 2
