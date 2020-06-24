'''_3775.py

ConceptGearMeshGearWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1794
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2234
from mastapy.system_model.analyses_and_results.system_deflections import _2163
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3790
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ConceptGearMeshGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshGearWhineAnalysis',)


class ConceptGearMeshGearWhineAnalysis(_3790.GearMeshGearWhineAnalysis):
    '''ConceptGearMeshGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1794.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1794.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2234.ConceptGearMeshLoadCase':
        '''ConceptGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2234.ConceptGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2163.ConceptGearMeshSystemDeflection':
        '''ConceptGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2163.ConceptGearMeshSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
