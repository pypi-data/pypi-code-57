'''_6187.py

StraightBevelDiffGearSetLoadCase
'''


from typing import List

from mastapy.system_model.part_model.gears import _2085
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6185, _6186, _6064
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'StraightBevelDiffGearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetLoadCase',)


class StraightBevelDiffGearSetLoadCase(_6064.BevelGearSetLoadCase):
    '''StraightBevelDiffGearSetLoadCase

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2085.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2085.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_diff_gears_load_case(self) -> 'List[_6185.StraightBevelDiffGearLoadCase]':
        '''List[StraightBevelDiffGearLoadCase]: 'StraightBevelDiffGearsLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsLoadCase, constructor.new(_6185.StraightBevelDiffGearLoadCase))
        return value

    @property
    def straight_bevel_diff_meshes_load_case(self) -> 'List[_6186.StraightBevelDiffGearMeshLoadCase]':
        '''List[StraightBevelDiffGearMeshLoadCase]: 'StraightBevelDiffMeshesLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesLoadCase, constructor.new(_6186.StraightBevelDiffGearMeshLoadCase))
        return value
