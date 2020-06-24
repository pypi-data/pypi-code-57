'''_1001.py

Micropitting
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.gears import _310
from mastapy.utility import _334
from mastapy._internal.python_net import python_net_import

_MICROPITTING = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'Micropitting')


__docformat__ = 'restructuredtext en'
__all__ = ('Micropitting',)


class Micropitting(_334.IndependentReportablePropertiesBase['Micropitting']):
    '''Micropitting

    This is a mastapy class.
    '''

    TYPE = _MICROPITTING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'Micropitting.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def estimate_bulk_temperature(self) -> 'bool':
        '''bool: 'EstimateBulkTemperature' is the original name of this property.'''

        return self.wrapped.EstimateBulkTemperature

    @estimate_bulk_temperature.setter
    def estimate_bulk_temperature(self, value: 'bool'):
        self.wrapped.EstimateBulkTemperature = bool(value) if value else False

    @property
    def method_a_coefficient_of_friction_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod':
        '''enum_with_selected_value.EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod: 'MethodACoefficientOfFrictionMethod' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod)(self.wrapped.MethodACoefficientOfFrictionMethod) if self.wrapped.MethodACoefficientOfFrictionMethod else None

    @method_a_coefficient_of_friction_method.setter
    def method_a_coefficient_of_friction_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.MethodACoefficientOfFrictionMethod = value
