'''_3523.py

GuideDxfModelParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _1998
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6124
from mastapy.system_model.analyses_and_results.system_deflections import _2270
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3486
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'GuideDxfModelParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelParametricStudyTool',)


class GuideDxfModelParametricStudyTool(_3486.ComponentParametricStudyTool):
    '''GuideDxfModelParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1998.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1998.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6124.GuideDxfModelLoadCase':
        '''GuideDxfModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6124.GuideDxfModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2270.GuideDxfModelSystemDeflection]':
        '''List[GuideDxfModelSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2270.GuideDxfModelSystemDeflection))
        return value
