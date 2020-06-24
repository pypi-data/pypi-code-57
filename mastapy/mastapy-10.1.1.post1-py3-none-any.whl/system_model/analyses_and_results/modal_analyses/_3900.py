'''_3900.py

CylindricalGearMeshModalAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1798
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2244
from mastapy.system_model.analyses_and_results.system_deflections import _2372, _2373, _2243
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.modal_analyses import _3909
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'CylindricalGearMeshModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshModalAnalysis',)


class CylindricalGearMeshModalAnalysis(_3909.GearMeshModalAnalysis):
    '''CylindricalGearMeshModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1798.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1798.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2244.CylindricalGearMeshLoadCase':
        '''CylindricalGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2244.CylindricalGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2372.CylindricalGearMeshSystemDeflection':
        '''CylindricalGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2372.CylindricalGearMeshSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def system_deflection_results_of_type_cylindrical_gear_mesh_system_deflection_timestep(self) -> '_2373.CylindricalGearMeshSystemDeflectionTimestep':
        '''CylindricalGearMeshSystemDeflectionTimestep: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.SystemDeflectionResults.__class__.__qualname__ != 'CylindricalGearMeshSystemDeflectionTimestep':
            raise CastException('Failed to cast system_deflection_results to CylindricalGearMeshSystemDeflectionTimestep. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new(_2373.CylindricalGearMeshSystemDeflectionTimestep)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def system_deflection_results_of_type_cylindrical_gear_mesh_system_deflection_with_ltca_results(self) -> '_2243.CylindricalGearMeshSystemDeflectionWithLTCAResults':
        '''CylindricalGearMeshSystemDeflectionWithLTCAResults: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.SystemDeflectionResults.__class__.__qualname__ != 'CylindricalGearMeshSystemDeflectionWithLTCAResults':
            raise CastException('Failed to cast system_deflection_results to CylindricalGearMeshSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new(_2243.CylindricalGearMeshSystemDeflectionWithLTCAResults)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshModalAnalysis]':
        '''List[CylindricalGearMeshModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshModalAnalysis))
        return value
