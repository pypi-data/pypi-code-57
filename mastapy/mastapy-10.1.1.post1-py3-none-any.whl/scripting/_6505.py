'''_6505.py

MastaPropertyAttribute
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.units_and_measurements import _6502
from mastapy._internal.python_net import python_net_import

_MASTA_PROPERTY_ATTRIBUTE = python_net_import('SMT.MastaAPIUtility.Scripting', 'MastaPropertyAttribute')


__docformat__ = 'restructuredtext en'
__all__ = ('MastaPropertyAttribute',)


class MastaPropertyAttribute:
    '''MastaPropertyAttribute

    This is a mastapy class.
    '''

    TYPE = _MASTA_PROPERTY_ATTRIBUTE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MastaPropertyAttribute.TYPE'):
        self.wrapped = instance_to_wrap

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def description(self) -> 'str':
        '''str: 'Description' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Description

    @property
    def symbol(self) -> 'str':
        '''str: 'Symbol' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Symbol

    @property
    def measurement(self) -> '_6502.MeasurementType':
        '''MeasurementType: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.Measurement)
        return constructor.new(_6502.MeasurementType)(value) if value else None
