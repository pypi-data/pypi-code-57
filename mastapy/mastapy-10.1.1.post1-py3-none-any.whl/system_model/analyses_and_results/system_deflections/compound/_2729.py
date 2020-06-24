'''_2729.py

StraightBevelDiffGearCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2014
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2356
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2648
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'StraightBevelDiffGearCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearCompoundSystemDeflection',)


class StraightBevelDiffGearCompoundSystemDeflection(_2648.BevelGearCompoundSystemDeflection):
    '''StraightBevelDiffGearCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2014.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2014.StraightBevelDiffGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2356.StraightBevelDiffGearSystemDeflection]':
        '''List[StraightBevelDiffGearSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2356.StraightBevelDiffGearSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2356.StraightBevelDiffGearSystemDeflection]':
        '''List[StraightBevelDiffGearSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2356.StraightBevelDiffGearSystemDeflection))
        return value
