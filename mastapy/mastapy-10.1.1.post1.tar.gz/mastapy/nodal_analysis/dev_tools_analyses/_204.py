'''_204.py

MassMatrixType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MASS_MATRIX_TYPE = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses', 'MassMatrixType')


__docformat__ = 'restructuredtext en'
__all__ = ('MassMatrixType',)


class MassMatrixType(Enum):
    '''MassMatrixType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _MASS_MATRIX_TYPE
    __hash__ = None

    DIAGONAL = 0
    CONSISTENT = 1
