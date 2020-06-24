'''_4290.py

PartToPartShearCouplingModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.couplings import _2122
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6158
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4249
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'PartToPartShearCouplingModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingModalAnalysisAtAStiffness',)


class PartToPartShearCouplingModalAnalysisAtAStiffness(_4249.CouplingModalAnalysisAtAStiffness):
    '''PartToPartShearCouplingModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2122.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2122.PartToPartShearCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6158.PartToPartShearCouplingLoadCase':
        '''PartToPartShearCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6158.PartToPartShearCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
