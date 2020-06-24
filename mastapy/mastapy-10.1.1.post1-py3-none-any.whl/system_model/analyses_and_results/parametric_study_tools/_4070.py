'''_4070.py

CylindricalGearParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _1996
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2326
from mastapy.system_model.analyses_and_results.system_deflections import _2376
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4073
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'CylindricalGearParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearParametricStudyTool',)


class CylindricalGearParametricStudyTool(_4073.GearParametricStudyTool):
    '''CylindricalGearParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1996.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1996.CylindricalGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2326.CylindricalGearLoadCase':
        '''CylindricalGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2326.CylindricalGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[CylindricalGearParametricStudyTool]':
        '''List[CylindricalGearParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearParametricStudyTool))
        return value

    @property
    def component_system_deflection_results(self) -> 'List[_2376.CylindricalGearSystemDeflection]':
        '''List[CylindricalGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2376.CylindricalGearSystemDeflection))
        return value
