'''_6251.py

WindTurbineCertificationReport
'''


from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.analyses_and_results.static_loads import _2057
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.load_case_groups import _2058
from mastapy.system_model.part_model import _1935
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2598
from mastapy.system_model.analyses_and_results.system_deflections import _2298
from mastapy.system_model.analyses_and_results.flexible_pin_analyses import _6243
from mastapy._internal.python_net import python_net_import

_WIND_TURBINE_CERTIFICATION_REPORT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses', 'WindTurbineCertificationReport')


__docformat__ = 'restructuredtext en'
__all__ = ('WindTurbineCertificationReport',)


class WindTurbineCertificationReport(_6243.CombinationAnalysis):
    '''WindTurbineCertificationReport

    This is a mastapy class.
    '''

    TYPE = _WIND_TURBINE_CERTIFICATION_REPORT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WindTurbineCertificationReport.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def extreme_load_case(self) -> 'list_with_selected_item.ListWithSelectedItem_StaticLoadCase':
        '''list_with_selected_item.ListWithSelectedItem_StaticLoadCase: 'ExtremeLoadCase' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_StaticLoadCase)(self.wrapped.ExtremeLoadCase) if self.wrapped.ExtremeLoadCase else None

    @extreme_load_case.setter
    def extreme_load_case(self, value: 'list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_StaticLoadCase.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.ExtremeLoadCase = value

    @property
    def ldd(self) -> 'list_with_selected_item.ListWithSelectedItem_DutyCycle':
        '''list_with_selected_item.ListWithSelectedItem_DutyCycle: 'LDD' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_DutyCycle)(self.wrapped.LDD) if self.wrapped.LDD else None

    @ldd.setter
    def ldd(self, value: 'list_with_selected_item.ListWithSelectedItem_DutyCycle.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_DutyCycle.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_DutyCycle.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.LDD = value

    @property
    def nominal_load_case(self) -> 'list_with_selected_item.ListWithSelectedItem_StaticLoadCase':
        '''list_with_selected_item.ListWithSelectedItem_StaticLoadCase: 'NominalLoadCase' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_StaticLoadCase)(self.wrapped.NominalLoadCase) if self.wrapped.NominalLoadCase else None

    @nominal_load_case.setter
    def nominal_load_case(self, value: 'list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_StaticLoadCase.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.NominalLoadCase = value

    @property
    def design(self) -> '_1935.RootAssembly':
        '''RootAssembly: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1935.RootAssembly)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def ldd_static_analysis(self) -> '_2598.RootAssemblyCompoundSystemDeflection':
        '''RootAssemblyCompoundSystemDeflection: 'LDDStaticAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2598.RootAssemblyCompoundSystemDeflection)(self.wrapped.LDDStaticAnalysis) if self.wrapped.LDDStaticAnalysis else None

    @property
    def nominal_load_case_static_analysis(self) -> '_2298.RootAssemblySystemDeflection':
        '''RootAssemblySystemDeflection: 'NominalLoadCaseStaticAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2298.RootAssemblySystemDeflection)(self.wrapped.NominalLoadCaseStaticAnalysis) if self.wrapped.NominalLoadCaseStaticAnalysis else None

    @property
    def extreme_load_case_static_analysis(self) -> '_2298.RootAssemblySystemDeflection':
        '''RootAssemblySystemDeflection: 'ExtremeLoadCaseStaticAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2298.RootAssemblySystemDeflection)(self.wrapped.ExtremeLoadCaseStaticAnalysis) if self.wrapped.ExtremeLoadCaseStaticAnalysis else None
