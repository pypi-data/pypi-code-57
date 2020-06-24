'''_6220.py

TEExcitationType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_TE_EXCITATION_TYPE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'TEExcitationType')


__docformat__ = 'restructuredtext en'
__all__ = ('TEExcitationType',)


class TEExcitationType(Enum):
    '''TEExcitationType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _TE_EXCITATION_TYPE
    __hash__ = None

    TRANSMISSION_ERROR = 0
    MISALIGNMENT = 1
