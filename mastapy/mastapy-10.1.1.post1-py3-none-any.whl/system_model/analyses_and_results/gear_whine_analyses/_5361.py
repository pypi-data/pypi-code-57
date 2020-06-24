'''_5361.py

ShaftGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.modal_analyses import _4794
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _2022
from mastapy.system_model.analyses_and_results.static_loads import _6174
from mastapy.system_model.analyses_and_results.system_deflections import _2308
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5254
from mastapy._internal.python_net import python_net_import

_SHAFT_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ShaftGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftGearWhineAnalysis',)


class ShaftGearWhineAnalysis(_5254.AbstractShaftOrHousingGearWhineAnalysis):
    '''ShaftGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def coupled_modal_analysis(self) -> '_4794.ShaftModalAnalysis':
        '''ShaftModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4794.ShaftModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def component_design(self) -> '_2022.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2022.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6174.ShaftLoadCase':
        '''ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6174.ShaftLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2308.ShaftSystemDeflection':
        '''ShaftSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2308.ShaftSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[ShaftGearWhineAnalysis]':
        '''List[ShaftGearWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftGearWhineAnalysis))
        return value
