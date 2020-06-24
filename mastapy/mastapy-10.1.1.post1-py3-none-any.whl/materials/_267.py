'''_267.py

QualityGrade
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_QUALITY_GRADE = python_net_import('SMT.MastaAPI.Materials', 'QualityGrade')


__docformat__ = 'restructuredtext en'
__all__ = ('QualityGrade',)


class QualityGrade(Enum):
    '''QualityGrade

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _QUALITY_GRADE
    __hash__ = None

    ML = 0
    MQ = 1
    ME = 2
