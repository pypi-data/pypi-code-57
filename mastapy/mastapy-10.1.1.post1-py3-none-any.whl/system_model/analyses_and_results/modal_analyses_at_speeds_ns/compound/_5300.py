'''_5300.py

BevelDifferentialGearSetCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _1981
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _5298, _5299, _5305
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5178
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'BevelDifferentialGearSetCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundModalAnalysesAtSpeeds',)


class BevelDifferentialGearSetCompoundModalAnalysesAtSpeeds(_5305.BevelGearSetCompoundModalAnalysesAtSpeeds):
    '''BevelDifferentialGearSetCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1981.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1981.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bevel_differential_gears_compound_modal_analyses_at_speeds(self) -> 'List[_5298.BevelDifferentialGearCompoundModalAnalysesAtSpeeds]':
        '''List[BevelDifferentialGearCompoundModalAnalysesAtSpeeds]: 'BevelDifferentialGearsCompoundModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundModalAnalysesAtSpeeds, constructor.new(_5298.BevelDifferentialGearCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def bevel_differential_meshes_compound_modal_analyses_at_speeds(self) -> 'List[_5299.BevelDifferentialGearMeshCompoundModalAnalysesAtSpeeds]':
        '''List[BevelDifferentialGearMeshCompoundModalAnalysesAtSpeeds]: 'BevelDifferentialMeshesCompoundModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundModalAnalysesAtSpeeds, constructor.new(_5299.BevelDifferentialGearMeshCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5178.BevelDifferentialGearSetModalAnalysesAtSpeeds]':
        '''List[BevelDifferentialGearSetModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5178.BevelDifferentialGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def assembly_modal_analyses_at_speeds_load_cases(self) -> 'List[_5178.BevelDifferentialGearSetModalAnalysesAtSpeeds]':
        '''List[BevelDifferentialGearSetModalAnalysesAtSpeeds]: 'AssemblyModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtSpeedsLoadCases, constructor.new(_5178.BevelDifferentialGearSetModalAnalysesAtSpeeds))
        return value
