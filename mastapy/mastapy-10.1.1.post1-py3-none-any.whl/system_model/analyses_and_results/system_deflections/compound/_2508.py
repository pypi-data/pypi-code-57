'''_2508.py

TorqueConverterTurbineCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2046
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2267
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2435
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'TorqueConverterTurbineCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineCompoundSystemDeflection',)


class TorqueConverterTurbineCompoundSystemDeflection(_2435.CouplingHalfCompoundSystemDeflection):
    '''TorqueConverterTurbineCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_COMPOUND_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2046.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2046.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2267.TorqueConverterTurbineSystemDeflection]':
        '''List[TorqueConverterTurbineSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2267.TorqueConverterTurbineSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2267.TorqueConverterTurbineSystemDeflection]':
        '''List[TorqueConverterTurbineSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2267.TorqueConverterTurbineSystemDeflection))
        return value
