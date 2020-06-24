'''_5254.py

AbstractShaftOrHousingGearWhineAnalysis
'''


from mastapy.system_model.part_model import _1982, _2001
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _2022
from mastapy.system_model.analyses_and_results.system_deflections import _2208, _2274, _2308
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5277
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_OR_HOUSING_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'AbstractShaftOrHousingGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftOrHousingGearWhineAnalysis',)


class AbstractShaftOrHousingGearWhineAnalysis(_5277.ComponentGearWhineAnalysis):
    '''AbstractShaftOrHousingGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_OR_HOUSING_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftOrHousingGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1982.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1982.AbstractShaftOrHousing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_imported_fe_component(self) -> '_2001.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.ImportedFEComponent.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ImportedFEComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2001.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft(self) -> '_2022.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.Shaft.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Shaft. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2022.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def system_deflection_results(self) -> '_2208.AbstractShaftOrHousingSystemDeflection':
        '''AbstractShaftOrHousingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2208.AbstractShaftOrHousingSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def system_deflection_results_of_type_imported_fe_component_system_deflection(self) -> '_2274.ImportedFEComponentSystemDeflection':
        '''ImportedFEComponentSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2274.ImportedFEComponentSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ImportedFEComponentSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new(_2274.ImportedFEComponentSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def system_deflection_results_of_type_shaft_system_deflection(self) -> '_2308.ShaftSystemDeflection':
        '''ShaftSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2308.ShaftSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to ShaftSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new(_2308.ShaftSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
