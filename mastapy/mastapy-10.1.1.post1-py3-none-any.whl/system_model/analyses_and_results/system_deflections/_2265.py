'''_2265.py

FaceGearSystemDeflection
'''


from mastapy.system_model.part_model.gears import _2067
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6113
from mastapy.system_model.analyses_and_results.power_flows import _3265
from mastapy.gears.rating.face import _250
from mastapy.system_model.analyses_and_results.system_deflections import _2269
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'FaceGearSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSystemDeflection',)


class FaceGearSystemDeflection(_2269.GearSystemDeflection):
    '''FaceGearSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2067.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2067.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6113.FaceGearLoadCase':
        '''FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6113.FaceGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3265.FaceGearPowerFlow':
        '''FaceGearPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3265.FaceGearPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def component_detailed_analysis(self) -> '_250.FaceGearRating':
        '''FaceGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_250.FaceGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
