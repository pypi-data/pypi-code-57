'''_3922.py

ImportedFEComponentModalAnalysis
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _1924
from mastapy.system_model.analyses_and_results.static_loads import _2281
from mastapy.system_model.analyses_and_results.system_deflections import _2280
from mastapy.nodal_analysis.component_mode_synthesis import _219
from mastapy.system_model.analyses_and_results.modal_analyses import _3911
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_COMPONENT_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ImportedFEComponentModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponentModalAnalysis',)


class ImportedFEComponentModalAnalysis(_3911.AbstractShaftOrHousingModalAnalysis):
    '''ImportedFEComponentModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponentModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def calculate_mode_shapes(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CalculateModeShapes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateModeShapes

    @property
    def calculate_selected_strain_and_kinetic_energy(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CalculateSelectedStrainAndKineticEnergy' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateSelectedStrainAndKineticEnergy

    @property
    def calculate_all_strain_and_kinetic_energies(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CalculateAllStrainAndKineticEnergies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateAllStrainAndKineticEnergies

    @property
    def component_design(self) -> '_1924.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1924.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2281.ImportedFEComponentLoadCase':
        '''ImportedFEComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2281.ImportedFEComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2280.ImportedFEComponentSystemDeflection':
        '''ImportedFEComponentSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2280.ImportedFEComponentSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[ImportedFEComponentModalAnalysis]':
        '''List[ImportedFEComponentModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ImportedFEComponentModalAnalysis))
        return value

    @property
    def modal_full_fe_results(self) -> 'List[_219.ModalCMSResults]':
        '''List[ModalCMSResults]: 'ModalFullFEResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ModalFullFEResults, constructor.new(_219.ModalCMSResults))
        return value
