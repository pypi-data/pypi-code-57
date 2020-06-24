'''_2591.py

PlanetCarrierCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _1932
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2292
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2586
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'PlanetCarrierCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierCompoundSystemDeflection',)


class PlanetCarrierCompoundSystemDeflection(_2586.MountableComponentCompoundSystemDeflection):
    '''PlanetCarrierCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_COMPOUND_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1932.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1932.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2292.PlanetCarrierSystemDeflection]':
        '''List[PlanetCarrierSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2292.PlanetCarrierSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2292.PlanetCarrierSystemDeflection]':
        '''List[PlanetCarrierSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2292.PlanetCarrierSystemDeflection))
        return value
