'''_6101.py

ElectricMachineDetail
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.utility.enums import _1335
from mastapy.utility.databases import _1342
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ElectricMachineDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineDetail',)


class ElectricMachineDetail(_1342.NamedDatabaseItem):
    '''ElectricMachineDetail

    This is a mastapy class.
    '''

    TYPE = _ELECTRIC_MACHINE_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElectricMachineDetail.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def default_number_of_slots(self) -> 'int':
        '''int: 'DefaultNumberOfSlots' is the original name of this property.'''

        return self.wrapped.DefaultNumberOfSlots

    @default_number_of_slots.setter
    def default_number_of_slots(self, value: 'int'):
        self.wrapped.DefaultNumberOfSlots = int(value) if value else 0

    @property
    def default_inner_diameter_of_stator_teeth(self) -> 'float':
        '''float: 'DefaultInnerDiameterOfStatorTeeth' is the original name of this property.'''

        return self.wrapped.DefaultInnerDiameterOfStatorTeeth

    @default_inner_diameter_of_stator_teeth.setter
    def default_inner_diameter_of_stator_teeth(self, value: 'float'):
        self.wrapped.DefaultInnerDiameterOfStatorTeeth = float(value) if value else 0.0

    @property
    def default_effective_length(self) -> 'float':
        '''float: 'DefaultEffectiveLength' is the original name of this property.'''

        return self.wrapped.DefaultEffectiveLength

    @default_effective_length.setter
    def default_effective_length(self, value: 'float'):
        self.wrapped.DefaultEffectiveLength = float(value) if value else 0.0

    @property
    def flow_rate_specification_method(self) -> '_1335.PropertySpecificationMethod':
        '''PropertySpecificationMethod: 'FlowRateSpecificationMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.FlowRateSpecificationMethod)
        return constructor.new(_1335.PropertySpecificationMethod)(value) if value else None

    @flow_rate_specification_method.setter
    def flow_rate_specification_method(self, value: '_1335.PropertySpecificationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FlowRateSpecificationMethod = value
