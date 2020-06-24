'''_679.py

ManufacturedQualityGrade
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_MANUFACTURED_QUALITY_GRADE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'ManufacturedQualityGrade')


__docformat__ = 'restructuredtext en'
__all__ = ('ManufacturedQualityGrade',)


class ManufacturedQualityGrade(_1.APIBase):
    '''ManufacturedQualityGrade

    This is a mastapy class.
    '''

    TYPE = _MANUFACTURED_QUALITY_GRADE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ManufacturedQualityGrade.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def designed(self) -> 'float':
        '''float: 'Designed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Designed

    @property
    def obtained(self) -> 'float':
        '''float: 'Obtained' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Obtained

    @property
    def deviation(self) -> 'float':
        '''float: 'Deviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Deviation

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name
