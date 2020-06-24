'''_223.py

AcousticRadiationEfficiency
'''


from mastapy.materials import _226
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ACOUSTIC_RADIATION_EFFICIENCY = python_net_import('SMT.MastaAPI.Materials', 'AcousticRadiationEfficiency')


__docformat__ = 'restructuredtext en'
__all__ = ('AcousticRadiationEfficiency',)


class AcousticRadiationEfficiency(_1.APIBase):
    '''AcousticRadiationEfficiency

    This is a mastapy class.
    '''

    TYPE = _ACOUSTIC_RADIATION_EFFICIENCY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AcousticRadiationEfficiency.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def input_type(self) -> '_226.AcousticRadiationEfficiencyInputType':
        '''AcousticRadiationEfficiencyInputType: 'InputType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.InputType)
        return constructor.new(_226.AcousticRadiationEfficiencyInputType)(value) if value else None

    @input_type.setter
    def input_type(self, value: '_226.AcousticRadiationEfficiencyInputType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.InputType = value

    @property
    def knee_frequency(self) -> 'float':
        '''float: 'KneeFrequency' is the original name of this property.'''

        return self.wrapped.KneeFrequency

    @knee_frequency.setter
    def knee_frequency(self, value: 'float'):
        self.wrapped.KneeFrequency = float(value) if value else 0.0

    @property
    def low_frequency_power(self) -> 'float':
        '''float: 'LowFrequencyPower' is the original name of this property.'''

        return self.wrapped.LowFrequencyPower

    @low_frequency_power.setter
    def low_frequency_power(self, value: 'float'):
        self.wrapped.LowFrequencyPower = float(value) if value else 0.0
