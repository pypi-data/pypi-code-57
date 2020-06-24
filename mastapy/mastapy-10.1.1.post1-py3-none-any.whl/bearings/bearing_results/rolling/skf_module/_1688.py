'''_1688.py

AdjustedSpeed
'''


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.skf_module import _1689, _1705
from mastapy._internal.python_net import python_net_import

_ADJUSTED_SPEED = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'AdjustedSpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('AdjustedSpeed',)


class AdjustedSpeed(_1705.SKFCalculationResult):
    '''AdjustedSpeed

    This is a mastapy class.
    '''

    TYPE = _ADJUSTED_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AdjustedSpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def adjusted_reference_speed(self) -> 'float':
        '''float: 'AdjustedReferenceSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AdjustedReferenceSpeed

    @property
    def adjustment_factors(self) -> '_1689.AdjustmentFactors':
        '''AdjustmentFactors: 'AdjustmentFactors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1689.AdjustmentFactors)(self.wrapped.AdjustmentFactors) if self.wrapped.AdjustmentFactors else None
