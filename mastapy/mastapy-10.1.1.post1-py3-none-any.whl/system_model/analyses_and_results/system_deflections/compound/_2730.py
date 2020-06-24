'''_2730.py

StraightBevelDiffGearMeshCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1814
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2237
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2649
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'StraightBevelDiffGearMeshCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearMeshCompoundSystemDeflection',)


class StraightBevelDiffGearMeshCompoundSystemDeflection(_2649.BevelGearMeshCompoundSystemDeflection):
    '''StraightBevelDiffGearMeshCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearMeshCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1814.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1814.StraightBevelDiffGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1814.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1814.StraightBevelDiffGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2237.StraightBevelDiffGearMeshSystemDeflection]':
        '''List[StraightBevelDiffGearMeshSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2237.StraightBevelDiffGearMeshSystemDeflection))
        return value

    @property
    def connection_system_deflection_load_cases(self) -> 'List[_2237.StraightBevelDiffGearMeshSystemDeflection]':
        '''List[StraightBevelDiffGearMeshSystemDeflection]: 'ConnectionSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionLoadCases, constructor.new(_2237.StraightBevelDiffGearMeshSystemDeflection))
        return value
