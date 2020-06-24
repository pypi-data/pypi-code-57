'''_4062.py

BevelDifferentialGearParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2003
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2315
from mastapy.system_model.analyses_and_results.system_deflections import _2146
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4066
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'BevelDifferentialGearParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearParametricStudyTool',)


class BevelDifferentialGearParametricStudyTool(_4066.BevelGearParametricStudyTool):
    '''BevelDifferentialGearParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2003.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2003.BevelDifferentialGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2315.BevelDifferentialGearLoadCase':
        '''BevelDifferentialGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2315.BevelDifferentialGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2146.BevelDifferentialGearSystemDeflection]':
        '''List[BevelDifferentialGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2146.BevelDifferentialGearSystemDeflection))
        return value
