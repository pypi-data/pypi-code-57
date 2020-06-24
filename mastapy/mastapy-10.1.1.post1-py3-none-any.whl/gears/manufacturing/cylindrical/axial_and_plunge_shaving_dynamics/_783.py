'''_783.py

RollAngleRangeRelativeToAccuracy
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import _784
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ROLL_ANGLE_RANGE_RELATIVE_TO_ACCURACY = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'RollAngleRangeRelativeToAccuracy')


__docformat__ = 'restructuredtext en'
__all__ = ('RollAngleRangeRelativeToAccuracy',)


class RollAngleRangeRelativeToAccuracy(_1.APIBase):
    '''RollAngleRangeRelativeToAccuracy

    This is a mastapy class.
    '''

    TYPE = _ROLL_ANGLE_RANGE_RELATIVE_TO_ACCURACY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollAngleRangeRelativeToAccuracy.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def accuracy(self) -> 'str':
        '''str: 'Accuracy' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Accuracy

    @property
    def roll_angle_range(self) -> 'List[_784.RollAngleReportObject]':
        '''List[RollAngleReportObject]: 'RollAngleRange' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollAngleRange, constructor.new(_784.RollAngleReportObject))
        return value
