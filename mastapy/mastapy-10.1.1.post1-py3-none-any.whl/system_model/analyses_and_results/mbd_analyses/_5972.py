'''_5972.py

InputVelocityForRunUpProcessingType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_INPUT_VELOCITY_FOR_RUN_UP_PROCESSING_TYPE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'InputVelocityForRunUpProcessingType')


__docformat__ = 'restructuredtext en'
__all__ = ('InputVelocityForRunUpProcessingType',)


class InputVelocityForRunUpProcessingType(Enum):
    '''InputVelocityForRunUpProcessingType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _INPUT_VELOCITY_FOR_RUN_UP_PROCESSING_TYPE
    __hash__ = None

    NONE = 0
    FIT_POLYNOMIAL = 1
    FILTER = 2
