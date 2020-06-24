'''_4049.py

PointLoadParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _1933
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2295
from mastapy.system_model.analyses_and_results.system_deflections import _2294
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4054
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'PointLoadParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadParametricStudyTool',)


class PointLoadParametricStudyTool(_4054.VirtualComponentParametricStudyTool):
    '''PointLoadParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1933.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1933.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2295.PointLoadLoadCase':
        '''PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2295.PointLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2294.PointLoadSystemDeflection]':
        '''List[PointLoadSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2294.PointLoadSystemDeflection))
        return value
