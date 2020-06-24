'''_3816.py

ShaftGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.modal_analyses import _3935
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _1942
from mastapy.system_model.analyses_and_results.static_loads import _2306
from mastapy.system_model.analyses_and_results.system_deflections import _2066
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3792
from mastapy._internal.python_net import python_net_import

_SHAFT_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ShaftGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftGearWhineAnalysis',)


class ShaftGearWhineAnalysis(_3792.AbstractShaftOrHousingGearWhineAnalysis):
    '''ShaftGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def coupled_modal_analysis(self) -> '_3935.ShaftModalAnalysis':
        '''ShaftModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3935.ShaftModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def component_design(self) -> '_1942.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1942.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2306.ShaftLoadCase':
        '''ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2306.ShaftLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2066.ShaftSystemDeflection':
        '''ShaftSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2066.ShaftSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[ShaftGearWhineAnalysis]':
        '''List[ShaftGearWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftGearWhineAnalysis))
        return value
