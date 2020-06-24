'''_342.py

GearSingleFlankRating
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating', 'GearSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSingleFlankRating',)


class GearSingleFlankRating(_1.APIBase):
    '''GearSingleFlankRating

    This is a mastapy class.
    '''

    TYPE = _GEAR_SINGLE_FLANK_RATING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def torque(self) -> 'float':
        '''float: 'Torque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Torque

    @property
    def rotation_speed(self) -> 'float':
        '''float: 'RotationSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RotationSpeed

    @property
    def power(self) -> 'float':
        '''float: 'Power' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Power

    @property
    def duration(self) -> 'float':
        '''float: 'Duration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Duration

    @property
    def number_of_load_cycles(self) -> 'float':
        '''float: 'NumberOfLoadCycles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfLoadCycles
