'''_4055.py

ShaftParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _1942
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2306
from mastapy.shafts import _42
from mastapy.system_model.analyses_and_results.system_deflections import _2066
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4031
from mastapy._internal.python_net import python_net_import

_SHAFT_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ShaftParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftParametricStudyTool',)


class ShaftParametricStudyTool(_4031.AbstractShaftOrHousingParametricStudyTool):
    '''ShaftParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _SHAFT_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1942.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1942.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2306.ShaftLoadCase':
        '''ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2306.ShaftLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def shaft_duty_cycle_results(self) -> 'List[_42.ShaftDamageResults]':
        '''List[ShaftDamageResults]: 'ShaftDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftDutyCycleResults, constructor.new(_42.ShaftDamageResults))
        return value

    @property
    def planetaries(self) -> 'List[ShaftParametricStudyTool]':
        '''List[ShaftParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftParametricStudyTool))
        return value

    @property
    def component_system_deflection_results(self) -> 'List[_2066.ShaftSystemDeflection]':
        '''List[ShaftSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2066.ShaftSystemDeflection))
        return value
