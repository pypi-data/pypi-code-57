'''_287.py

AccuracyGrades
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ACCURACY_GRADES = python_net_import('SMT.MastaAPI.Gears', 'AccuracyGrades')


__docformat__ = 'restructuredtext en'
__all__ = ('AccuracyGrades',)


class AccuracyGrades(_1.APIBase):
    '''AccuracyGrades

    This is a mastapy class.
    '''

    TYPE = _ACCURACY_GRADES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AccuracyGrades.TYPE'):
        super().__init__(instance_to_wrap)
