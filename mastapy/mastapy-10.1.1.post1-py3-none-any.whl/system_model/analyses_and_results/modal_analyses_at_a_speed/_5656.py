'''_5656.py

BevelDifferentialGearSetModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _1981
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2316
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5655, _5654, _5661
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'BevelDifferentialGearSetModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetModalAnalysisAtASpeed',)


class BevelDifferentialGearSetModalAnalysisAtASpeed(_5661.BevelGearSetModalAnalysisAtASpeed):
    '''BevelDifferentialGearSetModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1981.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2316.BevelDifferentialGearSetLoadCase':
        '''BevelDifferentialGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2316.BevelDifferentialGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bevel_differential_gears_modal_analysis_at_a_speed(self) -> 'List[_5655.BevelDifferentialGearModalAnalysisAtASpeed]':
        '''List[BevelDifferentialGearModalAnalysisAtASpeed]: 'BevelDifferentialGearsModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsModalAnalysisAtASpeed, constructor.new(_5655.BevelDifferentialGearModalAnalysisAtASpeed))
        return value

    @property
    def bevel_differential_meshes_modal_analysis_at_a_speed(self) -> 'List[_5654.BevelDifferentialGearMeshModalAnalysisAtASpeed]':
        '''List[BevelDifferentialGearMeshModalAnalysisAtASpeed]: 'BevelDifferentialMeshesModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesModalAnalysisAtASpeed, constructor.new(_5654.BevelDifferentialGearMeshModalAnalysisAtASpeed))
        return value
