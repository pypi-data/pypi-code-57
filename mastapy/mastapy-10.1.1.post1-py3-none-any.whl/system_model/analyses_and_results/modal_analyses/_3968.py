'''_3968.py

StraightBevelGearModalAnalysis
'''


from mastapy.system_model.part_model.gears import _2006
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2361
from mastapy.system_model.analyses_and_results.system_deflections import _2360
from mastapy.system_model.analyses_and_results.modal_analyses import _3946
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'StraightBevelGearModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearModalAnalysis',)


class StraightBevelGearModalAnalysis(_3946.BevelGearModalAnalysis):
    '''StraightBevelGearModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2006.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2006.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2361.StraightBevelGearLoadCase':
        '''StraightBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2361.StraightBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2360.StraightBevelGearSystemDeflection':
        '''StraightBevelGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2360.StraightBevelGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
