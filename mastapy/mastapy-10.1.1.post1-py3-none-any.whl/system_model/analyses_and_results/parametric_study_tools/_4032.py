'''_4032.py

BearingParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _1908
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2265
from mastapy.bearings.bearing_results import _1521
from mastapy.system_model.analyses_and_results.system_deflections import _2141
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4036
from mastapy._internal.python_net import python_net_import

_BEARING_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'BearingParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingParametricStudyTool',)


class BearingParametricStudyTool(_4036.ConnectorParametricStudyTool):
    '''BearingParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BEARING_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1908.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1908.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2265.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2265.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def bearing_duty_cycle_results(self) -> 'List[_1521.LoadedBearingDutyCycle]':
        '''List[LoadedBearingDutyCycle]: 'BearingDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BearingDutyCycleResults, constructor.new(_1521.LoadedBearingDutyCycle))
        return value

    @property
    def planetaries(self) -> 'List[BearingParametricStudyTool]':
        '''List[BearingParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingParametricStudyTool))
        return value

    @property
    def component_system_deflection_results(self) -> 'List[_2141.BearingSystemDeflection]':
        '''List[BearingSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2141.BearingSystemDeflection))
        return value
