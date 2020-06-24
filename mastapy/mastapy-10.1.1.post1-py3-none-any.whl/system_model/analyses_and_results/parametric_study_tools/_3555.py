'''_3555.py

PartToPartShearCouplingParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2122
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6158
from mastapy.system_model.analyses_and_results.system_deflections import _2295
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3500
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'PartToPartShearCouplingParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingParametricStudyTool',)


class PartToPartShearCouplingParametricStudyTool(_3500.CouplingParametricStudyTool):
    '''PartToPartShearCouplingParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingParametricStudyTool.TYPE'):
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

    @property
    def assembly_system_deflection_results(self) -> 'List[_2295.PartToPartShearCouplingSystemDeflection]':
        '''List[PartToPartShearCouplingSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2295.PartToPartShearCouplingSystemDeflection))
        return value
