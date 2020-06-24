'''_4278.py

KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2078
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6144
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4277, _4276, _4275
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness',)


class KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness(_4275.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtAStiffness):
    '''KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2078.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2078.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6144.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6144.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_modal_analysis_at_a_stiffness(self) -> 'List[_4277.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidHypoidGearModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidHypoidGearsModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsModalAnalysisAtAStiffness, constructor.new(_4277.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtAStiffness))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_modal_analysis_at_a_stiffness(self) -> 'List[_4276.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidHypoidMeshesModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesModalAnalysisAtAStiffness, constructor.new(_4276.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtAStiffness))
        return value
