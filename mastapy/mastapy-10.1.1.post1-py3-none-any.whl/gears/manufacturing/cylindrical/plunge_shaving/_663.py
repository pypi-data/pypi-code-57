'''_663.py

ShaverPointOfInterest
'''


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _660
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SHAVER_POINT_OF_INTEREST = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving', 'ShaverPointOfInterest')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaverPointOfInterest',)


class ShaverPointOfInterest(_1.APIBase):
    '''ShaverPointOfInterest

    This is a mastapy class.
    '''

    TYPE = _SHAVER_POINT_OF_INTEREST
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaverPointOfInterest.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def shaver_radius(self) -> 'float':
        '''float: 'ShaverRadius' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaverRadius

    @property
    def error(self) -> 'float':
        '''float: 'Error' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Error

    @property
    def shaver_z_plane(self) -> 'float':
        '''float: 'ShaverZPlane' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaverZPlane

    @property
    def point_of_interest_on_the_gear(self) -> '_660.PointOfInterest':
        '''PointOfInterest: 'PointOfInterestOnTheGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_660.PointOfInterest)(self.wrapped.PointOfInterestOnTheGear) if self.wrapped.PointOfInterestOnTheGear else None
