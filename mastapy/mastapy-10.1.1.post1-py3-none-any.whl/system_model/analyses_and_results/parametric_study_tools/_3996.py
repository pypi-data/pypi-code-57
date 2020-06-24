'''_3996.py

SynchroniserSleeveParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2025
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2204
from mastapy.system_model.analyses_and_results.system_deflections import _2203
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3995
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'SynchroniserSleeveParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveParametricStudyTool',)


class SynchroniserSleeveParametricStudyTool(_3995.SynchroniserPartParametricStudyTool):
    '''SynchroniserSleeveParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2025.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2025.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2204.SynchroniserSleeveLoadCase':
        '''SynchroniserSleeveLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2204.SynchroniserSleeveLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2203.SynchroniserSleeveSystemDeflection]':
        '''List[SynchroniserSleeveSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2203.SynchroniserSleeveSystemDeflection))
        return value
