'''_318.py

TESpecificationType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_TE_SPECIFICATION_TYPE = python_net_import('SMT.MastaAPI.Gears', 'TESpecificationType')


__docformat__ = 'restructuredtext en'
__all__ = ('TESpecificationType',)


class TESpecificationType(Enum):
    '''TESpecificationType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _TE_SPECIFICATION_TYPE
    __hash__ = None

    LINEAR = 0
    ANGULAR_WITH_RESPECT_TO_WHEEL = 1
