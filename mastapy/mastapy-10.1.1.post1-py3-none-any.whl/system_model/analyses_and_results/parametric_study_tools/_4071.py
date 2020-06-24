'''_4071.py

CylindricalGearSetParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _1968
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2328
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4070, _4020, _4074
from mastapy.system_model.analyses_and_results.system_deflections import _2374
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'CylindricalGearSetParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetParametricStudyTool',)


class CylindricalGearSetParametricStudyTool(_4074.GearSetParametricStudyTool):
    '''CylindricalGearSetParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1968.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2328.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2328.CylindricalGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def cylindrical_gears_parametric_study_tool(self) -> 'List[_4070.CylindricalGearParametricStudyTool]':
        '''List[CylindricalGearParametricStudyTool]: 'CylindricalGearsParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsParametricStudyTool, constructor.new(_4070.CylindricalGearParametricStudyTool))
        return value

    @property
    def cylindrical_meshes_parametric_study_tool(self) -> 'List[_4020.CylindricalGearMeshParametricStudyTool]':
        '''List[CylindricalGearMeshParametricStudyTool]: 'CylindricalMeshesParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesParametricStudyTool, constructor.new(_4020.CylindricalGearMeshParametricStudyTool))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2374.CylindricalGearSetSystemDeflection]':
        '''List[CylindricalGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2374.CylindricalGearSetSystemDeflection))
        return value
