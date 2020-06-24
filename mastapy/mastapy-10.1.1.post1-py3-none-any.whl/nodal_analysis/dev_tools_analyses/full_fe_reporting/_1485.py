'''_1485.py

MaterialPropertiesReporting
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.fe_tools.enums import _969
from mastapy._internal.implicit import overridable
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MATERIAL_PROPERTIES_REPORTING = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'MaterialPropertiesReporting')


__docformat__ = 'restructuredtext en'
__all__ = ('MaterialPropertiesReporting',)


class MaterialPropertiesReporting(_0.APIBase):
    '''MaterialPropertiesReporting

    This is a mastapy class.
    '''

    TYPE = _MATERIAL_PROPERTIES_REPORTING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MaterialPropertiesReporting.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def id(self) -> 'int':
        '''int: 'ID' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ID

    @property
    def class_(self) -> '_969.MaterialPropertyClass':
        '''MaterialPropertyClass: 'Class' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.Class)
        return constructor.new(_969.MaterialPropertyClass)(value) if value else None

    @property
    def density(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Density' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Density) if self.wrapped.Density else None

    @density.setter
    def density(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.Density = value

    @property
    def modulus_of_elasticity(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ModulusOfElasticity' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ModulusOfElasticity) if self.wrapped.ModulusOfElasticity else None

    @modulus_of_elasticity.setter
    def modulus_of_elasticity(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ModulusOfElasticity = value

    @property
    def modulus_of_elasticity_xyz(self) -> 'str':
        '''str: 'ModulusOfElasticityXYZ' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ModulusOfElasticityXYZ

    @property
    def shear_modulus_xyz(self) -> 'str':
        '''str: 'ShearModulusXYZ' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShearModulusXYZ

    @property
    def elastic_stiffness_tensor_lower_triangle(self) -> 'str':
        '''str: 'ElasticStiffnessTensorLowerTriangle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ElasticStiffnessTensorLowerTriangle

    @property
    def poissons_ratio(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'PoissonsRatio' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.PoissonsRatio) if self.wrapped.PoissonsRatio else None

    @poissons_ratio.setter
    def poissons_ratio(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.PoissonsRatio = value

    @property
    def poissons_ratio_xyz(self) -> 'str':
        '''str: 'PoissonsRatioXYZ' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PoissonsRatioXYZ

    @property
    def thermal_expansion_coefficient(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ThermalExpansionCoefficient' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ThermalExpansionCoefficient) if self.wrapped.ThermalExpansionCoefficient else None

    @thermal_expansion_coefficient.setter
    def thermal_expansion_coefficient(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ThermalExpansionCoefficient = value

    @property
    def thermal_expansion_coefficient_xyz(self) -> 'str':
        '''str: 'ThermalExpansionCoefficientXYZ' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ThermalExpansionCoefficientXYZ

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result
