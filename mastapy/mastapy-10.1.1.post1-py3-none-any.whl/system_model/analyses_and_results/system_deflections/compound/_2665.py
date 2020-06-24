'''_2665.py

ConicalGearMeshCompoundSystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2240
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2686
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ConicalGearMeshCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearMeshCompoundSystemDeflection',)


class ConicalGearMeshCompoundSystemDeflection(_2686.GearMeshCompoundSystemDeflection):
    '''ConicalGearMeshCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearMeshCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def planetaries(self) -> 'List[ConicalGearMeshCompoundSystemDeflection]':
        '''List[ConicalGearMeshCompoundSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ConicalGearMeshCompoundSystemDeflection))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_2240.ConicalGearMeshSystemDeflection]':
        '''List[ConicalGearMeshSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2240.ConicalGearMeshSystemDeflection))
        return value
