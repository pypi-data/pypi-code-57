'''_1589.py

FourPointContactBallBearing
'''


from mastapy.bearings.bearing_designs.rolling import _1693
from mastapy._internal.python_net import python_net_import

_FOUR_POINT_CONTACT_BALL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'FourPointContactBallBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('FourPointContactBallBearing',)


class FourPointContactBallBearing(_1693.MultiPointContactBallBearing):
    '''FourPointContactBallBearing

    This is a mastapy class.
    '''

    TYPE = _FOUR_POINT_CONTACT_BALL_BEARING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FourPointContactBallBearing.TYPE'):
        super().__init__(instance_to_wrap)
