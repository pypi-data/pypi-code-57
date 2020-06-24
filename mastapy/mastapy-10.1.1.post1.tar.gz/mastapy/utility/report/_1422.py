'''_1422.py

DefinitionBooleanCheckOptions
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_DEFINITION_BOOLEAN_CHECK_OPTIONS = python_net_import('SMT.MastaAPI.Utility.Report', 'DefinitionBooleanCheckOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('DefinitionBooleanCheckOptions',)


class DefinitionBooleanCheckOptions(Enum):
    '''DefinitionBooleanCheckOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _DEFINITION_BOOLEAN_CHECK_OPTIONS
    __hash__ = None

    NONE = 0
    INCLUDE_IF = 1
    EXCLUDE_IF = 2
