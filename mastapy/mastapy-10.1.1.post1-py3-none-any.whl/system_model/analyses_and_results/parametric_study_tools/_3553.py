'''_3553.py

PartToPartShearCouplingConnectionParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1900
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6156
from mastapy.system_model.analyses_and_results.system_deflections import _2293
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3498
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'PartToPartShearCouplingConnectionParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingConnectionParametricStudyTool',)


class PartToPartShearCouplingConnectionParametricStudyTool(_3498.CouplingConnectionParametricStudyTool):
    '''PartToPartShearCouplingConnectionParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_CONNECTION_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingConnectionParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1900.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1900.PartToPartShearCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6156.PartToPartShearCouplingConnectionLoadCase':
        '''PartToPartShearCouplingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6156.PartToPartShearCouplingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2293.PartToPartShearCouplingConnectionSystemDeflection]':
        '''List[PartToPartShearCouplingConnectionSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2293.PartToPartShearCouplingConnectionSystemDeflection))
        return value
