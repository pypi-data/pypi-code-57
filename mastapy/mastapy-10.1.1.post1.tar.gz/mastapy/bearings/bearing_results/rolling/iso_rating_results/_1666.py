'''_1666.py

ISO762006Results
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ISO762006_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.IsoRatingResults', 'ISO762006Results')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO762006Results',)


class ISO762006Results(_1.APIBase):
    '''ISO762006Results

    This is a mastapy class.
    '''

    TYPE = _ISO762006_RESULTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ISO762006Results.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def static_equivalent_load(self) -> 'float':
        '''float: 'StaticEquivalentLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StaticEquivalentLoad

    @property
    def safety_factor(self) -> 'float':
        '''float: 'SafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SafetyFactor

    @property
    def recommended_maximum_element_normal_stress(self) -> 'float':
        '''float: 'RecommendedMaximumElementNormalStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RecommendedMaximumElementNormalStress

    @property
    def static_axial_load_factor(self) -> 'float':
        '''float: 'StaticAxialLoadFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StaticAxialLoadFactor

    @property
    def static_radial_load_factor(self) -> 'float':
        '''float: 'StaticRadialLoadFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StaticRadialLoadFactor
