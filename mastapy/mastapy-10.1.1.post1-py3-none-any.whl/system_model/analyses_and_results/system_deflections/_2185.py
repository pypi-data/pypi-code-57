'''_2185.py

PulleySystemDeflection
'''


from mastapy.system_model.part_model.couplings import _2017
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2186
from mastapy.system_model.analyses_and_results.system_deflections import _2179
from mastapy._internal.python_net import python_net_import

_PULLEY_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'PulleySystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleySystemDeflection',)


class PulleySystemDeflection(_2179.CouplingHalfSystemDeflection):
    '''PulleySystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PULLEY_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleySystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2017.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2017.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2186.PulleyLoadCase':
        '''PulleyLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2186.PulleyLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
