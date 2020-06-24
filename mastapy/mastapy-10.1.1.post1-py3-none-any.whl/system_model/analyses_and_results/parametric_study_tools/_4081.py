'''_4081.py

KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2013
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2348
from mastapy.system_model.analyses_and_results.system_deflections import _2347
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4077
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool',)


class KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool(_4077.KlingelnbergCycloPalloidConicalGearParametricStudyTool):
    '''KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2013.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2013.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2348.KlingelnbergCycloPalloidSpiralBevelGearLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2348.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2347.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2347.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection))
        return value
