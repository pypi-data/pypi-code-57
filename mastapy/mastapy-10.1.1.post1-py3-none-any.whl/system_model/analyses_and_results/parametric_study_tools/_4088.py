'''_4088.py

StraightBevelGearParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2006
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2361
from mastapy.system_model.analyses_and_results.system_deflections import _2360
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4066
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'StraightBevelGearParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearParametricStudyTool',)


class StraightBevelGearParametricStudyTool(_4066.BevelGearParametricStudyTool):
    '''StraightBevelGearParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2006.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2006.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2361.StraightBevelGearLoadCase':
        '''StraightBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2361.StraightBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2360.StraightBevelGearSystemDeflection]':
        '''List[StraightBevelGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2360.StraightBevelGearSystemDeflection))
        return value
