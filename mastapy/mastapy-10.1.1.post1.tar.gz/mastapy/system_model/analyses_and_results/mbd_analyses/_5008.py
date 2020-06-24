'''_5008.py

CVTMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2120
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _4976
from mastapy._internal.python_net import python_net_import

_CVT_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'CVTMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTMultiBodyDynamicsAnalysis',)


class CVTMultiBodyDynamicsAnalysis(_4976.BeltDriveMultiBodyDynamicsAnalysis):
    '''CVTMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2120.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2120.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
