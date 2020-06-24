'''_186.py

FEModelSetupViewType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_FE_MODEL_SETUP_VIEW_TYPE = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses', 'FEModelSetupViewType')


__docformat__ = 'restructuredtext en'
__all__ = ('FEModelSetupViewType',)


class FEModelSetupViewType(Enum):
    '''FEModelSetupViewType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _FE_MODEL_SETUP_VIEW_TYPE
    __hash__ = None

    CURRENT_SETUP = 0
    REDUCTION_RESULT = 1
