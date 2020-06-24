'''_4033.py

BoltParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _1910
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2266
from mastapy.system_model.analyses_and_results.system_deflections import _2153
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4035
from mastapy._internal.python_net import python_net_import

_BOLT_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'BoltParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltParametricStudyTool',)


class BoltParametricStudyTool(_4035.ComponentParametricStudyTool):
    '''BoltParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BOLT_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1910.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1910.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2266.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2266.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2153.BoltSystemDeflection]':
        '''List[BoltSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2153.BoltSystemDeflection))
        return value
