'''_1721.py

ComponentDampingOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_COMPONENT_DAMPING_OPTION = python_net_import('SMT.MastaAPI.SystemModel', 'ComponentDampingOption')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentDampingOption',)


class ComponentDampingOption(Enum):
    '''ComponentDampingOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _COMPONENT_DAMPING_OPTION
    __hash__ = None

    LOAD_CASE_GLOBAL_DAMPING = 0
    SPECIFIED = 1
