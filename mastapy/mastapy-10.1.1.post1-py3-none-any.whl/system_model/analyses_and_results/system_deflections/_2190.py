'''_2190.py

ExternalCADModelSystemDeflection
'''


from mastapy.system_model.part_model import _1919
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2315
from mastapy.system_model.analyses_and_results.system_deflections import _2159
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ExternalCADModelSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelSystemDeflection',)


class ExternalCADModelSystemDeflection(_2159.ComponentSystemDeflection):
    '''ExternalCADModelSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1919.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1919.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2315.ExternalCADModelLoadCase':
        '''ExternalCADModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2315.ExternalCADModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
