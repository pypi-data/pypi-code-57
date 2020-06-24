'''_269.py

ContactPairSlaveType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CONTACT_PAIR_SLAVE_TYPE = python_net_import('SMT.MastaAPI.FETools.VisToolsGlobal.VisToolsGlobalEnums', 'ContactPairSlaveType')


__docformat__ = 'restructuredtext en'
__all__ = ('ContactPairSlaveType',)


class ContactPairSlaveType(Enum):
    '''ContactPairSlaveType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _CONTACT_PAIR_SLAVE_TYPE
    __hash__ = None

    NONE = 0
    NODE = 1
    ELEMENT_EDGE = 2
    ELEMENT_FACE = 3
