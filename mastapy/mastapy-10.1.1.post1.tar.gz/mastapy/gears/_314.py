'''_314.py

QualityGradeTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_QUALITY_GRADE_TYPES = python_net_import('SMT.MastaAPI.Gears', 'QualityGradeTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('QualityGradeTypes',)


class QualityGradeTypes(Enum):
    '''QualityGradeTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _QUALITY_GRADE_TYPES
    __hash__ = None

    AGMA_NEW = 0
    AGMA_OLD = 1
