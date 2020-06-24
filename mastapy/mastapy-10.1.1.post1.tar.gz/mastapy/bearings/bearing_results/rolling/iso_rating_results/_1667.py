'''_1667.py

ISOResults
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ISO_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.IsoRatingResults', 'ISOResults')


__docformat__ = 'restructuredtext en'
__all__ = ('ISOResults',)


class ISOResults(_1.APIBase):
    '''ISOResults

    This is a mastapy class.
    '''

    TYPE = _ISO_RESULTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ISOResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def life_modification_factor_for_reliability(self) -> 'float':
        '''float: 'LifeModificationFactorForReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LifeModificationFactorForReliability
