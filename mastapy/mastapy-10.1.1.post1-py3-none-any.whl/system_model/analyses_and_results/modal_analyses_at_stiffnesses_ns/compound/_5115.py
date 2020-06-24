'''_5115.py

KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _1985
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _5113, _5114, _5109
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _4993
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtStiffnesses',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtStiffnesses(_5109.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysesAtStiffnesses):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_modal_analyses_at_stiffnesses(self) -> 'List[_5113.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysesAtStiffnesses]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysesAtStiffnesses]: 'KlingelnbergCycloPalloidSpiralBevelGearsCompoundModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCompoundModalAnalysesAtStiffnesses, constructor.new(_5113.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_modal_analyses_at_stiffnesses(self) -> 'List[_5114.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysesAtStiffnesses]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysesAtStiffnesses]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCompoundModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCompoundModalAnalysesAtStiffnesses, constructor.new(_5114.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4993.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4993.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def assembly_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_4993.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses]: 'AssemblyModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtStiffnessesLoadCases, constructor.new(_4993.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses))
        return value
