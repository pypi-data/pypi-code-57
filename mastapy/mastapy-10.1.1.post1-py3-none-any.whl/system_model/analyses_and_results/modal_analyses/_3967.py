'''_3967.py

StraightBevelDiffGearSetModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1982
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2359
from mastapy.system_model.analyses_and_results.system_deflections import _2358
from mastapy.system_model.analyses_and_results.modal_analyses import _3966, _3896, _3947
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'StraightBevelDiffGearSetModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetModalAnalysis',)


class StraightBevelDiffGearSetModalAnalysis(_3947.BevelGearSetModalAnalysis):
    '''StraightBevelDiffGearSetModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1982.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1982.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2359.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2359.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2358.StraightBevelDiffGearSetSystemDeflection':
        '''StraightBevelDiffGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2358.StraightBevelDiffGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def straight_bevel_diff_gears_modal_analysis(self) -> 'List[_3966.StraightBevelDiffGearModalAnalysis]':
        '''List[StraightBevelDiffGearModalAnalysis]: 'StraightBevelDiffGearsModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsModalAnalysis, constructor.new(_3966.StraightBevelDiffGearModalAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_modal_analysis(self) -> 'List[_3896.StraightBevelDiffGearMeshModalAnalysis]':
        '''List[StraightBevelDiffGearMeshModalAnalysis]: 'StraightBevelDiffMeshesModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesModalAnalysis, constructor.new(_3896.StraightBevelDiffGearMeshModalAnalysis))
        return value
