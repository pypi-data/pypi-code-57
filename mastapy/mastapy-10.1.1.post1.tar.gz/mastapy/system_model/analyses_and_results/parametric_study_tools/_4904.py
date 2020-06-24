'''_4904.py

DesignOfExperimentsVariableSetter
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4905
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_DESIGN_OF_EXPERIMENTS_VARIABLE_SETTER = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'DesignOfExperimentsVariableSetter')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignOfExperimentsVariableSetter',)


class DesignOfExperimentsVariableSetter(_1.APIBase):
    '''DesignOfExperimentsVariableSetter

    This is a mastapy class.
    '''

    TYPE = _DESIGN_OF_EXPERIMENTS_VARIABLE_SETTER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DesignOfExperimentsVariableSetter.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def number_of_values(self) -> 'int':
        '''int: 'NumberOfValues' is the original name of this property.'''

        return self.wrapped.NumberOfValues

    @number_of_values.setter
    def number_of_values(self, value: 'int'):
        self.wrapped.NumberOfValues = int(value) if value else 0

    @property
    def define_using_range(self) -> 'bool':
        '''bool: 'DefineUsingRange' is the original name of this property.'''

        return self.wrapped.DefineUsingRange

    @define_using_range.setter
    def define_using_range(self, value: 'bool'):
        self.wrapped.DefineUsingRange = bool(value) if value else False

    @property
    def value_specification_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_DoeValueSpecificationOption':
        '''enum_with_selected_value.EnumWithSelectedValue_DoeValueSpecificationOption: 'ValueSpecificationType' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_DoeValueSpecificationOption)(self.wrapped.ValueSpecificationType) if self.wrapped.ValueSpecificationType else None

    @value_specification_type.setter
    def value_specification_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_DoeValueSpecificationOption.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_DoeValueSpecificationOption.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DoeValueSpecificationOption.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.ValueSpecificationType = value

    @property
    def current_design_value(self) -> 'float':
        '''float: 'CurrentDesignValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CurrentDesignValue

    @property
    def start_value(self) -> 'float':
        '''float: 'StartValue' is the original name of this property.'''

        return self.wrapped.StartValue

    @start_value.setter
    def start_value(self, value: 'float'):
        self.wrapped.StartValue = float(value) if value else 0.0

    @property
    def end_value(self) -> 'float':
        '''float: 'EndValue' is the original name of this property.'''

        return self.wrapped.EndValue

    @end_value.setter
    def end_value(self, value: 'float'):
        self.wrapped.EndValue = float(value) if value else 0.0

    @property
    def value(self) -> 'float':
        '''float: 'Value' is the original name of this property.'''

        return self.wrapped.Value

    @value.setter
    def value(self, value: 'float'):
        self.wrapped.Value = float(value) if value else 0.0

    @property
    def integer_start_value(self) -> 'int':
        '''int: 'IntegerStartValue' is the original name of this property.'''

        return self.wrapped.IntegerStartValue

    @integer_start_value.setter
    def integer_start_value(self, value: 'int'):
        self.wrapped.IntegerStartValue = int(value) if value else 0

    @property
    def integer_end_value(self) -> 'int':
        '''int: 'IntegerEndValue' is the original name of this property.'''

        return self.wrapped.IntegerEndValue

    @integer_end_value.setter
    def integer_end_value(self, value: 'int'):
        self.wrapped.IntegerEndValue = int(value) if value else 0

    @property
    def integer_value(self) -> 'int':
        '''int: 'IntegerValue' is the original name of this property.'''

        return self.wrapped.IntegerValue

    @integer_value.setter
    def integer_value(self, value: 'int'):
        self.wrapped.IntegerValue = int(value) if value else 0

    @property
    def mean_value(self) -> 'float':
        '''float: 'MeanValue' is the original name of this property.'''

        return self.wrapped.MeanValue

    @mean_value.setter
    def mean_value(self, value: 'float'):
        self.wrapped.MeanValue = float(value) if value else 0.0

    @property
    def standard_deviation(self) -> 'float':
        '''float: 'StandardDeviation' is the original name of this property.'''

        return self.wrapped.StandardDeviation

    @standard_deviation.setter
    def standard_deviation(self, value: 'float'):
        self.wrapped.StandardDeviation = float(value) if value else 0.0

    @property
    def unit(self) -> 'str':
        '''str: 'Unit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Unit
