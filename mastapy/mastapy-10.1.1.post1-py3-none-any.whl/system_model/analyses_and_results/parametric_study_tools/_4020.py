'''_4020.py

CylindricalGearMeshParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1798
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2244
from mastapy.system_model.analyses_and_results.system_deflections import _2372
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4029
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'CylindricalGearMeshParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshParametricStudyTool',)


class CylindricalGearMeshParametricStudyTool(_4029.GearMeshParametricStudyTool):
    '''CylindricalGearMeshParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1798.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1798.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2244.CylindricalGearMeshLoadCase':
        '''CylindricalGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2244.CylindricalGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshParametricStudyTool]':
        '''List[CylindricalGearMeshParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshParametricStudyTool))
        return value

    @property
    def connection_system_deflection_results(self) -> 'List[_2372.CylindricalGearMeshSystemDeflection]':
        '''List[CylindricalGearMeshSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2372.CylindricalGearMeshSystemDeflection))
        return value
