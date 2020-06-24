'''_1722.py

ConceptCouplingSpeedRatioSpecificationMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_SPEED_RATIO_SPECIFICATION_METHOD = python_net_import('SMT.MastaAPI.SystemModel', 'ConceptCouplingSpeedRatioSpecificationMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingSpeedRatioSpecificationMethod',)


class ConceptCouplingSpeedRatioSpecificationMethod(Enum):
    '''ConceptCouplingSpeedRatioSpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _CONCEPT_COUPLING_SPEED_RATIO_SPECIFICATION_METHOD
    __hash__ = None

    FIXED = 0
    VARYING_WITH_TIME = 1
    PID_CONTROL = 2
