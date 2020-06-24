'''_420.py

KlingelnbergCycloPalloidHypoidGearRating
'''


from mastapy.gears.gear_designs.klingelnberg_hypoid import _440
from mastapy._internal import constructor
from mastapy.gears.rating.klingelnberg_conical import _422
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.KlingelnbergHypoid', 'KlingelnbergCycloPalloidHypoidGearRating')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearRating',)


class KlingelnbergCycloPalloidHypoidGearRating(_422.KlingelnbergCycloPalloidConicalGearRating):
    '''KlingelnbergCycloPalloidHypoidGearRating

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_RATING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_440.KlingelnbergCycloPalloidHypoidGearDesign':
        '''KlingelnbergCycloPalloidHypoidGearDesign: 'KlingelnbergCycloPalloidHypoidGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_440.KlingelnbergCycloPalloidHypoidGearDesign)(self.wrapped.KlingelnbergCycloPalloidHypoidGear) if self.wrapped.KlingelnbergCycloPalloidHypoidGear else None
