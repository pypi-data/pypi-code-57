'''_4230.py

TorqueConverterSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _1999
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2206
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4216
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'TorqueConverterSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterSingleMeshWhineAnalysis',)


class TorqueConverterSingleMeshWhineAnalysis(_4216.CouplingSingleMeshWhineAnalysis):
    '''TorqueConverterSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1999.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1999.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2206.TorqueConverterLoadCase':
        '''TorqueConverterLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2206.TorqueConverterLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
