'''_5326.py

GuideDxfModelGearWhineAnalysis
'''


from mastapy.system_model.part_model import _1998
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6124
from mastapy.system_model.analyses_and_results.system_deflections import _2270
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5277
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'GuideDxfModelGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelGearWhineAnalysis',)


class GuideDxfModelGearWhineAnalysis(_5277.ComponentGearWhineAnalysis):
    '''GuideDxfModelGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1998.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1998.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6124.GuideDxfModelLoadCase':
        '''GuideDxfModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6124.GuideDxfModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2270.GuideDxfModelSystemDeflection':
        '''GuideDxfModelSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2270.GuideDxfModelSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
