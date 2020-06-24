'''_136.py

ISOToleranceStandard
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ISO_TOLERANCE_STANDARD = python_net_import('SMT.MastaAPI.Gears', 'ISOToleranceStandard')


__docformat__ = 'restructuredtext en'
__all__ = ('ISOToleranceStandard',)


class ISOToleranceStandard(Enum):
    '''ISOToleranceStandard

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _ISO_TOLERANCE_STANDARD

    __hash__ = None

    ISO_132811995EISO_132821997E = 0
    ISO_132812013EISO_132821997E = 1
