'''_1692.py

Frequencies
'''


from mastapy.bearings.bearing_results.rolling.skf_module import _1704, _1693, _1705
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_FREQUENCIES = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'Frequencies')


__docformat__ = 'restructuredtext en'
__all__ = ('Frequencies',)


class Frequencies(_1705.SKFCalculationResult):
    '''Frequencies

    This is a mastapy class.
    '''

    TYPE = _FREQUENCIES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Frequencies.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def rotational_frequency(self) -> '_1704.RotationalFrequency':
        '''RotationalFrequency: 'RotationalFrequency' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1704.RotationalFrequency)(self.wrapped.RotationalFrequency) if self.wrapped.RotationalFrequency else None

    @property
    def frequency_of_over_rolling(self) -> '_1693.FrequencyOfOverRolling':
        '''FrequencyOfOverRolling: 'FrequencyOfOverRolling' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1693.FrequencyOfOverRolling)(self.wrapped.FrequencyOfOverRolling) if self.wrapped.FrequencyOfOverRolling else None
