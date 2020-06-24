'''_965.py

ContactPairMasterType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CONTACT_PAIR_MASTER_TYPE = python_net_import('SMT.MastaAPI.FETools.VisToolsGlobal.VisToolsGlobalEnums', 'ContactPairMasterType')


__docformat__ = 'restructuredtext en'
__all__ = ('ContactPairMasterType',)


class ContactPairMasterType(Enum):
    '''ContactPairMasterType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _CONTACT_PAIR_MASTER_TYPE

    __hash__ = None

    ELEMENT_EDGE = 2
    ELEMENT_FACE = 3
    ANALYTIC_SURFACE = 2660
