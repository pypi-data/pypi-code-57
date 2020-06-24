'''_4219.py

CVTPulleySingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2032
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4220
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'CVTPulleySingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleySingleMeshWhineAnalysis',)


class CVTPulleySingleMeshWhineAnalysis(_4220.PulleySingleMeshWhineAnalysis):
    '''CVTPulleySingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleySingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2032.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2032.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
