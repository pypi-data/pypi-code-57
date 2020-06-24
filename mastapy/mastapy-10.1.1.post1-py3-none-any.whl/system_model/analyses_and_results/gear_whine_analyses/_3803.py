'''_3803.py

ImportedFEComponentGearWhineAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _3922
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _6205, _3792
from mastapy.system_model.part_model import _1924
from mastapy.system_model.analyses_and_results.static_loads import _2281
from mastapy.system_model.analyses_and_results.system_deflections import _2280
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_COMPONENT_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ImportedFEComponentGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponentGearWhineAnalysis',)


class ImportedFEComponentGearWhineAnalysis(_3792.AbstractShaftOrHousingGearWhineAnalysis):
    '''ImportedFEComponentGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponentGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def export_displacements(self) -> 'str':
        '''str: 'ExportDisplacements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExportDisplacements

    @property
    def export_velocities(self) -> 'str':
        '''str: 'ExportVelocities' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExportVelocities

    @property
    def export_accelerations(self) -> 'str':
        '''str: 'ExportAccelerations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExportAccelerations

    @property
    def export_forces(self) -> 'str':
        '''str: 'ExportForces' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExportForces

    @property
    def coupled_modal_analysis(self) -> '_3922.ImportedFEComponentModalAnalysis':
        '''ImportedFEComponentModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3922.ImportedFEComponentModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def export(self) -> '_6205.GearWhineAnalysisFEExportOptions':
        '''GearWhineAnalysisFEExportOptions: 'Export' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6205.GearWhineAnalysisFEExportOptions)(self.wrapped.Export) if self.wrapped.Export else None

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
    def planetaries(self) -> 'List[ImportedFEComponentGearWhineAnalysis]':
        '''List[ImportedFEComponentGearWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ImportedFEComponentGearWhineAnalysis))
        return value
