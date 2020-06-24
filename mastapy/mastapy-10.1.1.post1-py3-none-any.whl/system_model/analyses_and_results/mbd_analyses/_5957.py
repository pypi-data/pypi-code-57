'''_5957.py

FaceGearMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.gears import _1997
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2310
from mastapy.system_model.analyses_and_results.mbd_analyses import _5962
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'FaceGearMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMultiBodyDynamicsAnalysis',)


class FaceGearMultiBodyDynamicsAnalysis(_5962.GearMultiBodyDynamicsAnalysis):
    '''FaceGearMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1997.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1997.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2310.FaceGearLoadCase':
        '''FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2310.FaceGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
