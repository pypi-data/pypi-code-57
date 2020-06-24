'''_4804.py

StraightBevelDiffGearMeshModalAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1886
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6186
from mastapy.system_model.analyses_and_results.system_deflections import _2317
from mastapy.system_model.analyses_and_results.modal_analyses import _4713
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'StraightBevelDiffGearMeshModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearMeshModalAnalysis',)


class StraightBevelDiffGearMeshModalAnalysis(_4713.BevelGearMeshModalAnalysis):
    '''StraightBevelDiffGearMeshModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearMeshModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1886.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1886.StraightBevelDiffGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6186.StraightBevelDiffGearMeshLoadCase':
        '''StraightBevelDiffGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6186.StraightBevelDiffGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2317.StraightBevelDiffGearMeshSystemDeflection':
        '''StraightBevelDiffGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2317.StraightBevelDiffGearMeshSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
