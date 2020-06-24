'''_784.py

RollAngleReportObject
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ROLL_ANGLE_REPORT_OBJECT = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'RollAngleReportObject')


__docformat__ = 'restructuredtext en'
__all__ = ('RollAngleReportObject',)


class RollAngleReportObject(_1.APIBase):
    '''RollAngleReportObject

    This is a mastapy class.
    '''

    TYPE = _ROLL_ANGLE_REPORT_OBJECT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollAngleReportObject.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def required_roll_angle_range(self) -> 'float':
        '''float: 'RequiredRollAngleRange' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RequiredRollAngleRange

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name
