'''_1603.py

PlainOilFedJournalBearing
'''


from mastapy.bearings import _1476
from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_designs.fluid_film import (
    _1707, _1708, _1709, _1717
)
from mastapy._internal.python_net import python_net_import

_PLAIN_OIL_FED_JOURNAL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm', 'PlainOilFedJournalBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('PlainOilFedJournalBearing',)


class PlainOilFedJournalBearing(_1717.PlainJournalBearing):
    '''PlainOilFedJournalBearing

    This is a mastapy class.
    '''

    TYPE = _PLAIN_OIL_FED_JOURNAL_BEARING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlainOilFedJournalBearing.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def feed_type(self) -> '_1476.JournalOilFeedType':
        '''JournalOilFeedType: 'FeedType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.FeedType)
        return constructor.new(_1476.JournalOilFeedType)(value) if value else None

    @feed_type.setter
    def feed_type(self, value: '_1476.JournalOilFeedType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FeedType = value

    @property
    def land_width(self) -> 'float':
        '''float: 'LandWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LandWidth

    @property
    def axial_groove_oil_feed(self) -> '_1707.AxialGrooveJournalBearing':
        '''AxialGrooveJournalBearing: 'AxialGrooveOilFeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1707.AxialGrooveJournalBearing)(self.wrapped.AxialGrooveOilFeed) if self.wrapped.AxialGrooveOilFeed else None

    @property
    def axial_hole_oil_feed(self) -> '_1708.AxialHoleJournalBearing':
        '''AxialHoleJournalBearing: 'AxialHoleOilFeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1708.AxialHoleJournalBearing)(self.wrapped.AxialHoleOilFeed) if self.wrapped.AxialHoleOilFeed else None

    @property
    def circumferential_groove_oil_feed(self) -> '_1709.CircumferentialFeedJournalBearing':
        '''CircumferentialFeedJournalBearing: 'CircumferentialGrooveOilFeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1709.CircumferentialFeedJournalBearing)(self.wrapped.CircumferentialGrooveOilFeed) if self.wrapped.CircumferentialGrooveOilFeed else None
