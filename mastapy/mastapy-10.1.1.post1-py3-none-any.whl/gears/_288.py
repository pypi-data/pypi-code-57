'''_288.py

AGMAToleranceStandard
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_AGMA_TOLERANCE_STANDARD = python_net_import('SMT.MastaAPI.Gears', 'AGMAToleranceStandard')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAToleranceStandard',)


class AGMAToleranceStandard(Enum):
    '''AGMAToleranceStandard

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _AGMA_TOLERANCE_STANDARD
    __hash__ = None

    AGMA_20151A01 = 0
    AGMA_2000A88 = 1
    ANSIAGMA_ISO_13281B14 = 2
