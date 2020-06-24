'''_3554.py

PartToPartShearCouplingHalfParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2123
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6157
from mastapy.system_model.analyses_and_results.system_deflections import _2294
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3499
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_HALF_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'PartToPartShearCouplingHalfParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingHalfParametricStudyTool',)


class PartToPartShearCouplingHalfParametricStudyTool(_3499.CouplingHalfParametricStudyTool):
    '''PartToPartShearCouplingHalfParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_HALF_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingHalfParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2123.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2123.PartToPartShearCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6157.PartToPartShearCouplingHalfLoadCase':
        '''PartToPartShearCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6157.PartToPartShearCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2294.PartToPartShearCouplingHalfSystemDeflection]':
        '''List[PartToPartShearCouplingHalfSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2294.PartToPartShearCouplingHalfSystemDeflection))
        return value
