'''_1515.py

UserSpecifiedProfilePoint
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_USER_SPECIFIED_PROFILE_POINT = python_net_import('SMT.MastaAPI.Bearings.RollerBearingProfiles', 'UserSpecifiedProfilePoint')


__docformat__ = 'restructuredtext en'
__all__ = ('UserSpecifiedProfilePoint',)


class UserSpecifiedProfilePoint(_1.APIBase):
    '''UserSpecifiedProfilePoint

    This is a mastapy class.
    '''

    TYPE = _USER_SPECIFIED_PROFILE_POINT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'UserSpecifiedProfilePoint.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def position(self) -> 'float':
        '''float: 'Position' is the original name of this property.'''

        return self.wrapped.Position

    @position.setter
    def position(self, value: 'float'):
        self.wrapped.Position = float(value) if value else 0.0

    @property
    def deviation(self) -> 'float':
        '''float: 'Deviation' is the original name of this property.'''

        return self.wrapped.Deviation

    @deviation.setter
    def deviation(self, value: 'float'):
        self.wrapped.Deviation = float(value) if value else 0.0
