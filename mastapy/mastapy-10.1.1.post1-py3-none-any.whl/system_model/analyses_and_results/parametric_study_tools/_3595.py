'''_3595.py

WormGearParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2090
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6209
from mastapy.system_model.analyses_and_results.system_deflections import _2342
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3521
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'WormGearParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearParametricStudyTool',)


class WormGearParametricStudyTool(_3521.GearParametricStudyTool):
    '''WormGearParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2090.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2090.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6209.WormGearLoadCase':
        '''WormGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6209.WormGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2342.WormGearSystemDeflection]':
        '''List[WormGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2342.WormGearSystemDeflection))
        return value
