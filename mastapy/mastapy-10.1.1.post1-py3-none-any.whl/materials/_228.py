'''_228.py

AGMAMaterialApplications
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_AGMA_MATERIAL_APPLICATIONS = python_net_import('SMT.MastaAPI.Materials', 'AGMAMaterialApplications')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAMaterialApplications',)


class AGMAMaterialApplications(Enum):
    '''AGMAMaterialApplications

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _AGMA_MATERIAL_APPLICATIONS
    __hash__ = None

    GENERAL_APPLICATION = 0
    CRITICAL_SERVICE = 1
