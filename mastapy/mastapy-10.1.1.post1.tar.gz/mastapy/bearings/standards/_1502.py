'''_1502.py

ISO2812007BallBearingDynamicEquivalentLoadCalculator
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ISO2812007_BALL_BEARING_DYNAMIC_EQUIVALENT_LOAD_CALCULATOR = python_net_import('SMT.MastaAPI.Bearings.Standards', 'ISO2812007BallBearingDynamicEquivalentLoadCalculator')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO2812007BallBearingDynamicEquivalentLoadCalculator',)


class ISO2812007BallBearingDynamicEquivalentLoadCalculator(_1.APIBase):
    '''ISO2812007BallBearingDynamicEquivalentLoadCalculator

    This is a mastapy class.
    '''

    TYPE = _ISO2812007_BALL_BEARING_DYNAMIC_EQUIVALENT_LOAD_CALCULATOR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ISO2812007BallBearingDynamicEquivalentLoadCalculator.TYPE'):
        super().__init__(instance_to_wrap)
