'''_2358.py

StraightBevelDiffGearSetSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _1982
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2359
from mastapy.gears.rating.straight_bevel_diff import _399
from mastapy.system_model.analyses_and_results.system_deflections import _2356, _2237, _2150
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'StraightBevelDiffGearSetSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetSystemDeflection',)


class StraightBevelDiffGearSetSystemDeflection(_2150.BevelGearSetSystemDeflection):
    '''StraightBevelDiffGearSetSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetSystemDeflection.TYPE'):
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
    def rating(self) -> '_399.StraightBevelDiffGearSetRating':
        '''StraightBevelDiffGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_399.StraightBevelDiffGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_399.StraightBevelDiffGearSetRating':
        '''StraightBevelDiffGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_399.StraightBevelDiffGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def straight_bevel_diff_gears_system_deflection(self) -> 'List[_2356.StraightBevelDiffGearSystemDeflection]':
        '''List[StraightBevelDiffGearSystemDeflection]: 'StraightBevelDiffGearsSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsSystemDeflection, constructor.new(_2356.StraightBevelDiffGearSystemDeflection))
        return value

    @property
    def straight_bevel_diff_meshes_system_deflection(self) -> 'List[_2237.StraightBevelDiffGearMeshSystemDeflection]':
        '''List[StraightBevelDiffGearMeshSystemDeflection]: 'StraightBevelDiffMeshesSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesSystemDeflection, constructor.new(_2237.StraightBevelDiffGearMeshSystemDeflection))
        return value
