'''_5010.py

RootAssemblyModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model import _1935
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _4962, _4929
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'RootAssemblyModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyModalAnalysesAtStiffnesses',)


class RootAssemblyModalAnalysesAtStiffnesses(_4929.AssemblyModalAnalysesAtStiffnesses):
    '''RootAssemblyModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1935.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1935.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def modal_analyses_at_stiffnesses_inputs(self) -> '_4962.CriticalSpeedAnalysis':
        '''CriticalSpeedAnalysis: 'ModalAnalysesAtStiffnessesInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4962.CriticalSpeedAnalysis)(self.wrapped.ModalAnalysesAtStiffnessesInputs) if self.wrapped.ModalAnalysesAtStiffnessesInputs else None
